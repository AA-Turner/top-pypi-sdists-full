r'''
# `google_os_config_v2_policy_orchestrator_for_organization`

Refer to the Terraform Registry for docs: [`google_os_config_v2_policy_orchestrator_for_organization`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization).
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


class OsConfigV2PolicyOrchestratorForOrganization(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganization",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization google_os_config_v2_policy_orchestrator_for_organization}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        orchestrated_resource: typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource", typing.Dict[builtins.str, typing.Any]],
        organization_id: builtins.str,
        policy_orchestrator_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        orchestration_scope: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope", typing.Dict[builtins.str, typing.Any]]] = None,
        state: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization google_os_config_v2_policy_orchestrator_for_organization} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: Required. Action to be done by the orchestrator in 'projects/{project_id}/zones/{zone_id}' locations defined by the 'orchestration_scope'. Allowed values: - 'UPSERT' - Orchestrator will create or update target resources. - 'DELETE' - Orchestrator will delete target resources, if they exist Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#action OsConfigV2PolicyOrchestratorForOrganization#action}
        :param orchestrated_resource: orchestrated_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#orchestrated_resource OsConfigV2PolicyOrchestratorForOrganization#orchestrated_resource}
        :param organization_id: Part of 'parent'. Required. The parent resource name in the form of: * 'organizations/{organization_id}/locations/global' * 'folders/{folder_id}/locations/global' * 'projects/{project_id_or_number}/locations/global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#organization_id OsConfigV2PolicyOrchestratorForOrganization#organization_id}
        :param policy_orchestrator_id: Required. The logical identifier of the policy orchestrator, with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#policy_orchestrator_id OsConfigV2PolicyOrchestratorForOrganization#policy_orchestrator_id}
        :param description: Optional. Freeform text describing the purpose of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#description OsConfigV2PolicyOrchestratorForOrganization#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#labels OsConfigV2PolicyOrchestratorForOrganization#labels}
        :param orchestration_scope: orchestration_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#orchestration_scope OsConfigV2PolicyOrchestratorForOrganization#orchestration_scope}
        :param state: Optional. State of the orchestrator. Can be updated to change orchestrator behaviour. Allowed values: - 'ACTIVE' - orchestrator is actively looking for actions to be taken. - 'STOPPED' - orchestrator won't make any changes. Note: There might be more states added in the future. We use string here instead of an enum, to avoid the need of propagating new states to all the client code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#state OsConfigV2PolicyOrchestratorForOrganization#state}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#timeouts OsConfigV2PolicyOrchestratorForOrganization#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b10b215bc8f6831dcf7e393a540c23b15d4a062df33764508187f232783651)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OsConfigV2PolicyOrchestratorForOrganizationConfig(
            action=action,
            orchestrated_resource=orchestrated_resource,
            organization_id=organization_id,
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
        '''Generates CDKTF code for importing a OsConfigV2PolicyOrchestratorForOrganization resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OsConfigV2PolicyOrchestratorForOrganization to import.
        :param import_from_id: The id of the existing OsConfigV2PolicyOrchestratorForOrganization that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OsConfigV2PolicyOrchestratorForOrganization to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b362b9a8490da3b2019c0331db09e0b6da6e7c999553819585484b97356f5d)
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
        os_policy_assignment_v1_payload: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Optional. ID of the resource to be used while generating set of affected resources. For UPSERT action the value is auto-generated during PolicyOrchestrator creation when not set. When the value is set it should following next restrictions: - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. For DELETE action, ID must be specified explicitly during PolicyOrchestrator creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param os_policy_assignment_v1_payload: os_policy_assignment_v1_payload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_policy_assignment_v1_payload OsConfigV2PolicyOrchestratorForOrganization#os_policy_assignment_v1_payload}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource(
            id=id, os_policy_assignment_v1_payload=os_policy_assignment_v1_payload
        )

        return typing.cast(None, jsii.invoke(self, "putOrchestratedResource", [value]))

    @jsii.member(jsii_name="putOrchestrationScope")
    def put_orchestration_scope(
        self,
        *,
        selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#selectors OsConfigV2PolicyOrchestratorForOrganization#selectors}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#create OsConfigV2PolicyOrchestratorForOrganization#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#delete OsConfigV2PolicyOrchestratorForOrganization#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#update OsConfigV2PolicyOrchestratorForOrganization#update}.
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationTimeouts(
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
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOutputReference", jsii.get(self, "orchestratedResource"))

    @builtins.property
    @jsii.member(jsii_name="orchestrationScope")
    def orchestration_scope(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeOutputReference", jsii.get(self, "orchestrationScope"))

    @builtins.property
    @jsii.member(jsii_name="orchestrationState")
    def orchestration_state(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateList":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateList", jsii.get(self, "orchestrationState"))

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
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationTimeoutsOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource"], jsii.get(self, "orchestratedResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="orchestrationScopeInput")
    def orchestration_scope_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope"], jsii.get(self, "orchestrationScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationIdInput")
    def organization_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationIdInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OsConfigV2PolicyOrchestratorForOrganizationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OsConfigV2PolicyOrchestratorForOrganizationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de11a4572aa6400d4c3568cb569582c84670b0dbfea653c9115e82733a245827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4815037a7f562d48e20556ba1c5adfe349e90d92f16e5b7845acc9ff41939f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6dcc558da5320077df3d8f67306023b4e248b62a06b230b3e4e73d396debd02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__124865ff2019803ca1afabf0c5ac612dd2c3a282fd9e5f46b9531fcd9606cff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @organization_id.setter
    def organization_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c258fb683b99d22b7e9b9a18359c46127ca579c9c8580fb22005f49a907919d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyOrchestratorId")
    def policy_orchestrator_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyOrchestratorId"))

    @policy_orchestrator_id.setter
    def policy_orchestrator_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7bdfd2736d2f58a7da20ddc53d52f0e7511f74b7af0ab3d40e78b424bf178a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyOrchestratorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea73b4842082d97c4b76f958e50e9af5c78708071ce71dad2291becc5ae04c84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationConfig",
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
        "organization_id": "organizationId",
        "policy_orchestrator_id": "policyOrchestratorId",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "orchestration_scope": "orchestrationScope",
        "state": "state",
        "timeouts": "timeouts",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationConfig(
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
        orchestrated_resource: typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource", typing.Dict[builtins.str, typing.Any]],
        organization_id: builtins.str,
        policy_orchestrator_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        orchestration_scope: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope", typing.Dict[builtins.str, typing.Any]]] = None,
        state: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: Required. Action to be done by the orchestrator in 'projects/{project_id}/zones/{zone_id}' locations defined by the 'orchestration_scope'. Allowed values: - 'UPSERT' - Orchestrator will create or update target resources. - 'DELETE' - Orchestrator will delete target resources, if they exist Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#action OsConfigV2PolicyOrchestratorForOrganization#action}
        :param orchestrated_resource: orchestrated_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#orchestrated_resource OsConfigV2PolicyOrchestratorForOrganization#orchestrated_resource}
        :param organization_id: Part of 'parent'. Required. The parent resource name in the form of: * 'organizations/{organization_id}/locations/global' * 'folders/{folder_id}/locations/global' * 'projects/{project_id_or_number}/locations/global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#organization_id OsConfigV2PolicyOrchestratorForOrganization#organization_id}
        :param policy_orchestrator_id: Required. The logical identifier of the policy orchestrator, with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#policy_orchestrator_id OsConfigV2PolicyOrchestratorForOrganization#policy_orchestrator_id}
        :param description: Optional. Freeform text describing the purpose of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#description OsConfigV2PolicyOrchestratorForOrganization#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#labels OsConfigV2PolicyOrchestratorForOrganization#labels}
        :param orchestration_scope: orchestration_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#orchestration_scope OsConfigV2PolicyOrchestratorForOrganization#orchestration_scope}
        :param state: Optional. State of the orchestrator. Can be updated to change orchestrator behaviour. Allowed values: - 'ACTIVE' - orchestrator is actively looking for actions to be taken. - 'STOPPED' - orchestrator won't make any changes. Note: There might be more states added in the future. We use string here instead of an enum, to avoid the need of propagating new states to all the client code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#state OsConfigV2PolicyOrchestratorForOrganization#state}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#timeouts OsConfigV2PolicyOrchestratorForOrganization#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(orchestrated_resource, dict):
            orchestrated_resource = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource(**orchestrated_resource)
        if isinstance(orchestration_scope, dict):
            orchestration_scope = OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope(**orchestration_scope)
        if isinstance(timeouts, dict):
            timeouts = OsConfigV2PolicyOrchestratorForOrganizationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb798e48ca17ff16d26976b83a58d9d32d6ad52acdc532f17b5c9f2cbfc533d7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument orchestrated_resource", value=orchestrated_resource, expected_type=type_hints["orchestrated_resource"])
            check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
            check_type(argname="argument policy_orchestrator_id", value=policy_orchestrator_id, expected_type=type_hints["policy_orchestrator_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument orchestration_scope", value=orchestration_scope, expected_type=type_hints["orchestration_scope"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "orchestrated_resource": orchestrated_resource,
            "organization_id": organization_id,
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
        '''Required.

        Action to be done by the orchestrator in
        'projects/{project_id}/zones/{zone_id}' locations defined by the
        'orchestration_scope'. Allowed values:

        - 'UPSERT' - Orchestrator will create or update target resources.
        - 'DELETE' - Orchestrator will delete target resources, if they exist

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#action OsConfigV2PolicyOrchestratorForOrganization#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def orchestrated_resource(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource":
        '''orchestrated_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#orchestrated_resource OsConfigV2PolicyOrchestratorForOrganization#orchestrated_resource}
        '''
        result = self._values.get("orchestrated_resource")
        assert result is not None, "Required property 'orchestrated_resource' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource", result)

    @builtins.property
    def organization_id(self) -> builtins.str:
        '''Part of 'parent'. Required. The parent resource name in the form of: * 'organizations/{organization_id}/locations/global' * 'folders/{folder_id}/locations/global' * 'projects/{project_id_or_number}/locations/global'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#organization_id OsConfigV2PolicyOrchestratorForOrganization#organization_id}
        '''
        result = self._values.get("organization_id")
        assert result is not None, "Required property 'organization_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_orchestrator_id(self) -> builtins.str:
        '''Required. The logical identifier of the policy orchestrator, with the following restrictions:.

        - Must contain only lowercase letters, numbers, and hyphens.
        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the parent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#policy_orchestrator_id OsConfigV2PolicyOrchestratorForOrganization#policy_orchestrator_id}
        '''
        result = self._values.get("policy_orchestrator_id")
        assert result is not None, "Required property 'policy_orchestrator_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Freeform text describing the purpose of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#description OsConfigV2PolicyOrchestratorForOrganization#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#labels OsConfigV2PolicyOrchestratorForOrganization#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def orchestration_scope(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope"]:
        '''orchestration_scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#orchestration_scope OsConfigV2PolicyOrchestratorForOrganization#orchestration_scope}
        '''
        result = self._values.get("orchestration_scope")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#state OsConfigV2PolicyOrchestratorForOrganization#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#timeouts OsConfigV2PolicyOrchestratorForOrganization#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "os_policy_assignment_v1_payload": "osPolicyAssignmentV1Payload",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        os_policy_assignment_v1_payload: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Optional. ID of the resource to be used while generating set of affected resources. For UPSERT action the value is auto-generated during PolicyOrchestrator creation when not set. When the value is set it should following next restrictions: - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. For DELETE action, ID must be specified explicitly during PolicyOrchestrator creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param os_policy_assignment_v1_payload: os_policy_assignment_v1_payload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_policy_assignment_v1_payload OsConfigV2PolicyOrchestratorForOrganization#os_policy_assignment_v1_payload}
        '''
        if isinstance(os_policy_assignment_v1_payload, dict):
            os_policy_assignment_v1_payload = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload(**os_policy_assignment_v1_payload)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a69f1b258ef34f83f145214ac90a711295d189af4931c23f63c021fdb3df3243)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_policy_assignment_v1_payload(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload"]:
        '''os_policy_assignment_v1_payload block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_policy_assignment_v1_payload OsConfigV2PolicyOrchestratorForOrganization#os_policy_assignment_v1_payload}
        '''
        result = self._values.get("os_policy_assignment_v1_payload")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload",
    jsii_struct_bases=[],
    name_mapping={
        "instance_filter": "instanceFilter",
        "os_policies": "osPolicies",
        "rollout": "rollout",
        "description": "description",
        "etag": "etag",
        "name": "name",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload:
    def __init__(
        self,
        *,
        instance_filter: typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter", typing.Dict[builtins.str, typing.Any]],
        os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies", typing.Dict[builtins.str, typing.Any]]]],
        rollout: typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        etag: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#instance_filter OsConfigV2PolicyOrchestratorForOrganization#instance_filter}
        :param os_policies: os_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_policies OsConfigV2PolicyOrchestratorForOrganization#os_policies}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#rollout OsConfigV2PolicyOrchestratorForOrganization#rollout}
        :param description: OS policy assignment description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#description OsConfigV2PolicyOrchestratorForOrganization#description}
        :param etag: The etag for this OS policy assignment. If this is provided on update, it must match the server's etag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#etag OsConfigV2PolicyOrchestratorForOrganization#etag}
        :param name: Resource name. Format: 'projects/{project_number}/locations/{location}/osPolicyAssignments/{os_policy_assignment_id}' This field is ignored when you create an OS policy assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        if isinstance(instance_filter, dict):
            instance_filter = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter(**instance_filter)
        if isinstance(rollout, dict):
            rollout = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout(**rollout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f334dd60053a432ec4f5de094a39f8cf4260f12efb076a9d4bd44b45578c8c)
            check_type(argname="argument instance_filter", value=instance_filter, expected_type=type_hints["instance_filter"])
            check_type(argname="argument os_policies", value=os_policies, expected_type=type_hints["os_policies"])
            check_type(argname="argument rollout", value=rollout, expected_type=type_hints["rollout"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_filter": instance_filter,
            "os_policies": os_policies,
            "rollout": rollout,
        }
        if description is not None:
            self._values["description"] = description
        if etag is not None:
            self._values["etag"] = etag
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def instance_filter(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter":
        '''instance_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#instance_filter OsConfigV2PolicyOrchestratorForOrganization#instance_filter}
        '''
        result = self._values.get("instance_filter")
        assert result is not None, "Required property 'instance_filter' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter", result)

    @builtins.property
    def os_policies(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies"]]:
        '''os_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_policies OsConfigV2PolicyOrchestratorForOrganization#os_policies}
        '''
        result = self._values.get("os_policies")
        assert result is not None, "Required property 'os_policies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies"]], result)

    @builtins.property
    def rollout(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout":
        '''rollout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#rollout OsConfigV2PolicyOrchestratorForOrganization#rollout}
        '''
        result = self._values.get("rollout")
        assert result is not None, "Required property 'rollout' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''OS policy assignment description. Length of the description is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#description OsConfigV2PolicyOrchestratorForOrganization#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def etag(self) -> typing.Optional[builtins.str]:
        '''The etag for this OS policy assignment. If this is provided on update, it must match the server's etag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#etag OsConfigV2PolicyOrchestratorForOrganization#etag}
        '''
        result = self._values.get("etag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Resource name.

        Format:
        'projects/{project_number}/locations/{location}/osPolicyAssignments/{os_policy_assignment_id}'

        This field is ignored when you create an OS policy assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter",
    jsii_struct_bases=[],
    name_mapping={
        "all": "all",
        "exclusion_labels": "exclusionLabels",
        "inclusion_labels": "inclusionLabels",
        "inventories": "inventories",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all: Target all VMs in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#all OsConfigV2PolicyOrchestratorForOrganization#all}
        :param exclusion_labels: exclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#exclusion_labels OsConfigV2PolicyOrchestratorForOrganization#exclusion_labels}
        :param inclusion_labels: inclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#inclusion_labels OsConfigV2PolicyOrchestratorForOrganization#inclusion_labels}
        :param inventories: inventories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#inventories OsConfigV2PolicyOrchestratorForOrganization#inventories}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ac287c73be5ffae1e5fec1a8fb7b3500b9b1e3c2bb11d129832af946c6f207)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#all OsConfigV2PolicyOrchestratorForOrganization#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclusion_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels"]]]:
        '''exclusion_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#exclusion_labels OsConfigV2PolicyOrchestratorForOrganization#exclusion_labels}
        '''
        result = self._values.get("exclusion_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels"]]], result)

    @builtins.property
    def inclusion_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels"]]]:
        '''inclusion_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#inclusion_labels OsConfigV2PolicyOrchestratorForOrganization#inclusion_labels}
        '''
        result = self._values.get("inclusion_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels"]]], result)

    @builtins.property
    def inventories(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories"]]]:
        '''inventories block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#inventories OsConfigV2PolicyOrchestratorForOrganization#inventories}
        '''
        result = self._values.get("inventories")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Labels are identified by key/value pairs in this map. A VM should contain all the key/value pairs specified in this map to be selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#labels OsConfigV2PolicyOrchestratorForOrganization#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e85fb4cc96c37a94d2f5e2083b1a0cdf0a5338e96b741196d50d35fcf1afe28)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels are identified by key/value pairs in this map.

        A VM should contain all the key/value pairs specified in this
        map to be selected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#labels OsConfigV2PolicyOrchestratorForOrganization#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a65340af8a60ee405f5957700653e12fae00a926dc7ee9b512ae8a12c81b375e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e96f89aa1f6874e3bb2fde1ce240101c9d578781b6699e026c5e28de7ed419)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2524b89d52bfb39a39d2c078914674137d85db54903de531a19f879cc78d19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71725bc0e65b324651c257055d6c1e5d1b484301c9630d8f80fdd40d58804017)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae52b9f2afcefeaad5d1f6a9f70dd6a96ec6500680894b534c3550d0a9768db7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba2dd9ea98e2505619979b0bc821b6e581f78a3e307ea11d94fa808a933589a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6d6926c498f96b5405e80974e6ad57233dba6e11c92c091ddda3063ce32584b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be452cc3cf550dd304a0d3f7b00a1f690d82d3165b71328f84a7a2d94f4fba5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62aca8c672e823f6a0c741b5eddc099b1337ab09f2af6017738431efa3034a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Labels are identified by key/value pairs in this map. A VM should contain all the key/value pairs specified in this map to be selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#labels OsConfigV2PolicyOrchestratorForOrganization#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbede0ee2a585d21293e6bfe168f4f118f33d37ba34aa4330b94690ea3bf3f03)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels are identified by key/value pairs in this map.

        A VM should contain all the key/value pairs specified in this
        map to be selected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#labels OsConfigV2PolicyOrchestratorForOrganization#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3535a53a2ae9c7b9124d4d737818cf1a33da6839dccdadbbbc26e9f98d924a86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d6ec2ade62847d85c91f7802d21e240920f40dfea8414ae72eb425dbb96cdcd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__597814fb8c0af4f77fc101242c25bf2fcd0977ffc59879bfb6f6845d3867c517)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d07e5537f91b59470391a189ee40979a6807d99935751e2cad9a9b9a7a343d1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3760c77c23bcdf15b83574a14cf448a9b463ccdccb13062ec75fa5d23ab4f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a2e363b575c0cecbd488518d2705c9efbe26bc9a63139722e49362863519d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63c3906b6f790b84769ae1d2b4fbad86d10a2c96d4da915f298d864cb4f858ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afa6c4a29f993603f46ae7e7650323e3049c8923d7318d420171a315a4b8950f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758fc66f8840a70ff89c2122bcd121785b938fafb7fd88b22db7843eb76217db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories",
    jsii_struct_bases=[],
    name_mapping={"os_short_name": "osShortName", "os_version": "osVersion"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories:
    def __init__(
        self,
        *,
        os_short_name: builtins.str,
        os_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_short_name: Required. The OS short name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_short_name OsConfigV2PolicyOrchestratorForOrganization#os_short_name}
        :param os_version: The OS version. Prefix matches are supported if asterisk(*) is provided as the last character. For example, to match all versions with a major version of '7', specify the following value for this field '7.*' An empty string matches all OS versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_version OsConfigV2PolicyOrchestratorForOrganization#os_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d206cb5935bc9f5c4b14dae637a4d5681ae884a01be51b8705c9c68bb0ed4f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_short_name OsConfigV2PolicyOrchestratorForOrganization#os_short_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_version OsConfigV2PolicyOrchestratorForOrganization#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e9654e8ebfce074337abb13c726748819fed006e6cf48686b5a4ab7f82e77ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc90bddbb64fbd6856634a9adbaab679befab093aa9cce868f7067f9b1b5070)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d564a0c41f9486a843afdc35c7e0d699ff197f2bfac5656257927e79ae84a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae37c62672cdfefafd663cc61ad035e3d763932325083370e85a52e61c9e0fa1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1d972387a73d43a7cbc5db7443fb2a4c85eeb70c4bfda3ce1265a9067c58a1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290c5bb7a8674835df80fd18712a1f48e7dc8453c373f89cdfcbf57b92e5323f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b524a7d45efd7b1e396e4f2455962392774264794f5bdef8bde75eab6706a9a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59b7688e3b266eb810dfb75634d854a6d049c61088e94b89a22dd5fe2bc3d0c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osShortName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0079c8c1589e9fa0f6026a8bc798ad973d613063de7adfddda64234345476505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db22a34aba54fd757d9f1db2f13b897f01e9e46c62e182878fc5a55bfde7ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3c1c5811549f87cfa0318c73c8e6befda64b49610d59c2baa6b00f8d096f25c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusionLabels")
    def put_exclusion_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d467c5e18be762fc83320ab16549f2727b809b8a6c9eecfe06d43ed5551eb1f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusionLabels", [value]))

    @jsii.member(jsii_name="putInclusionLabels")
    def put_inclusion_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03035a3e3493fbde0fee940e687781a909b2fdaa993a2d5659cd8b4dc79441a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInclusionLabels", [value]))

    @jsii.member(jsii_name="putInventories")
    def put_inventories(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ad79fb61b466c58a3a2b63fd9227b175f9063bcab53430409307395cff1e12)
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList, jsii.get(self, "exclusionLabels"))

    @builtins.property
    @jsii.member(jsii_name="inclusionLabels")
    def inclusion_labels(
        self,
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList, jsii.get(self, "inclusionLabels"))

    @builtins.property
    @jsii.member(jsii_name="inventories")
    def inventories(
        self,
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList, jsii.get(self, "inventories"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]], jsii.get(self, "exclusionLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="inclusionLabelsInput")
    def inclusion_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]], jsii.get(self, "inclusionLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="inventoriesInput")
    def inventories_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]], jsii.get(self, "inventoriesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5a9adcfd1adc2e49637d1e7a69905a28edd06040d8760ed17a7b2062a5c035fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ace6c87dc6a37a82d4389e30bf0b8e2ca0f881dd3e3e86d1bf51eddea03d077d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "mode": "mode",
        "resource_groups": "resourceGroups",
        "allow_no_resource_group_match": "allowNoResourceGroupMatch",
        "description": "description",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies:
    def __init__(
        self,
        *,
        id: builtins.str,
        mode: builtins.str,
        resource_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups", typing.Dict[builtins.str, typing.Any]]]],
        allow_no_resource_group_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Required. The id of the OS policy with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mode: Required. Policy mode Possible values: MODE_UNSPECIFIED VALIDATION ENFORCEMENT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#mode OsConfigV2PolicyOrchestratorForOrganization#mode}
        :param resource_groups: resource_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#resource_groups OsConfigV2PolicyOrchestratorForOrganization#resource_groups}
        :param allow_no_resource_group_match: This flag determines the OS policy compliance status when none of the resource groups within the policy are applicable for a VM. Set this value to 'true' if the policy needs to be reported as compliant even if the policy has nothing to validate or enforce. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_no_resource_group_match OsConfigV2PolicyOrchestratorForOrganization#allow_no_resource_group_match}
        :param description: Policy description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#description OsConfigV2PolicyOrchestratorForOrganization#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc35915575d30f279ebae167e23642509633a08317a6dddd29d6fbe6bbae7b0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''Required. Policy mode Possible values: MODE_UNSPECIFIED VALIDATION ENFORCEMENT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#mode OsConfigV2PolicyOrchestratorForOrganization#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_groups(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]]:
        '''resource_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#resource_groups OsConfigV2PolicyOrchestratorForOrganization#resource_groups}
        '''
        result = self._values.get("resource_groups")
        assert result is not None, "Required property 'resource_groups' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]], result)

    @builtins.property
    def allow_no_resource_group_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag determines the OS policy compliance status when none of the resource groups within the policy are applicable for a VM.

        Set this value
        to 'true' if the policy needs to be reported as compliant even if the
        policy has nothing to validate or enforce.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_no_resource_group_match OsConfigV2PolicyOrchestratorForOrganization#allow_no_resource_group_match}
        '''
        result = self._values.get("allow_no_resource_group_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Policy description. Length of the description is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#description OsConfigV2PolicyOrchestratorForOrganization#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbd3420d4a87ca4ccce5378965c76e025c2db5c4cb7bbf4b219b5f5d681b9d75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ebdf04f9a135b9fa7f6e81e35a42430e2542bf6471ea457a74f527ae0e80ebb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcfeecee8da7a83e87072f5bf5e4f83bd3c9bfc8a547b712596cc34d663205cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d31faea6fef6479aaf070fd52fb19757634a347ced2f6a563c47832171bcdaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bab33e7b80dbb61218f45719c60a007713805c728f1470483f0b136c497a6fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2b0d57ba836090207cf590ecd1153f38d6b1ccdb757d0618b51b28c27c4934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a7e3b7dbe81c056b629397a7e1053a2be19c7d556eebdd82c66610b3c37c076)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putResourceGroups")
    def put_resource_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e3b62a22d17226c4111778cfa8dbd78199cec29701927ebfeff82485513658)
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
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList", jsii.get(self, "resourceGroups"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]]], jsii.get(self, "resourceGroupsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c16ca00f47c3772f77c5f279a0a9027bf4f7eb22e8bd78e26e3dae7f9c0f8e5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowNoResourceGroupMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aab65e3a52c4d15d52f5d1666b574afa6194a24f28956140c6a1007d4d6a66e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8352023fe8f718854fc39343b5b171d5b8633bf4595ea64270f8837f6e3ffc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1f14cd97a3cd27a1f31803735447642d8b80770ef14b12586277b8ac60b402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7f2d53f9c5660789413de3886f5899a268c0aea3ec6ec649652ee4d3771e08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups",
    jsii_struct_bases=[],
    name_mapping={"resources": "resources", "inventory_filters": "inventoryFilters"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups:
    def __init__(
        self,
        *,
        resources: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources", typing.Dict[builtins.str, typing.Any]]]],
        inventory_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#resources OsConfigV2PolicyOrchestratorForOrganization#resources}
        :param inventory_filters: inventory_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#inventory_filters OsConfigV2PolicyOrchestratorForOrganization#inventory_filters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f7a3fefe16a32d5befa24cab89ec47ae3506b7631a464f39f78c7bd7f23c56)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#resources OsConfigV2PolicyOrchestratorForOrganization#resources}
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]], result)

    @builtins.property
    def inventory_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters"]]]:
        '''inventory_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#inventory_filters OsConfigV2PolicyOrchestratorForOrganization#inventory_filters}
        '''
        result = self._values.get("inventory_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters",
    jsii_struct_bases=[],
    name_mapping={"os_short_name": "osShortName", "os_version": "osVersion"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters:
    def __init__(
        self,
        *,
        os_short_name: builtins.str,
        os_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_short_name: Required. The OS short name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_short_name OsConfigV2PolicyOrchestratorForOrganization#os_short_name}
        :param os_version: The OS version. Prefix matches are supported if asterisk(*) is provided as the last character. For example, to match all versions with a major version of '7', specify the following value for this field '7.*' An empty string matches all OS versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_version OsConfigV2PolicyOrchestratorForOrganization#os_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f120fd2b8624e5f99ec5a696677ce792dc654cac8daecd5dcd3c48b7a3f51102)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_short_name OsConfigV2PolicyOrchestratorForOrganization#os_short_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_version OsConfigV2PolicyOrchestratorForOrganization#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c074b729b7d610e54bf35e43db4827daffeb65eda1094301a60eec4d7a6a7c9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8826674e85c4d4c9b3f99c9ddab976338b69637f6cfe6c32478911aa5a9b41d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b33c7aed9ffd5d861299ae1d57e83042904b09fd33312dc94acc297636b5df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0144b90cbdc53ccb3abb9a45f020576eed3038373a0b1f785a4ece935fe0b139)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4413249de279dc056e383a2b2aa272db7da810761e53c0f1757436ff593847a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54381a8108e902b5eb5a4ccce8feb7d71b39fab02ab399abe20bc3f52e6047a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eeb732b93ae0eec89a027ec678d5a9f8bd534357d1eeae425131ceddddb16479)
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
            type_hints = typing.get_type_hints(_typecheckingstub__883536077b292ed761b79dc31a8cfbdfd5910f4024e4863bd2abef67a6ef7630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osShortName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5de236e2171f14f9804bc3cc531d6087f05876bdd20b4e4a16f97eed0faa6da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635fa39f7cc624107a2ee4f17ef31ab07b0ae448cac98d1427411dfbfb17d80a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__173a0b3334d4670f340c0417b7ee124309f89eba60613c4aa659260304169092)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc83b69f9310d3b3708d0a36837cddf943f05df34696f4bf21de33732afc489b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d04f37e8d5af5a8f220e20fec0c6bf97039683cacda0b6758ddc4ad66c7414)
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
            type_hints = typing.get_type_hints(_typecheckingstub__826ecbe907ac36b7bcec7b50dca1a333bf75e1c832109c6db6bb4ab59172e9f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efb9b15dc639b8711636876ae3553b845d375a3a0d556703239e244c7dcf93bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__128b6999df7feed3a4f6bbf773e90b6061623772daef9c77da37907fa321f9d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f036d48becca546b597d80aa0136f9bcb0d44ec1473a14196fad040836968bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInventoryFilters")
    def put_inventory_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfc6d0140e680d93257f026f6d36a64bfd87e1155298ebceec0e344014ea5ba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInventoryFilters", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ebb0a0255f99715be58ef29a87a3f49ff6303dffe858f82bd3afc4ea429f88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="resetInventoryFilters")
    def reset_inventory_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInventoryFilters", []))

    @builtins.property
    @jsii.member(jsii_name="inventoryFilters")
    def inventory_filters(
        self,
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList, jsii.get(self, "inventoryFilters"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="inventoryFiltersInput")
    def inventory_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]], jsii.get(self, "inventoryFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947a4e8057d4e33fee5e6c14b7b8f5d2384d962801608cda9913d697010e8a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "exec": "exec",
        "file": "file",
        "pkg": "pkg",
        "repository": "repository",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources:
    def __init__(
        self,
        *,
        id: builtins.str,
        exec: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile", typing.Dict[builtins.str, typing.Any]]] = None,
        pkg: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg", typing.Dict[builtins.str, typing.Any]]] = None,
        repository: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Required. The id of the resource with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the OS policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#exec OsConfigV2PolicyOrchestratorForOrganization#exec}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#file OsConfigV2PolicyOrchestratorForOrganization#file}
        :param pkg: pkg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#pkg OsConfigV2PolicyOrchestratorForOrganization#pkg}
        :param repository: repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#repository OsConfigV2PolicyOrchestratorForOrganization#repository}
        '''
        if isinstance(exec, dict):
            exec = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec(**exec)
        if isinstance(file, dict):
            file = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile(**file)
        if isinstance(pkg, dict):
            pkg = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg(**pkg)
        if isinstance(repository, dict):
            repository = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository(**repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e350c71b07ac91dc57c59ab8ae3ef5abc2048e6e3e4e1d6a5e9cb17fb4ac05)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exec(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec"]:
        '''exec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#exec OsConfigV2PolicyOrchestratorForOrganization#exec}
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec"], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#file OsConfigV2PolicyOrchestratorForOrganization#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile"], result)

    @builtins.property
    def pkg(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"]:
        '''pkg block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#pkg OsConfigV2PolicyOrchestratorForOrganization#pkg}
        '''
        result = self._values.get("pkg")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"], result)

    @builtins.property
    def repository(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"]:
        '''repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#repository OsConfigV2PolicyOrchestratorForOrganization#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec",
    jsii_struct_bases=[],
    name_mapping={"validate": "validate", "enforce": "enforce"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec:
    def __init__(
        self,
        *,
        validate: typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate", typing.Dict[builtins.str, typing.Any]],
        enforce: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param validate: validate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#validate OsConfigV2PolicyOrchestratorForOrganization#validate}
        :param enforce: enforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#enforce OsConfigV2PolicyOrchestratorForOrganization#enforce}
        '''
        if isinstance(validate, dict):
            validate = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate(**validate)
        if isinstance(enforce, dict):
            enforce = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce(**enforce)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fcf755620de9492e0a8dca376b0d0494579e65eeaeff36a83d5a47dd7ed5ef8)
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
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate":
        '''validate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#validate OsConfigV2PolicyOrchestratorForOrganization#validate}
        '''
        result = self._values.get("validate")
        assert result is not None, "Required property 'validate' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate", result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce"]:
        '''enforce block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#enforce OsConfigV2PolicyOrchestratorForOrganization#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce",
    jsii_struct_bases=[],
    name_mapping={
        "interpreter": "interpreter",
        "args": "args",
        "file": "file",
        "output_file_path": "outputFilePath",
        "script": "script",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce:
    def __init__(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: Required. The script interpreter to use. Possible values: INTERPRETER_UNSPECIFIED NONE SHELL POWERSHELL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#interpreter OsConfigV2PolicyOrchestratorForOrganization#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#args OsConfigV2PolicyOrchestratorForOrganization#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#file OsConfigV2PolicyOrchestratorForOrganization#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#output_file_path OsConfigV2PolicyOrchestratorForOrganization#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#script OsConfigV2PolicyOrchestratorForOrganization#script}
        '''
        if isinstance(file, dict):
            file = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__162ffd9661a0d143377e577204168ad080a1c21bd50d82772fe3ae11c9abb81c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#interpreter OsConfigV2PolicyOrchestratorForOrganization#interpreter}
        '''
        result = self._values.get("interpreter")
        assert result is not None, "Required property 'interpreter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional arguments to pass to the source during execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#args OsConfigV2PolicyOrchestratorForOrganization#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#file OsConfigV2PolicyOrchestratorForOrganization#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile"], result)

    @builtins.property
    def output_file_path(self) -> typing.Optional[builtins.str]:
        '''Only recorded for enforce Exec.

        Path to an output file (that is created by this Exec) whose
        content will be recorded in OSPolicyResourceCompliance after a
        successful run. Absence or failure to read this file will result in
        this ExecResource being non-compliant. Output file size is limited to
        500K bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#output_file_path OsConfigV2PolicyOrchestratorForOrganization#output_file_path}
        '''
        result = self._values.get("output_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''An inline script. The size of the script is limited to 32KiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#script OsConfigV2PolicyOrchestratorForOrganization#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac7415b4cced7175da978d6ec3b05d7a38d27c093f3b92348657be322918d3ec)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2311ab998a9248c4651f378cf1fcbfce8df9de971c192a14c075fb4c259f698)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Required. Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3429b17ca07b1ae6f702732bc16040fcc405000dfd9c623e918fff4567b93a6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4db00c36939112adc80c3cb0e0a75b1fe3d4667f7341636339e29b85e1dfebe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d34bb084dd5a2b55b1062599bfcda75528e7c0625acd8f156f4f5ffd1ade0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5166eb8481f18814545e400bdb46aa4a0657e8130c0fbf52b1a26602851d0341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb731f1611501cb75ae011b439d885aa025b4ab02fec09b62481cd7627c15c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f36861fe4748713aa281c737a87471764812608e5450b42b7a4a865efe22249)
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
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(
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
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ddda31674a3e9aef7f07239fe8117c75a25773e37565b77a0dbb98161236c317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1cb2c81ede405dfd2aabfb5e2d4c9888b45142f367ee5d9e6671a628b11252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d1572ca26d1a9af930e5bb8a251e9904aa5703864d0d6e5c5c2d6e14039dcc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627ed0dc2a9611ba6d44e1a48f2ff7778e3ab115021001e3f80280f598ffa48a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6d8c14b7b20201fb4f503e25b9283a06744905a58f1f782fb7f2e9b4fe43f6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4799e3a62bc455f1430e06141af624ef653631733ce3b0718f0514da07c0a983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8734062f22feb391b9ad0835c1ca05e338c39ea1782875527f1f7bc6f986f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d965abf9235807402f4e54cf79b8cb163c70f4ec5e607aa2409de0fe99ec884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dadf28f314d6b7c97b6dbc920cd9ceb78de0be64d6ff7a024b49da5a58ca126)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile], jsii.get(self, "fileInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3f66a4c53364f0179a8b587923b57d125476f24d693a37975e92e3e0084e6c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18477a6158b79197fd057dd92b6000548f034e61f3b0aa5f0d77314f16fc28b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFilePath")
    def output_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFilePath"))

    @output_file_path.setter
    def output_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e15856f77a9db9f53f46df5bbe02191024faa4637815401b837dab558ee7fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27819e7fcab0e9c2bf3374544b3d15f5e8e4162b3e24a28f285767edccc84c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a70eab086943c52a395df24edd7936061c7a61ee1bbc26e73fb33130d5f419)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66dd4d0b28692f2c81901f2e201d03585eeed074c54580a982456cf3d33530b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnforce")
    def put_enforce(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile, typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: Required. The script interpreter to use. Possible values: INTERPRETER_UNSPECIFIED NONE SHELL POWERSHELL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#interpreter OsConfigV2PolicyOrchestratorForOrganization#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#args OsConfigV2PolicyOrchestratorForOrganization#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#file OsConfigV2PolicyOrchestratorForOrganization#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#output_file_path OsConfigV2PolicyOrchestratorForOrganization#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#script OsConfigV2PolicyOrchestratorForOrganization#script}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce(
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
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: Required. The script interpreter to use. Possible values: INTERPRETER_UNSPECIFIED NONE SHELL POWERSHELL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#interpreter OsConfigV2PolicyOrchestratorForOrganization#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#args OsConfigV2PolicyOrchestratorForOrganization#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#file OsConfigV2PolicyOrchestratorForOrganization#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#output_file_path OsConfigV2PolicyOrchestratorForOrganization#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#script OsConfigV2PolicyOrchestratorForOrganization#script}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference, jsii.get(self, "enforce"))

    @builtins.property
    @jsii.member(jsii_name="validate")
    def validate(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference", jsii.get(self, "validate"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="validateInput")
    def validate_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate"], jsii.get(self, "validateInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2bfe2dc2ed33072df48e92f23482fd8b89ac6590a3212c0501f3df501b9a1a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate",
    jsii_struct_bases=[],
    name_mapping={
        "interpreter": "interpreter",
        "args": "args",
        "file": "file",
        "output_file_path": "outputFilePath",
        "script": "script",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate:
    def __init__(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: Required. The script interpreter to use. Possible values: INTERPRETER_UNSPECIFIED NONE SHELL POWERSHELL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#interpreter OsConfigV2PolicyOrchestratorForOrganization#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#args OsConfigV2PolicyOrchestratorForOrganization#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#file OsConfigV2PolicyOrchestratorForOrganization#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#output_file_path OsConfigV2PolicyOrchestratorForOrganization#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#script OsConfigV2PolicyOrchestratorForOrganization#script}
        '''
        if isinstance(file, dict):
            file = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3795aa607c7590d8d5a19a0ea93fa32c3addce07c9b516a3f173ac579adab9f7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#interpreter OsConfigV2PolicyOrchestratorForOrganization#interpreter}
        '''
        result = self._values.get("interpreter")
        assert result is not None, "Required property 'interpreter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional arguments to pass to the source during execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#args OsConfigV2PolicyOrchestratorForOrganization#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#file OsConfigV2PolicyOrchestratorForOrganization#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile"], result)

    @builtins.property
    def output_file_path(self) -> typing.Optional[builtins.str]:
        '''Only recorded for enforce Exec.

        Path to an output file (that is created by this Exec) whose
        content will be recorded in OSPolicyResourceCompliance after a
        successful run. Absence or failure to read this file will result in
        this ExecResource being non-compliant. Output file size is limited to
        500K bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#output_file_path OsConfigV2PolicyOrchestratorForOrganization#output_file_path}
        '''
        result = self._values.get("output_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''An inline script. The size of the script is limited to 32KiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#script OsConfigV2PolicyOrchestratorForOrganization#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93fd0995fcd0e4db2c3544430b133a4ba0f18bf665f624b1b0281bc1279982f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f692643460553138ec66b40dc38bcc7061ad2a059123ebe927b003c3eff2db1e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Required. Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__787a0c0499a24d827455028db4943a5b86fffa29248fad2ba38986451ab02534)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9017eb38fd391c624976c971f2b3e8060ca3b64ea1ab388dd91f015c9d4d9c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e683ed32703870055ec68a2cf6a01674df8422f19f62dd821b765f3ce52fbef1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf0278bd30d8ed379393129ee5c2108d3d06f45dfaff24075bc8198e70d0eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861939b1622ce8b2cf53ed17526553ec626b11704e0a6c275293076c33fb59b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ecbb061552d9c1b448f334d6ae00e6e3223516794f54d0c1a6886ecab4acab3)
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
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs(
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
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6455a49ddcdea6c94264f87d69b71e31b3564cc0b0ebc75dd0dda54a8b0b9da8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f0a10c801a6529c3ec2f291598f3e47263c76f09624a117bd5f64476821655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652178ef9cf712032dedec10f5cc3ee8c14182bb83c519e33600e7ea7d6c8b12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f7ad623848ca9e9334a4c5334776f8321468750348016fa93a3ee91f3bada6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5dc6a6da7d99297a6ac52a64549d3214ec2c5fcc8ec3d72db562cba900b2dad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d0da44cdbaec90767935b78ba9565256a9fe9b3d07f7a661d6347dd5bdc56d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5195905de34ca58448cef2ac7ba6cab9c62275d9b71ba9901feb796e270f3ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a253d4372d471aeb7a8129d151977e456890d13358475b7b62f3d617828243a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efa78e91d277b90f260247a04695a619c34f4a2792063dbbdb5583b41d8d11fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile], jsii.get(self, "fileInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e430f1cc5da77c9de55d7666fc89aa6930b99c54169cc0c98f4a2912dc1fea05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3bd62fe1ed9f069509e093fc15fe5b67b38ccf485ee11f2ee206dbfb408728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFilePath")
    def output_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFilePath"))

    @output_file_path.setter
    def output_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3436df6437c640a45832f6033d6dae2caf636d6bcea067f28884033dbd91b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2c11f470588455767fd13316571747dba3589295f36ebdb5b1ee0b3a866d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6298cd722ee15110efd138cb9148d72746be0dc53ad906e374b382769fe57151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "state": "state",
        "content": "content",
        "file": "file",
        "permissions": "permissions",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile:
    def __init__(
        self,
        *,
        path: builtins.str,
        state: builtins.str,
        content: typing.Optional[builtins.str] = None,
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile", typing.Dict[builtins.str, typing.Any]]] = None,
        permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: Required. The absolute path of the file within the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#path OsConfigV2PolicyOrchestratorForOrganization#path}
        :param state: Required. Desired state of the file. Possible values: DESIRED_STATE_UNSPECIFIED PRESENT ABSENT CONTENTS_MATCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#state OsConfigV2PolicyOrchestratorForOrganization#state}
        :param content: A a file with this content. The size of the content is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#content OsConfigV2PolicyOrchestratorForOrganization#content}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#file OsConfigV2PolicyOrchestratorForOrganization#file}
        :param permissions: Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility). Each digit represents a three bit number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one bit corresponds to the execute permission. Default behavior is 755. Below are some examples of permissions and their associated values: read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#permissions OsConfigV2PolicyOrchestratorForOrganization#permissions}
        '''
        if isinstance(file, dict):
            file = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e7ed8745b0e076f84e788989632a23dc3e17e3779d82b0c230030dbfc85954)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#path OsConfigV2PolicyOrchestratorForOrganization#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''Required. Desired state of the file. Possible values: DESIRED_STATE_UNSPECIFIED PRESENT ABSENT CONTENTS_MATCH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#state OsConfigV2PolicyOrchestratorForOrganization#state}
        '''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''A a file with this content. The size of the content is limited to 32KiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#content OsConfigV2PolicyOrchestratorForOrganization#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#file OsConfigV2PolicyOrchestratorForOrganization#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#permissions OsConfigV2PolicyOrchestratorForOrganization#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f77eb0cab8ff709f2fa5af9d839330ce5dc66224d20f863fae368dbea5e037ea)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97b97c13de76e054d3e6fc6bbf0667af46ebbffbd6c5dca05473f5068f2adfc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Required. Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__728c565db7223b13033d0fb2863886dbb3b273c1d458607bc5268b15c866b695)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b3b43a422730bc7e18480204bd7bcfeb8103a2af6b7ee9c43324f3996988aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e69a9ef8d9fef1644682d2d531b1dbe92b01c5bc805911bccff11b8b6b5921d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73f52ded4e389886c537ba0d0b63aa11590627762973a5ca3caaa39d0f996b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdef27b3f24d743a1cabb470a0d671cb96f169475306655f1c349db096f71ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bec981037305249a97fb733cd3af936c9c43e7cde3b3032d12d899ac0975377)
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
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs(
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
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__35fc9b864e149d4a30dc54b91169eaf64eea01116bfbc1f2a9cec5beba76e131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdb92332bb01106f1a55a7b10e7221af7f122fb80ee2572fc394258c6561c637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1baaa16944f38c009b23ca5532c7ba9d2789ce7f012d7f6dcc6db2176dd79b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caacc2bd56c27b3179415d11e4d2d2873bf5288c109cf1e34e4e2ce916a4691b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bb5a7304dfdc3177b707331dac13ffb56b00d5b8a0f49475be65d1a99c44701)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8352a579550f8fcff80d70244a899f98cfdbc986deb99fd87fb9dacefac6875a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b27017ca6de4b822a5855305a18135f378bfa8f25ae1a45a5b4f36e9bba281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b29f579886eee694c39b97a3af957d74186913d1812d7ef7b2fed35956e3b177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0243a022d166571aeb511687413c1a5f22a70813c1b362aa88f79e6d75b11ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile], jsii.get(self, "fileInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__50948df5d6dcca4338f01236cedaf7b86eb4c0f239441fd3c4cf4fb50543f084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a35981339f4973f98fd267da33e38ee564e46871fabd855da044c70fd7f20e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6040163821e9882d827e6928e87307e30c042874437fc84fe2d1355b4850a6e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999b8853960351c80036e8a66d07033e5123a5a77d6213ca48048e974973ac45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe778fe70644bea5a3cef18bfdb6a5f5c23127328d25374a8715dc330d1f6c27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0540593a59cb3aabd5206bcc066204d5f1f246a5120856bb693230d6ed767a9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5929750940ce043c3bcca7f6660c52d95045e93a9decd7886329f20b6659768c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb4af5ce400a9563dc053afb2dc878bd3c11b454f766812898978ce63c9e0c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19cb57e049b8c4aadb16c67e4e213136a536006016bc1cb51c7f889327d23b0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc0412061acca854649e77c9d89fb96dbab4c4fbe105d8d85d294aa45cef8bc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e1e974431137f45d9aecee19e6586ea7bbe5c801548dea2c526680c249a0da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4be1b2f145b043b62e866c1145b178be1b7a6b0effb95a4bd6d7491d035435e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExec")
    def put_exec(
        self,
        *,
        validate: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate, typing.Dict[builtins.str, typing.Any]],
        enforce: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param validate: validate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#validate OsConfigV2PolicyOrchestratorForOrganization#validate}
        :param enforce: enforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#enforce OsConfigV2PolicyOrchestratorForOrganization#enforce}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec(
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
        file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile, typing.Dict[builtins.str, typing.Any]]] = None,
        permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: Required. The absolute path of the file within the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#path OsConfigV2PolicyOrchestratorForOrganization#path}
        :param state: Required. Desired state of the file. Possible values: DESIRED_STATE_UNSPECIFIED PRESENT ABSENT CONTENTS_MATCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#state OsConfigV2PolicyOrchestratorForOrganization#state}
        :param content: A a file with this content. The size of the content is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#content OsConfigV2PolicyOrchestratorForOrganization#content}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#file OsConfigV2PolicyOrchestratorForOrganization#file}
        :param permissions: Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility). Each digit represents a three bit number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one bit corresponds to the execute permission. Default behavior is 755. Below are some examples of permissions and their associated values: read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#permissions OsConfigV2PolicyOrchestratorForOrganization#permissions}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile(
            path=path, state=state, content=content, file=file, permissions=permissions
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="putPkg")
    def put_pkg(
        self,
        *,
        desired_state: builtins.str,
        apt: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt", typing.Dict[builtins.str, typing.Any]]] = None,
        deb: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb", typing.Dict[builtins.str, typing.Any]]] = None,
        googet: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget", typing.Dict[builtins.str, typing.Any]]] = None,
        msi: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi", typing.Dict[builtins.str, typing.Any]]] = None,
        rpm: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param desired_state: Required. The desired state the agent should maintain for this package. Possible values: DESIRED_STATE_UNSPECIFIED INSTALLED REMOVED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#desired_state OsConfigV2PolicyOrchestratorForOrganization#desired_state}
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#apt OsConfigV2PolicyOrchestratorForOrganization#apt}
        :param deb: deb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#deb OsConfigV2PolicyOrchestratorForOrganization#deb}
        :param googet: googet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#googet OsConfigV2PolicyOrchestratorForOrganization#googet}
        :param msi: msi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#msi OsConfigV2PolicyOrchestratorForOrganization#msi}
        :param rpm: rpm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#rpm OsConfigV2PolicyOrchestratorForOrganization#rpm}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#yum OsConfigV2PolicyOrchestratorForOrganization#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#zypper OsConfigV2PolicyOrchestratorForOrganization#zypper}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg(
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
        apt: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#apt OsConfigV2PolicyOrchestratorForOrganization#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#goo OsConfigV2PolicyOrchestratorForOrganization#goo}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#yum OsConfigV2PolicyOrchestratorForOrganization#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#zypper OsConfigV2PolicyOrchestratorForOrganization#zypper}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference, jsii.get(self, "exec"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="pkg")
    def pkg(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference", jsii.get(self, "pkg"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference", jsii.get(self, "repository"))

    @builtins.property
    @jsii.member(jsii_name="execInput")
    def exec_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec], jsii.get(self, "execInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="pkgInput")
    def pkg_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"], jsii.get(self, "pkgInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2b3f4130f095801c399f6e7ccef90ec23386bfd8827c7cd860fbacb4f60cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2303b5910208d7787ac2c2daa415954ba32eda9270482c6f092bb0079a59ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg",
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
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg:
    def __init__(
        self,
        *,
        desired_state: builtins.str,
        apt: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt", typing.Dict[builtins.str, typing.Any]]] = None,
        deb: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb", typing.Dict[builtins.str, typing.Any]]] = None,
        googet: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget", typing.Dict[builtins.str, typing.Any]]] = None,
        msi: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi", typing.Dict[builtins.str, typing.Any]]] = None,
        rpm: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param desired_state: Required. The desired state the agent should maintain for this package. Possible values: DESIRED_STATE_UNSPECIFIED INSTALLED REMOVED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#desired_state OsConfigV2PolicyOrchestratorForOrganization#desired_state}
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#apt OsConfigV2PolicyOrchestratorForOrganization#apt}
        :param deb: deb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#deb OsConfigV2PolicyOrchestratorForOrganization#deb}
        :param googet: googet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#googet OsConfigV2PolicyOrchestratorForOrganization#googet}
        :param msi: msi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#msi OsConfigV2PolicyOrchestratorForOrganization#msi}
        :param rpm: rpm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#rpm OsConfigV2PolicyOrchestratorForOrganization#rpm}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#yum OsConfigV2PolicyOrchestratorForOrganization#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#zypper OsConfigV2PolicyOrchestratorForOrganization#zypper}
        '''
        if isinstance(apt, dict):
            apt = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt(**apt)
        if isinstance(deb, dict):
            deb = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb(**deb)
        if isinstance(googet, dict):
            googet = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget(**googet)
        if isinstance(msi, dict):
            msi = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi(**msi)
        if isinstance(rpm, dict):
            rpm = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm(**rpm)
        if isinstance(yum, dict):
            yum = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum(**yum)
        if isinstance(zypper, dict):
            zypper = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper(**zypper)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3467a668f94ac3c802aadc91e8b4145057081f3ed077a5fdf1c31e309943b37a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#desired_state OsConfigV2PolicyOrchestratorForOrganization#desired_state}
        '''
        result = self._values.get("desired_state")
        assert result is not None, "Required property 'desired_state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def apt(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt"]:
        '''apt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#apt OsConfigV2PolicyOrchestratorForOrganization#apt}
        '''
        result = self._values.get("apt")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt"], result)

    @builtins.property
    def deb(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb"]:
        '''deb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#deb OsConfigV2PolicyOrchestratorForOrganization#deb}
        '''
        result = self._values.get("deb")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb"], result)

    @builtins.property
    def googet(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget"]:
        '''googet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#googet OsConfigV2PolicyOrchestratorForOrganization#googet}
        '''
        result = self._values.get("googet")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget"], result)

    @builtins.property
    def msi(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi"]:
        '''msi block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#msi OsConfigV2PolicyOrchestratorForOrganization#msi}
        '''
        result = self._values.get("msi")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi"], result)

    @builtins.property
    def rpm(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"]:
        '''rpm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#rpm OsConfigV2PolicyOrchestratorForOrganization#rpm}
        '''
        result = self._values.get("rpm")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"], result)

    @builtins.property
    def yum(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"]:
        '''yum block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#yum OsConfigV2PolicyOrchestratorForOrganization#yum}
        '''
        result = self._values.get("yum")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"], result)

    @builtins.property
    def zypper(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"]:
        '''zypper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#zypper OsConfigV2PolicyOrchestratorForOrganization#zypper}
        '''
        result = self._values.get("zypper")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19fa0e39c3c66f3c6a0c55391ec114922be0598848c6c1edeb1794fbad2f3f4d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Required. Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__331f57f854ddd4bb5f455c8c0cc57ecbadb8445696fcb9049e5c23b30e53c172)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab8c59315ed2d71edb753d030a17ad7f0dee1104ef3bfc84efa588ab810752c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095017f29bb15df89c754043a5857f680ae9f34bacc22ee004d811ce201f76c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "pull_deps": "pullDeps"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb:
    def __init__(
        self,
        *,
        source: typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#source OsConfigV2PolicyOrchestratorForOrganization#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'dpkg -i package' - install when true: 'apt-get update && apt-get -y install package.deb' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#pull_deps OsConfigV2PolicyOrchestratorForOrganization#pull_deps}
        '''
        if isinstance(source, dict):
            source = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51245c6ea358db3a62f170ae8987898d793ea02af79d5cf840149cdb4344fc1a)
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
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#source OsConfigV2PolicyOrchestratorForOrganization#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource", result)

    @builtins.property
    def pull_deps(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether dependencies should also be installed.

        - install when false: 'dpkg -i package'
        - install when true: 'apt-get update && apt-get -y install
          package.deb'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#pull_deps OsConfigV2PolicyOrchestratorForOrganization#pull_deps}
        '''
        result = self._values.get("pull_deps")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__696461ad069564f3310bedbc28eacc82f7d696f759dcb3309b889837a20ae0c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource(
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
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference", jsii.get(self, "source"))

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
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource"], jsii.get(self, "sourceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8c01343c77f38fab27ab934f178f926894c85088b86c2f1e6e38d00bb502b1c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullDeps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ac8c2ff417b09627432fb190a7ef5a2dcd9e314a3e073e691ecb5cc71edeb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42fe650fabe4a4829151a9098b31591c229162eeede2fd275afff04129078e3f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10d83f3b5511ae15a6512e719cf1a5ea09b42d7cad769cfa754c8aa871451de0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Required. Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf667582db3a22d1216bf792eda95ea324c6abd1e57dbf4ae16c4d987ea1fb08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__264a5c2e29179b24d8cb6d79fd57ea1ed1d1f7bf6012a0620601ade68abc8b94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6223dec4599ac85930c143ab928331be546c403584abdecca72c63424607837d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0478113683b33fff60cdc2f964a7127bb93c32a1a6d24dd3e2e4aea29de0e418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c582eab541a5fce425f3fb7ec41b23e6315ee89809711ec865740430a6e6ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c231d6f34c69d00c2e1ef2c82122012cc9390d847771f39299cddf434a4ee34c)
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
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(
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
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__447f89c768afba640844b65bcfca4626560e9909eb9bf4fde873dca554571dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e878369c1b4b7b9a86c4161da7e63af3eeb5b6b82b882a632d34aeed73fe53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fe5f1478b7393fb67307a86a9c8bb4b98a8d51e98093fd35f3a8c9b8f7e65f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865b297a2bfe7f6ac8391bcb311e50c86bf1372f1c7ac84d36d029d5391872fa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5918ebebda77aedda136fa95dfa1db3ae0a0299a0c93e45783843ae67ce42f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eef4004338264bd91879fd911607a6122904e1c2c53643f2c9e8cd72769b45b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e371d9fc241508f9fb365a283a6f441f01ee33eb4fa923d28f916bab38d72620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056bf3f2ce12072c0a281decccfc63ba68d8e0ddf82aeda8db94d8a7c5414fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ccc3ddaa7a65657f2ccc317fbd762e86ef1ae3994e18d13d6e44a30fb64e17e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Required. Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d5d5ba557f95928b761ae6edbf7e011e44ba823001020b2f6a212284dd07d81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98764a81f33f370df519173d2acde1bd6a607349060f5ad052ab7274d007d15d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb4f3b9b5b30c9f9217fb6033e059de147ea73d41175fc47efe5f128442483c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "properties": "properties"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi:
    def __init__(
        self,
        *,
        source: typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource", typing.Dict[builtins.str, typing.Any]],
        properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#source OsConfigV2PolicyOrchestratorForOrganization#source}
        :param properties: Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#properties OsConfigV2PolicyOrchestratorForOrganization#properties}
        '''
        if isinstance(source, dict):
            source = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b990880e0292f5df7fb9870bf0dc49307f6e418e3f3b706bc173232f3049bd)
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
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#source OsConfigV2PolicyOrchestratorForOrganization#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource", result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#properties OsConfigV2PolicyOrchestratorForOrganization#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54060760f305cfb4b1473635ad74a03df05c5256362e54b5da50a8e7124207d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource(
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
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2832f0d1f56142e1c03cb06154f0706cb58216c47b969b31e183c3d841c7036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c2a7522ddd5ad738bebe0e0a574257ccdc93122964ff8974413404ceed73ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9853023bbede6f01d45a4b7198a2737bfd4de47523a14fa9a3753a2332b4ae12)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9695a59f5a4265247e9301f0fdc85c9d8c1bb36b439632712cdf501a72500cb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Required. Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9200a50b5d8c30a039c423671645dc1c9369601c47a3ba49e0dbd392f7014d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__196ab7423d1d48eb625013ad0a6ab1ad5ee4d5b986b8995c993540e0e4cefd45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8d3888a1e9da3bde5c8c04104aa4f42940b164afe246ccbbe6af7654d2b157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76eb04ac7730e29c4615c6a104d0761c42fa5f187e8cadb91a8fc5d24a48a15e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e0b044fb8d172a0aafaf1196e3ee467a2c1ae3462f0d4e14607d3b6dd28df74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50f4b733aa48b245e30749b2408d3587ee1562748c040d48c86991757e7a8339)
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
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(
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
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__459df3755d5ef75af29cf00ca96cd42483e1aa86688869abb4db71cd0dc2ad0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__277d254563764aafb43ed59ed6615343be35a8f6e893d2b0c1d51e6ca6787129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f941e940126318b48ad64ada41407d9f4519a95ff8654c10edd315d6e56dd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9101e8146887972807f3f09dd5c07aeb58245c77d54128f8ecc37eedc41f9394)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73f5bd5814327a70dd1260269843006b99315fa9330018e4c3cdc573b4ecd57c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b3e0dedd7031cacc1b7be74c1cca95701959d11033822e61fd802cfaeab1fce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__644a8e346ec3b32641fd2a3566308f41203da4bb6be582e1c0425fcd1bfb28f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09cf91a9a308f34c299778772e3705bbc7ea13f585e3bf24c2186688a8b58622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc3875752f6e0eeed9700ffbb2db0a46c246fe4ae6badbd9cfd9feeb7865d317)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApt")
    def put_apt(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putApt", [value]))

    @jsii.member(jsii_name="putDeb")
    def put_deb(
        self,
        *,
        source: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource, typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#source OsConfigV2PolicyOrchestratorForOrganization#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'dpkg -i package' - install when true: 'apt-get update && apt-get -y install package.deb' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#pull_deps OsConfigV2PolicyOrchestratorForOrganization#pull_deps}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb(
            source=source, pull_deps=pull_deps
        )

        return typing.cast(None, jsii.invoke(self, "putDeb", [value]))

    @jsii.member(jsii_name="putGooget")
    def put_googet(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putGooget", [value]))

    @jsii.member(jsii_name="putMsi")
    def put_msi(
        self,
        *,
        source: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource, typing.Dict[builtins.str, typing.Any]],
        properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#source OsConfigV2PolicyOrchestratorForOrganization#source}
        :param properties: Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#properties OsConfigV2PolicyOrchestratorForOrganization#properties}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi(
            source=source, properties=properties
        )

        return typing.cast(None, jsii.invoke(self, "putMsi", [value]))

    @jsii.member(jsii_name="putRpm")
    def put_rpm(
        self,
        *,
        source: typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#source OsConfigV2PolicyOrchestratorForOrganization#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'rpm --upgrade --replacepkgs package.rpm' - install when true: 'yum -y install package.rpm' or 'zypper -y install package.rpm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#pull_deps OsConfigV2PolicyOrchestratorForOrganization#pull_deps}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm(
            source=source, pull_deps=pull_deps
        )

        return typing.cast(None, jsii.invoke(self, "putRpm", [value]))

    @jsii.member(jsii_name="putYum")
    def put_yum(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putYum", [value]))

    @jsii.member(jsii_name="putZypper")
    def put_zypper(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference, jsii.get(self, "apt"))

    @builtins.property
    @jsii.member(jsii_name="deb")
    def deb(
        self,
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference, jsii.get(self, "deb"))

    @builtins.property
    @jsii.member(jsii_name="googet")
    def googet(
        self,
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference, jsii.get(self, "googet"))

    @builtins.property
    @jsii.member(jsii_name="msi")
    def msi(
        self,
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference, jsii.get(self, "msi"))

    @builtins.property
    @jsii.member(jsii_name="rpm")
    def rpm(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference", jsii.get(self, "rpm"))

    @builtins.property
    @jsii.member(jsii_name="yum")
    def yum(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference", jsii.get(self, "yum"))

    @builtins.property
    @jsii.member(jsii_name="zypper")
    def zypper(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference", jsii.get(self, "zypper"))

    @builtins.property
    @jsii.member(jsii_name="aptInput")
    def apt_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt], jsii.get(self, "aptInput"))

    @builtins.property
    @jsii.member(jsii_name="debInput")
    def deb_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb], jsii.get(self, "debInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="googetInput")
    def googet_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget], jsii.get(self, "googetInput"))

    @builtins.property
    @jsii.member(jsii_name="msiInput")
    def msi_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi], jsii.get(self, "msiInput"))

    @builtins.property
    @jsii.member(jsii_name="rpmInput")
    def rpm_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"], jsii.get(self, "rpmInput"))

    @builtins.property
    @jsii.member(jsii_name="yumInput")
    def yum_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"], jsii.get(self, "yumInput"))

    @builtins.property
    @jsii.member(jsii_name="zypperInput")
    def zypper_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"], jsii.get(self, "zypperInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab044a9a41106ec5906a892cd10e78266e40171814be7718051887057d50c728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d041b4f0f8ff85edab7d531d2f5bf08e20b611c8e2dd7fc4a938556b848c1fba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "pull_deps": "pullDeps"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm:
    def __init__(
        self,
        *,
        source: typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#source OsConfigV2PolicyOrchestratorForOrganization#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'rpm --upgrade --replacepkgs package.rpm' - install when true: 'yum -y install package.rpm' or 'zypper -y install package.rpm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#pull_deps OsConfigV2PolicyOrchestratorForOrganization#pull_deps}
        '''
        if isinstance(source, dict):
            source = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17350bbf58a1e593a53259318c53ff3f7ac7c1b7d33e3d8cfab8d0d219f0a0ac)
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
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#source OsConfigV2PolicyOrchestratorForOrganization#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource", result)

    @builtins.property
    def pull_deps(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether dependencies should also be installed.

        - install when false: 'rpm --upgrade --replacepkgs package.rpm'
        - install when true: 'yum -y install package.rpm' or
          'zypper -y install package.rpm'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#pull_deps OsConfigV2PolicyOrchestratorForOrganization#pull_deps}
        '''
        result = self._values.get("pull_deps")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ebd415ebf5eecbedc10da7370e3aae68ad7d1d0b21c634332289a564631e038)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource(
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
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference", jsii.get(self, "source"))

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
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource"], jsii.get(self, "sourceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__dc41de812fd3eedb4d5970b908100abe9968e653ab9f1c3b5befd52ce2e9967e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullDeps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0851bcb140ef17f2a09a7040a06aa3032bce6dfcac01dbc1b84825108c9a2610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7673e2961b10a933142e202b5e26df968252e3246377f85ba61ed94f9c67def8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#allow_insecure OsConfigV2PolicyOrchestratorForOrganization#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gcs OsConfigV2PolicyOrchestratorForOrganization#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#local_path OsConfigV2PolicyOrchestratorForOrganization#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#remote OsConfigV2PolicyOrchestratorForOrganization#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b33e3610503f6dfe89f8adbf8170fe34ea208f0e02c51eaf709cd2635febd7a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Required. Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6925dfc550461a73937a018e8178cf73ff43dff31c32cc3c1d26489cd0af8f93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa44db912607e8180c831031091855eace590d49f8601e51cd04a0701ef3c9a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd274bddf82ce54393472b75cbfc0be3a93340bd657da99ff851b4d8a1494b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688e185435ee2a5308f0eb9c11eb79fbe126da574634a128f3af3bf1231a9a91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62393ae93b81cf7a95f160a912f2cb17e88ade8cf9958a1018eb7a8c97076f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d25ee5194c3151b55fd804b1f74418c8dd930f15b68bb1b1e1f4c4674bd4da5)
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
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#bucket OsConfigV2PolicyOrchestratorForOrganization#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#object OsConfigV2PolicyOrchestratorForOrganization#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#generation OsConfigV2PolicyOrchestratorForOrganization#generation}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(
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
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4e8cfdb3a36a3e13f46dc0879d53f4a260f830456d2c5a7c4218beb8f37dcf3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390ac98ebbbadac5e678b432aaf32229f58c4e486d1b08930db5a497282a2e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd68a35f1ed2fea3db659e3ab770c847f662880c43b9bf29f0aef26e712939a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5e71effd2f19a8d50b14e330c8af2a4060ab752c3a810eb7e85ea10341f6a8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#sha256_checksum OsConfigV2PolicyOrchestratorForOrganization#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb4664658e8ddc2b9c7be2f2bec6f9b80132ee44549771d28d5fb6cc5d4c32b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd82a79f07eed30c403510010ca2c79459633fbd71c10e1afef35924e7bb0de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04b701d3479433a750049ad107ed1bd9368e8574fbbe99eff1efd835335b2c8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c91142acf715a20129d73e70d7d5c59209801bcf7dd55046d961fa9e3f12f324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c33c71fdc81b5562d2659ea58ad9cf8312b73353b204026480597c1e20915b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Required. Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5ac11299752e9cdd1314a2eba1db7eb00bff3251cf948dcb4dc4bdb76ebc644)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30e803d56459af6e0c11378dcd7e771d91cd11869d3b4d3b9893ed3bbf247352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae3ebc3882c63c9d9867a7c2b4146de65e8e01516a9782600ee5949ba4a9f6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d533bb1504dfb14e998e26b8e0e690c2b5e70fe45953b597a893f6f93538d76c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Required. Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81c7f7e30d18a46a52ef4280704e8715b431449d63cfc45746ccefdfc9994f89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c52a9d672a90f3c5e570411ccf726b587746e968d034f891fb515c5558f9afcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d5dbd361a7d6fa238a27f63ab4d434b6b0f04fb47016ebddd8c132ef43bcbf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository",
    jsii_struct_bases=[],
    name_mapping={"apt": "apt", "goo": "goo", "yum": "yum", "zypper": "zypper"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository:
    def __init__(
        self,
        *,
        apt: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#apt OsConfigV2PolicyOrchestratorForOrganization#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#goo OsConfigV2PolicyOrchestratorForOrganization#goo}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#yum OsConfigV2PolicyOrchestratorForOrganization#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#zypper OsConfigV2PolicyOrchestratorForOrganization#zypper}
        '''
        if isinstance(apt, dict):
            apt = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt(**apt)
        if isinstance(goo, dict):
            goo = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo(**goo)
        if isinstance(yum, dict):
            yum = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum(**yum)
        if isinstance(zypper, dict):
            zypper = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper(**zypper)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b4b5e3e8470f94a4c568d51da2ca9fdca032fd32bf3d452bb2525cd5abc0e5)
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
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt"]:
        '''apt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#apt OsConfigV2PolicyOrchestratorForOrganization#apt}
        '''
        result = self._values.get("apt")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt"], result)

    @builtins.property
    def goo(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo"]:
        '''goo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#goo OsConfigV2PolicyOrchestratorForOrganization#goo}
        '''
        result = self._values.get("goo")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo"], result)

    @builtins.property
    def yum(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"]:
        '''yum block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#yum OsConfigV2PolicyOrchestratorForOrganization#yum}
        '''
        result = self._values.get("yum")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"], result)

    @builtins.property
    def zypper(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"]:
        '''zypper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#zypper OsConfigV2PolicyOrchestratorForOrganization#zypper}
        '''
        result = self._values.get("zypper")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt",
    jsii_struct_bases=[],
    name_mapping={
        "archive_type": "archiveType",
        "components": "components",
        "distribution": "distribution",
        "uri": "uri",
        "gpg_key": "gpgKey",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt:
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
        :param archive_type: Required. Type of archive files in this repository. Possible values: ARCHIVE_TYPE_UNSPECIFIED DEB DEB_SRC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#archive_type OsConfigV2PolicyOrchestratorForOrganization#archive_type}
        :param components: Required. List of components for this repository. Must contain at least one item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#components OsConfigV2PolicyOrchestratorForOrganization#components}
        :param distribution: Required. Distribution of this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#distribution OsConfigV2PolicyOrchestratorForOrganization#distribution}
        :param uri: Required. URI for this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param gpg_key: URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gpg_key OsConfigV2PolicyOrchestratorForOrganization#gpg_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d627d29fbd4ac3fe89499d3a76c353e1db601cd27ce3f519baaa63667141688)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#archive_type OsConfigV2PolicyOrchestratorForOrganization#archive_type}
        '''
        result = self._values.get("archive_type")
        assert result is not None, "Required property 'archive_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def components(self) -> typing.List[builtins.str]:
        '''Required. List of components for this repository. Must contain at least one item.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#components OsConfigV2PolicyOrchestratorForOrganization#components}
        '''
        result = self._values.get("components")
        assert result is not None, "Required property 'components' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def distribution(self) -> builtins.str:
        '''Required. Distribution of this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#distribution OsConfigV2PolicyOrchestratorForOrganization#distribution}
        '''
        result = self._values.get("distribution")
        assert result is not None, "Required property 'distribution' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Required. URI for this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gpg_key(self) -> typing.Optional[builtins.str]:
        '''URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gpg_key OsConfigV2PolicyOrchestratorForOrganization#gpg_key}
        '''
        result = self._values.get("gpg_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24f9b5ea63e31fddbef63f03e3cfa284963b19f8e0e30108b2a84305454b0455)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3f49e1fdcb907cf1abae485b8c3032806d1b9d70d5267dd4f36426693f3dbd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "components"))

    @components.setter
    def components(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9175a234a9f1a1dafeef4dabcd5701189e449a7c38e6be49920eb36b85eeb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distribution"))

    @distribution.setter
    def distribution(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b2991804b855e31fe5422b6126bfafb87348bd2636e667c3e8efe04b4b96be4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distribution", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKey")
    def gpg_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpgKey"))

    @gpg_key.setter
    def gpg_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5256a87d54af28988157cb320d3eee92f8168bbab4fce06826cc662065ccbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c384d7f3f0cf8e3c79db1b109d867ff4cc383b1d616fbdae76f3c799072e7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d973c8bf5386bc429aadb6df07d9d3f7c82e5425c389999392c9fdb93955d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "url": "url"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo:
    def __init__(self, *, name: builtins.str, url: builtins.str) -> None:
        '''
        :param name: Required. The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        :param url: Required. The url of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#url OsConfigV2PolicyOrchestratorForOrganization#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1d87ad292a9786f8d57e0866a82e7a4ecbeb1b31750543469a1eb6cf69eeb7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "url": url,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Required. The name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Required. The url of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#url OsConfigV2PolicyOrchestratorForOrganization#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c1404fcaf81922adc287da050cfda92aef889d7e57bb63eeeb8a4ccc8860df4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8dc8dc6a9612e1a7485d1b235aa92c1cbb71ca7b167845d6d00e8624ec5ebb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff40650d090b6fc0a34167fcaf84205ad74dbeedffbf8a5d26c47a383ad987a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679bd816a9da40fd3265fc11aec9310e8de6d1c947cd166e02d116eed06dfcc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__240862915d49ebf7bb365a0d933d66c2f115f53bcb6e2c5ea47b7ffad5609525)
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
        :param archive_type: Required. Type of archive files in this repository. Possible values: ARCHIVE_TYPE_UNSPECIFIED DEB DEB_SRC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#archive_type OsConfigV2PolicyOrchestratorForOrganization#archive_type}
        :param components: Required. List of components for this repository. Must contain at least one item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#components OsConfigV2PolicyOrchestratorForOrganization#components}
        :param distribution: Required. Distribution of this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#distribution OsConfigV2PolicyOrchestratorForOrganization#distribution}
        :param uri: Required. URI for this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#uri OsConfigV2PolicyOrchestratorForOrganization#uri}
        :param gpg_key: URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gpg_key OsConfigV2PolicyOrchestratorForOrganization#gpg_key}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt(
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
        :param name: Required. The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        :param url: Required. The url of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#url OsConfigV2PolicyOrchestratorForOrganization#url}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo(
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
        :param base_url: Required. The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#base_url OsConfigV2PolicyOrchestratorForOrganization#base_url}
        :param id: Required. A one word, unique name for this repository. This is the 'repo id' in the yum config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for resource conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#display_name OsConfigV2PolicyOrchestratorForOrganization#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gpg_keys OsConfigV2PolicyOrchestratorForOrganization#gpg_keys}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum(
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
        :param base_url: Required. The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#base_url OsConfigV2PolicyOrchestratorForOrganization#base_url}
        :param id: Required. A one word, unique name for this repository. This is the 'repo id' in the zypper config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for GuestPolicy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#display_name OsConfigV2PolicyOrchestratorForOrganization#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gpg_keys OsConfigV2PolicyOrchestratorForOrganization#gpg_keys}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference, jsii.get(self, "apt"))

    @builtins.property
    @jsii.member(jsii_name="goo")
    def goo(
        self,
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference, jsii.get(self, "goo"))

    @builtins.property
    @jsii.member(jsii_name="yum")
    def yum(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference", jsii.get(self, "yum"))

    @builtins.property
    @jsii.member(jsii_name="zypper")
    def zypper(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference", jsii.get(self, "zypper"))

    @builtins.property
    @jsii.member(jsii_name="aptInput")
    def apt_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt], jsii.get(self, "aptInput"))

    @builtins.property
    @jsii.member(jsii_name="gooInput")
    def goo_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo], jsii.get(self, "gooInput"))

    @builtins.property
    @jsii.member(jsii_name="yumInput")
    def yum_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"], jsii.get(self, "yumInput"))

    @builtins.property
    @jsii.member(jsii_name="zypperInput")
    def zypper_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"], jsii.get(self, "zypperInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0203ddbc78c047f23f948938571a9ad1dd0de34be70f78084c367f5710987d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum",
    jsii_struct_bases=[],
    name_mapping={
        "base_url": "baseUrl",
        "id": "id",
        "display_name": "displayName",
        "gpg_keys": "gpgKeys",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum:
    def __init__(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: Required. The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#base_url OsConfigV2PolicyOrchestratorForOrganization#base_url}
        :param id: Required. A one word, unique name for this repository. This is the 'repo id' in the yum config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for resource conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#display_name OsConfigV2PolicyOrchestratorForOrganization#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gpg_keys OsConfigV2PolicyOrchestratorForOrganization#gpg_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a0ee4b514fcc597c561302c85997d3c2cb35b6d4ccc6193c78e84dc002ae06a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#base_url OsConfigV2PolicyOrchestratorForOrganization#base_url}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#display_name OsConfigV2PolicyOrchestratorForOrganization#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URIs of GPG keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gpg_keys OsConfigV2PolicyOrchestratorForOrganization#gpg_keys}
        '''
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bb56458f77fe7aad0142164372791cf49a28969e3a23e64932ec09ba8e19773)
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
            type_hints = typing.get_type_hints(_typecheckingstub__887cc3a6bd4786fb80cb7475c1655069cf6bbeee450afabf0ecce3f78776c810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54029686aed74d2560fcd4486920716c7707b9005506d370cede487e65a205de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKeys")
    def gpg_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gpgKeys"))

    @gpg_keys.setter
    def gpg_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e77309b5699d111b07e22fb79ab529881f96e22fd81a97c2360b821b61f2e5cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afc3fc46a11f99e3334df02294453a2c1ededdc3254dccb17384e88ae8d6e91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9101c1ecf049bf4f3cc65d9aa4b27b0d02dcf8acb95e130a6cc0e286bc6a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper",
    jsii_struct_bases=[],
    name_mapping={
        "base_url": "baseUrl",
        "id": "id",
        "display_name": "displayName",
        "gpg_keys": "gpgKeys",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper:
    def __init__(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: Required. The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#base_url OsConfigV2PolicyOrchestratorForOrganization#base_url}
        :param id: Required. A one word, unique name for this repository. This is the 'repo id' in the zypper config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for GuestPolicy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#display_name OsConfigV2PolicyOrchestratorForOrganization#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gpg_keys OsConfigV2PolicyOrchestratorForOrganization#gpg_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad197deed9e6ac7a9ca590542646a58c448a060296582a6c0ffa5cfab4b6cc3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#base_url OsConfigV2PolicyOrchestratorForOrganization#base_url}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#id OsConfigV2PolicyOrchestratorForOrganization#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#display_name OsConfigV2PolicyOrchestratorForOrganization#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URIs of GPG keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#gpg_keys OsConfigV2PolicyOrchestratorForOrganization#gpg_keys}
        '''
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78f333adfd824d4e48df4ab54aba9929011ffb66d922bca257fa3325613cdebc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f14785cd4123ecf438661f87dbb198e3d09a75e4f5332a28585e225a0dce5b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e727f7a8b4e377a4bf85dd6f40c4da1d085b0a52c3b58f752aa071f2b3615f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKeys")
    def gpg_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gpgKeys"))

    @gpg_keys.setter
    def gpg_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13dc0930489a9005066d9308ed3a7a9ef5895046b82628b17a29fdc266720359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e80dab66f407989ce893fa6de45eb120c1753031932451a7385c3aed702591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d63a7b0471f32f55a02be011012a9fa6bb0c9ad65c6ef1ad67a5e4a8a5221e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5836ea110fcfee11e0051a136e24d880b21a2bfa70f4c3d63c81421c2491ff6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInstanceFilter")
    def put_instance_filter(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
        inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
        inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all: Target all VMs in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#all OsConfigV2PolicyOrchestratorForOrganization#all}
        :param exclusion_labels: exclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#exclusion_labels OsConfigV2PolicyOrchestratorForOrganization#exclusion_labels}
        :param inclusion_labels: inclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#inclusion_labels OsConfigV2PolicyOrchestratorForOrganization#inclusion_labels}
        :param inventories: inventories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#inventories OsConfigV2PolicyOrchestratorForOrganization#inventories}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter(
            all=all,
            exclusion_labels=exclusion_labels,
            inclusion_labels=inclusion_labels,
            inventories=inventories,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceFilter", [value]))

    @jsii.member(jsii_name="putOsPolicies")
    def put_os_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8cb37be65d6be8e9c850b59e4817c9a68d48d84f12aa21e842aeef7fc72a0dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOsPolicies", [value]))

    @jsii.member(jsii_name="putRollout")
    def put_rollout(
        self,
        *,
        disruption_budget: typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        min_wait_duration: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#disruption_budget OsConfigV2PolicyOrchestratorForOrganization#disruption_budget}
        :param min_wait_duration: Required. This determines the minimum duration of time to wait after the configuration changes are applied through the current rollout. A VM continues to count towards the 'disruption_budget' at least until this duration of time has passed after configuration changes are applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#min_wait_duration OsConfigV2PolicyOrchestratorForOrganization#min_wait_duration}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout(
            disruption_budget=disruption_budget, min_wait_duration=min_wait_duration
        )

        return typing.cast(None, jsii.invoke(self, "putRollout", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEtag")
    def reset_etag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEtag", []))

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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference, jsii.get(self, "instanceFilter"))

    @builtins.property
    @jsii.member(jsii_name="osPolicies")
    def os_policies(
        self,
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList, jsii.get(self, "osPolicies"))

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
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference", jsii.get(self, "rollout"))

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
    @jsii.member(jsii_name="etagInput")
    def etag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "etagInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceFilterInput")
    def instance_filter_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter], jsii.get(self, "instanceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="osPoliciesInput")
    def os_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]], jsii.get(self, "osPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutInput")
    def rollout_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout"], jsii.get(self, "rolloutInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eadbfc5cbd2c7e5645552ffcda8a68c155bb5f171b7a3f6b59f32a10f9d44df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @etag.setter
    def etag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5d0b07507b3a7aa24f0f005a40c99dbc7b68b4236801e89d5d71b11c5076450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "etag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e105e76fa460adcedb947151cf9214fb4eec94374d81a9cd621382c425cecab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16bb31d944c00a8161d004bb8f122cffcf78493dfde929f8eb0dd382d19a352b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout",
    jsii_struct_bases=[],
    name_mapping={
        "disruption_budget": "disruptionBudget",
        "min_wait_duration": "minWaitDuration",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout:
    def __init__(
        self,
        *,
        disruption_budget: typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        min_wait_duration: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#disruption_budget OsConfigV2PolicyOrchestratorForOrganization#disruption_budget}
        :param min_wait_duration: Required. This determines the minimum duration of time to wait after the configuration changes are applied through the current rollout. A VM continues to count towards the 'disruption_budget' at least until this duration of time has passed after configuration changes are applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#min_wait_duration OsConfigV2PolicyOrchestratorForOrganization#min_wait_duration}
        '''
        if isinstance(disruption_budget, dict):
            disruption_budget = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget(**disruption_budget)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4073396de18ef4709dc34bbd8b0cc6eeacd50e906489c7973bf046a2dc6a3af9)
            check_type(argname="argument disruption_budget", value=disruption_budget, expected_type=type_hints["disruption_budget"])
            check_type(argname="argument min_wait_duration", value=min_wait_duration, expected_type=type_hints["min_wait_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disruption_budget": disruption_budget,
            "min_wait_duration": min_wait_duration,
        }

    @builtins.property
    def disruption_budget(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget":
        '''disruption_budget block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#disruption_budget OsConfigV2PolicyOrchestratorForOrganization#disruption_budget}
        '''
        result = self._values.get("disruption_budget")
        assert result is not None, "Required property 'disruption_budget' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget", result)

    @builtins.property
    def min_wait_duration(self) -> builtins.str:
        '''Required.

        This determines the minimum duration of time to wait after the
        configuration changes are applied through the current rollout. A
        VM continues to count towards the 'disruption_budget' at least
        until this duration of time has passed after configuration changes are
        applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#min_wait_duration OsConfigV2PolicyOrchestratorForOrganization#min_wait_duration}
        '''
        result = self._values.get("min_wait_duration")
        assert result is not None, "Required property 'min_wait_duration' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#fixed OsConfigV2PolicyOrchestratorForOrganization#fixed}
        :param percent: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#percent OsConfigV2PolicyOrchestratorForOrganization#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d37cd84a1d0d3d3695b504459f1944a69334ec60c007bdb7bfd5496b0d94bac)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#fixed OsConfigV2PolicyOrchestratorForOrganization#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies the relative value defined as a percentage, which will be multiplied by a reference value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#percent OsConfigV2PolicyOrchestratorForOrganization#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e99b0bb63bdf496c924f6661447c28d2603e95682edcb1c51a73b6b7fb4151f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__163a8532af351245659620d6358785628391665ce04e847f483b6c70275fc12e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69a8b8f27ec7654f57fc9a4157da5b5165a1f255909602d9e9f78830101b1cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574fc682247b3f4d303588db8fd0b95670f930f05fe613c2b0c72ab36146a682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64306960c0999515423945ba23be9bad24dd799a158b303df08fc61fa773646e)
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
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#fixed OsConfigV2PolicyOrchestratorForOrganization#fixed}
        :param percent: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#percent OsConfigV2PolicyOrchestratorForOrganization#percent}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget(
            fixed=fixed, percent=percent
        )

        return typing.cast(None, jsii.invoke(self, "putDisruptionBudget", [value]))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudget")
    def disruption_budget(
        self,
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference, jsii.get(self, "disruptionBudget"))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudgetInput")
    def disruption_budget_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget], jsii.get(self, "disruptionBudgetInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__40e2f72eb4fb47eed2b0849bb39c94735d1c63e34cff14b1bb4d7d4db2450035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minWaitDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c74060fd6106b6bf46dd15e1ec20a567544d1826d63dca491fdd8788c2feb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e428082ff3b57a488e4b3893bc8d2b57e923a15c0c96d137fb331f5f374d8cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOsPolicyAssignmentV1Payload")
    def put_os_policy_assignment_v1_payload(
        self,
        *,
        instance_filter: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter, typing.Dict[builtins.str, typing.Any]],
        os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
        rollout: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout, typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        etag: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#instance_filter OsConfigV2PolicyOrchestratorForOrganization#instance_filter}
        :param os_policies: os_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#os_policies OsConfigV2PolicyOrchestratorForOrganization#os_policies}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#rollout OsConfigV2PolicyOrchestratorForOrganization#rollout}
        :param description: OS policy assignment description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#description OsConfigV2PolicyOrchestratorForOrganization#description}
        :param etag: The etag for this OS policy assignment. If this is provided on update, it must match the server's etag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#etag OsConfigV2PolicyOrchestratorForOrganization#etag}
        :param name: Resource name. Format: 'projects/{project_number}/locations/{location}/osPolicyAssignments/{os_policy_assignment_id}' This field is ignored when you create an OS policy assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#name OsConfigV2PolicyOrchestratorForOrganization#name}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload(
            instance_filter=instance_filter,
            os_policies=os_policies,
            rollout=rollout,
            description=description,
            etag=etag,
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference, jsii.get(self, "osPolicyAssignmentV1Payload"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="osPolicyAssignmentV1PayloadInput")
    def os_policy_assignment_v1_payload_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload], jsii.get(self, "osPolicyAssignmentV1PayloadInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d0b211b575ecc67f3735285603f8e028a2cbee04aa9f34e96c75e4c65fedf86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6726b383f943f9f8ecc11aeecac84ff48490769637be91f6233c566df9dc0a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope",
    jsii_struct_bases=[],
    name_mapping={"selectors": "selectors"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope:
    def __init__(
        self,
        *,
        selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#selectors OsConfigV2PolicyOrchestratorForOrganization#selectors}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c131c5490836949a22ea4c1b7bf74470dc1409ac38f4fe5914d27c9671b68df)
            check_type(argname="argument selectors", value=selectors, expected_type=type_hints["selectors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if selectors is not None:
            self._values["selectors"] = selectors

    @builtins.property
    def selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors"]]]:
        '''selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#selectors OsConfigV2PolicyOrchestratorForOrganization#selectors}
        '''
        result = self._values.get("selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__708a9037cd7c7d4fc035dbd5f174a24774dda63c862cb6e2dc6927c078f58da1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelectors")
    def put_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd821dfa8f50e287bd4cba548e2a3f246db1b88342b7c0ed67442919088170b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelectors", [value]))

    @jsii.member(jsii_name="resetSelectors")
    def reset_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectors", []))

    @builtins.property
    @jsii.member(jsii_name="selectors")
    def selectors(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsList":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsList", jsii.get(self, "selectors"))

    @builtins.property
    @jsii.member(jsii_name="selectorsInput")
    def selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors"]]], jsii.get(self, "selectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf7b43ff4abe4951128025a37693fb112957696aa9109bab9f6f9ba20f7774f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors",
    jsii_struct_bases=[],
    name_mapping={
        "location_selector": "locationSelector",
        "resource_hierarchy_selector": "resourceHierarchySelector",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors:
    def __init__(
        self,
        *,
        location_selector: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_hierarchy_selector: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param location_selector: location_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#location_selector OsConfigV2PolicyOrchestratorForOrganization#location_selector}
        :param resource_hierarchy_selector: resource_hierarchy_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#resource_hierarchy_selector OsConfigV2PolicyOrchestratorForOrganization#resource_hierarchy_selector}
        '''
        if isinstance(location_selector, dict):
            location_selector = OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector(**location_selector)
        if isinstance(resource_hierarchy_selector, dict):
            resource_hierarchy_selector = OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector(**resource_hierarchy_selector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b35f6d2dac0c86cf51068a864fa143eaa585f4b54aa01be65e6a32c20a3e2a)
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
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector"]:
        '''location_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#location_selector OsConfigV2PolicyOrchestratorForOrganization#location_selector}
        '''
        result = self._values.get("location_selector")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector"], result)

    @builtins.property
    def resource_hierarchy_selector(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector"]:
        '''resource_hierarchy_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#resource_hierarchy_selector OsConfigV2PolicyOrchestratorForOrganization#resource_hierarchy_selector}
        '''
        result = self._values.get("resource_hierarchy_selector")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8fb320fe067e33359c10d5661d17919ff505e465ad923a3e826a51b8a931186)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef70baa62f0358d8130a1a6b8497d898544e1251efa392cd2fdd2f6f003a5c5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ab3af52a645e5294093d54bafc5d34e95100347aabf3dcb1560f6f069ad108)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7293808435973a5523dc945b8e9d716b1bcb62f80739da67e37a08a90b605bb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1234a92abb939b1711181940e97b07e00c88a2c54cbda60eb6bfbfe615a99f1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796eb1b0da50a1c2d91eff3b4db5feb6a26cae4fdfd81a105b9624a66f24db86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector",
    jsii_struct_bases=[],
    name_mapping={"included_locations": "includedLocations"},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector:
    def __init__(
        self,
        *,
        included_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_locations: Optional. Names of the locations in scope. Format: 'us-central1-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#included_locations OsConfigV2PolicyOrchestratorForOrganization#included_locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79020a4af42e8e04c584cb6a1bb0e9ba9857407d11d27346d76d290bc83b19a)
            check_type(argname="argument included_locations", value=included_locations, expected_type=type_hints["included_locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if included_locations is not None:
            self._values["included_locations"] = included_locations

    @builtins.property
    def included_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Names of the locations in scope. Format: 'us-central1-a'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#included_locations OsConfigV2PolicyOrchestratorForOrganization#included_locations}
        '''
        result = self._values.get("included_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c128559712bd21a322dc24e9dc58bc5b271e3c5043447569a73d8b9d729c611)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e77381c4565ccddf1118a18b5f06a6c74ac95ee49c4df03fa6c4ae3de4aa3e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedLocations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f797e339b0c32a6860d481e87849a222483a2bb5bf8fbc3f5495c79534696d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9b4414bf3679a7cc4d16181321a26ae8ca9bdfa199384ffff8dd0a2edc940ab)
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
        :param included_locations: Optional. Names of the locations in scope. Format: 'us-central1-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#included_locations OsConfigV2PolicyOrchestratorForOrganization#included_locations}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector(
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
        :param included_folders: Optional. Names of the folders in scope. Format: 'folders/{folder_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#included_folders OsConfigV2PolicyOrchestratorForOrganization#included_folders}
        :param included_projects: Optional. Names of the projects in scope. Format: 'projects/{project_number}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#included_projects OsConfigV2PolicyOrchestratorForOrganization#included_projects}
        '''
        value = OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector(
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelectorOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelectorOutputReference, jsii.get(self, "locationSelector"))

    @builtins.property
    @jsii.member(jsii_name="resourceHierarchySelector")
    def resource_hierarchy_selector(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference", jsii.get(self, "resourceHierarchySelector"))

    @builtins.property
    @jsii.member(jsii_name="locationSelectorInput")
    def location_selector_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector], jsii.get(self, "locationSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceHierarchySelectorInput")
    def resource_hierarchy_selector_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector"], jsii.get(self, "resourceHierarchySelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02aa378e1d1adf1173cc06cac8e07db3dc4c31553fc6e997bc10eda9516ef310)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector",
    jsii_struct_bases=[],
    name_mapping={
        "included_folders": "includedFolders",
        "included_projects": "includedProjects",
    },
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector:
    def __init__(
        self,
        *,
        included_folders: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_folders: Optional. Names of the folders in scope. Format: 'folders/{folder_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#included_folders OsConfigV2PolicyOrchestratorForOrganization#included_folders}
        :param included_projects: Optional. Names of the projects in scope. Format: 'projects/{project_number}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#included_projects OsConfigV2PolicyOrchestratorForOrganization#included_projects}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12fc48a501f33f0a17e146b4565e0fe5d8d5b18cbb0e861c685b5acce22324b9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#included_folders OsConfigV2PolicyOrchestratorForOrganization#included_folders}
        '''
        result = self._values.get("included_folders")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_projects(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Names of the projects in scope. Format: 'projects/{project_number}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#included_projects OsConfigV2PolicyOrchestratorForOrganization#included_projects}
        '''
        result = self._values.get("included_projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a41d3be48776b8b5bcef0d7555ebcfee5281bdc95b8efe5b0a057929970bf6dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef983df57749477c2edcc6039e054c653762e2361715cd6274d38aaaed336b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedFolders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedProjects")
    def included_projects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedProjects"))

    @included_projects.setter
    def included_projects(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51ae3927b3e178a8765b4b18b96756913e6e138f825b64a9a6a0d26715dd263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedProjects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e043fb9b19e4f6247efaaeb98eb960a6ae91b89a1052531cb477065a8d1dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateError",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e769430dd6c13e15d1eedcc9e9db90c3d587d7213d368fc9523b3d008697d32c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e83050cc3e9564e76537be9b66b945d27bb8431dfb4a59c8b5ef6939418cdf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6432c196d197c3054e67faeb65eb69e2934176c81ee9a2cf09d99b1402e29daa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10d7faea3f60c021858a64256fdbf026a44f8b53fd580c0ef49a13f0a73a0e40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0aaa70b1f4d3797c0f0eee3da1615390905198492e0aef7e55a876d48839983c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42998e5d5c717744595f14c9cbc7354895bfeacf245f49bf8d8b25eea90f9afd)
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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetails]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9e6ce7d448bccfdd470a7e022a582c30c440f0bdcbba035704ba03c014e690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3738e1d16d62eecf616b079977ce45e9fc38258bdfa7a04af69dbc7830fb9356)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dacf65a58cc158c76ae0fcada3d4926fda39aa8f4ac7293fd48c92173f5d4798)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8271555e0972079cab2fde67987e228e4048fb246a4e31079ba753f8283fc819)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf393cd58ba26c638e37f2a4ffae1d78588fa148e3b2cc3c04a671c5fb8c9d59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22e5412ae8a0a3510c1d939fdfe37f8789e47101e6877d671de41e0156fab6fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bf68445d7dba236ed963982d3895a8bd0dc2fbb7f465597dcf8081a172c44e3)
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetailsList:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetailsList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateError]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ae00ca6bad3842a0c79b6e22e359468b8e3627fbf5134f0337e9b380f06af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ab6e614ae7ec62746224d0bac8d66f8db91e0f73e01a14337d0a467eb3e4ac6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834339f36b1d24359301837af4aeb766cd5b1107bf8282c2f2444be30bf74cee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ce7eb3e1f84bb7d97ecfa1f1018f7127a1ad3e8278868b4b8c7010466178d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a06bdea621d1bbcabba6fcb8d81a9bf02719252b9d87dea733c421bd6991db09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3c5483c4b32afdb2516f07f814cb05839ab3c2fa9ea6e6cb43a336dd85c69e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbe19e5bfa5752501a4024b7ffe03df5a9a208c06b4f3c6740f93dc4dc4bd810)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(
        self,
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorList:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorList, jsii.get(self, "error"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationState]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__118b4b1901d3a8d31695d8e4f44ea747b18ceb9866e26d83922cff63c4ebf857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d8204a84a23216a4e9004d71e721f55b670f9c9c264cf1b9f426133e2b63d58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66fae2875f668f37a1e07850575148a1b2b026456227b24a3cc289503ac7670c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a125a73d4543aec320e5a0c04a0335d68b6b7f81538a5f782d04e1940f33cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbcf0531a4fe1e2a8492b3b1b062ce63d99320e12e55a61d554fa779cac6e638)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d32cd3698e0dd44b7b74b3a16a1c3018794f3d1ba065d2354fa110a14f58b50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64361503f5f20621f2c804955dd15270fa500e7adb419d7855a642223839cce6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="currentIterationState")
    def current_iteration_state(
        self,
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateList:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateList, jsii.get(self, "currentIterationState"))

    @builtins.property
    @jsii.member(jsii_name="previousIterationState")
    def previous_iteration_state(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateList":
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateList", jsii.get(self, "previousIterationState"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationState]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415e06fb6883f3bd129a7b657c1eb99a7fe7bc9f629e90fe3570eba08ecf92fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateError",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90ceaf44a96649c026b9317de66a58ac1237e5c9ccc09e92ff59c260467a8607)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e9b423af7777daf114b093b5297d2cdb5df3869a8e58ac93496cdbf70878a4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38489c29d35f9cf8d145fe1c1ad12a0d657d01141b994d2b26126efe3feba8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e52031c65877826726b227789e22bf43b11baa2a47d8dec9d14f52cc5c72024)
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
            type_hints = typing.get_type_hints(_typecheckingstub__941e1f08cc672b9e972ecbb1f6f72a19162992652f7a999510f629bbb696e2fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc624cc409f63a581cd8f108e7e49bfcb3e28ca2086f81599e58e8293125faff)
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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetails]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55feefadb7551a57ea4271e03ee40091fa02c644735729dc7393888953fcd7e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba71cd8662881628e9ce10ebb94adf1e7541086f45ab2f5c1aba5f66e053672c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee66f192e3c9efeb15fc8c6c31543a8214924089efada5248b5e603a6957f527)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c176356df7de35be31a108127b5d6a332f02b5fac51a218cf058b4d6e9dca4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ab1968be1ff3498a468889741db45d777e4e31d5c0ecef1db84135c5b5a63ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8436bd629899ec20677caf88c9cab44973fcf7e67088a8832f5213199fb2e69b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__322ba0955d6def42a188be0e260e593d88c5ba4d390646c003fb9dc9ca47325b)
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
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetailsList:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetailsList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateError]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c1c8450a776a74d18e854519b6ff993da1e61ac9139e1bd41edb6c07eafdd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1242be5046f62539cca792017b77370dc006498e1e724749d39d554a8714516)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a8e3c87daaef291eb0b9622bce8ffbd1b912cc487eab5219e4f35555960a2b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a4b6df859bfa6a3a171b10f93ffc4a1a65a29e4c8d0b6f76c6ca5787e6e447)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cc18e9038abdf4fd2b3cc2763ca1dd78cf487a12a8f15b69cc8cea48947aab3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__757314a8ec7c6f1085ab54a024d1a0654eefa7422387b8f8ab4730aed4edcd0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9145f5f74b6721df0d304e181eeddb4c33e9a8d2594d06503f24eb501d412b4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(
        self,
    ) -> OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorList:
        return typing.cast(OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorList, jsii.get(self, "error"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationState]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf7d9ea90affce302d25bae14467f9d86aa0160f30a524a8b252c0abc3a7f34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class OsConfigV2PolicyOrchestratorForOrganizationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#create OsConfigV2PolicyOrchestratorForOrganization#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#delete OsConfigV2PolicyOrchestratorForOrganization#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#update OsConfigV2PolicyOrchestratorForOrganization#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d10acec3856fbbf156b5958f08bb24d76ba3c371d919ea01c44b645437de154)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#create OsConfigV2PolicyOrchestratorForOrganization#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#delete OsConfigV2PolicyOrchestratorForOrganization#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_organization#update OsConfigV2PolicyOrchestratorForOrganization#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForOrganizationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForOrganizationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForOrganization.OsConfigV2PolicyOrchestratorForOrganizationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75b22ef496237773a4eb541a7fde6e68521e8a0e4e80d06edc96cbfdcf872a3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f433a59901742ccedcf61518c15b58e252119e4bcc8bd84209599b0e7d819b8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d541494b1b752f387ba1cdd522efd26b63e66082a5ad12c8414cb7ef9e9aa0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb4e82fc41f91d33dca4b644afff50e04b71bea74baead550e6c2d31c6d14de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ac08c9664a510f2946e5164740f5cdb1b5ba9135c2b61f7bd63c31969596db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OsConfigV2PolicyOrchestratorForOrganization",
    "OsConfigV2PolicyOrchestratorForOrganizationConfig",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelectorOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationState",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationState",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateError",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetails",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetailsList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetailsOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationState",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateError",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetails",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetailsList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetailsOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateList",
    "OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateOutputReference",
    "OsConfigV2PolicyOrchestratorForOrganizationTimeouts",
    "OsConfigV2PolicyOrchestratorForOrganizationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__02b10b215bc8f6831dcf7e393a540c23b15d4a062df33764508187f232783651(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    orchestrated_resource: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource, typing.Dict[builtins.str, typing.Any]],
    organization_id: builtins.str,
    policy_orchestrator_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    orchestration_scope: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope, typing.Dict[builtins.str, typing.Any]]] = None,
    state: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f4b362b9a8490da3b2019c0331db09e0b6da6e7c999553819585484b97356f5d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de11a4572aa6400d4c3568cb569582c84670b0dbfea653c9115e82733a245827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4815037a7f562d48e20556ba1c5adfe349e90d92f16e5b7845acc9ff41939f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6dcc558da5320077df3d8f67306023b4e248b62a06b230b3e4e73d396debd02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124865ff2019803ca1afabf0c5ac612dd2c3a282fd9e5f46b9531fcd9606cff4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c258fb683b99d22b7e9b9a18359c46127ca579c9c8580fb22005f49a907919d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bdfd2736d2f58a7da20ddc53d52f0e7511f74b7af0ab3d40e78b424bf178a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea73b4842082d97c4b76f958e50e9af5c78708071ce71dad2291becc5ae04c84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb798e48ca17ff16d26976b83a58d9d32d6ad52acdc532f17b5c9f2cbfc533d7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: builtins.str,
    orchestrated_resource: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource, typing.Dict[builtins.str, typing.Any]],
    organization_id: builtins.str,
    policy_orchestrator_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    orchestration_scope: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope, typing.Dict[builtins.str, typing.Any]]] = None,
    state: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69f1b258ef34f83f145214ac90a711295d189af4931c23f63c021fdb3df3243(
    *,
    id: typing.Optional[builtins.str] = None,
    os_policy_assignment_v1_payload: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f334dd60053a432ec4f5de094a39f8cf4260f12efb076a9d4bd44b45578c8c(
    *,
    instance_filter: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter, typing.Dict[builtins.str, typing.Any]],
    os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
    rollout: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    etag: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ac287c73be5ffae1e5fec1a8fb7b3500b9b1e3c2bb11d129832af946c6f207(
    *,
    all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e85fb4cc96c37a94d2f5e2083b1a0cdf0a5338e96b741196d50d35fcf1afe28(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65340af8a60ee405f5957700653e12fae00a926dc7ee9b512ae8a12c81b375e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e96f89aa1f6874e3bb2fde1ce240101c9d578781b6699e026c5e28de7ed419(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2524b89d52bfb39a39d2c078914674137d85db54903de531a19f879cc78d19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71725bc0e65b324651c257055d6c1e5d1b484301c9630d8f80fdd40d58804017(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae52b9f2afcefeaad5d1f6a9f70dd6a96ec6500680894b534c3550d0a9768db7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba2dd9ea98e2505619979b0bc821b6e581f78a3e307ea11d94fa808a933589a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d6926c498f96b5405e80974e6ad57233dba6e11c92c091ddda3063ce32584b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be452cc3cf550dd304a0d3f7b00a1f690d82d3165b71328f84a7a2d94f4fba5c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62aca8c672e823f6a0c741b5eddc099b1337ab09f2af6017738431efa3034a2b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbede0ee2a585d21293e6bfe168f4f118f33d37ba34aa4330b94690ea3bf3f03(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3535a53a2ae9c7b9124d4d737818cf1a33da6839dccdadbbbc26e9f98d924a86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6ec2ade62847d85c91f7802d21e240920f40dfea8414ae72eb425dbb96cdcd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597814fb8c0af4f77fc101242c25bf2fcd0977ffc59879bfb6f6845d3867c517(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07e5537f91b59470391a189ee40979a6807d99935751e2cad9a9b9a7a343d1b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3760c77c23bcdf15b83574a14cf448a9b463ccdccb13062ec75fa5d23ab4f1e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a2e363b575c0cecbd488518d2705c9efbe26bc9a63139722e49362863519d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c3906b6f790b84769ae1d2b4fbad86d10a2c96d4da915f298d864cb4f858ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa6c4a29f993603f46ae7e7650323e3049c8923d7318d420171a315a4b8950f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758fc66f8840a70ff89c2122bcd121785b938fafb7fd88b22db7843eb76217db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d206cb5935bc9f5c4b14dae637a4d5681ae884a01be51b8705c9c68bb0ed4f(
    *,
    os_short_name: builtins.str,
    os_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9654e8ebfce074337abb13c726748819fed006e6cf48686b5a4ab7f82e77ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc90bddbb64fbd6856634a9adbaab679befab093aa9cce868f7067f9b1b5070(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d564a0c41f9486a843afdc35c7e0d699ff197f2bfac5656257927e79ae84a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae37c62672cdfefafd663cc61ad035e3d763932325083370e85a52e61c9e0fa1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d972387a73d43a7cbc5db7443fb2a4c85eeb70c4bfda3ce1265a9067c58a1d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290c5bb7a8674835df80fd18712a1f48e7dc8453c373f89cdfcbf57b92e5323f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b524a7d45efd7b1e396e4f2455962392774264794f5bdef8bde75eab6706a9a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b7688e3b266eb810dfb75634d854a6d049c61088e94b89a22dd5fe2bc3d0c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0079c8c1589e9fa0f6026a8bc798ad973d613063de7adfddda64234345476505(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db22a34aba54fd757d9f1db2f13b897f01e9e46c62e182878fc5a55bfde7ba9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c1c5811549f87cfa0318c73c8e6befda64b49610d59c2baa6b00f8d096f25c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d467c5e18be762fc83320ab16549f2727b809b8a6c9eecfe06d43ed5551eb1f5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03035a3e3493fbde0fee940e687781a909b2fdaa993a2d5659cd8b4dc79441a4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ad79fb61b466c58a3a2b63fd9227b175f9063bcab53430409307395cff1e12(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9adcfd1adc2e49637d1e7a69905a28edd06040d8760ed17a7b2062a5c035fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace6c87dc6a37a82d4389e30bf0b8e2ca0f881dd3e3e86d1bf51eddea03d077d(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc35915575d30f279ebae167e23642509633a08317a6dddd29d6fbe6bbae7b0(
    *,
    id: builtins.str,
    mode: builtins.str,
    resource_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups, typing.Dict[builtins.str, typing.Any]]]],
    allow_no_resource_group_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd3420d4a87ca4ccce5378965c76e025c2db5c4cb7bbf4b219b5f5d681b9d75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ebdf04f9a135b9fa7f6e81e35a42430e2542bf6471ea457a74f527ae0e80ebb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcfeecee8da7a83e87072f5bf5e4f83bd3c9bfc8a547b712596cc34d663205cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d31faea6fef6479aaf070fd52fb19757634a347ced2f6a563c47832171bcdaf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bab33e7b80dbb61218f45719c60a007713805c728f1470483f0b136c497a6fd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2b0d57ba836090207cf590ecd1153f38d6b1ccdb757d0618b51b28c27c4934(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7e3b7dbe81c056b629397a7e1053a2be19c7d556eebdd82c66610b3c37c076(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e3b62a22d17226c4111778cfa8dbd78199cec29701927ebfeff82485513658(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16ca00f47c3772f77c5f279a0a9027bf4f7eb22e8bd78e26e3dae7f9c0f8e5d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aab65e3a52c4d15d52f5d1666b574afa6194a24f28956140c6a1007d4d6a66e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8352023fe8f718854fc39343b5b171d5b8633bf4595ea64270f8837f6e3ffc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1f14cd97a3cd27a1f31803735447642d8b80770ef14b12586277b8ac60b402(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7f2d53f9c5660789413de3886f5899a268c0aea3ec6ec649652ee4d3771e08(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f7a3fefe16a32d5befa24cab89ec47ae3506b7631a464f39f78c7bd7f23c56(
    *,
    resources: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources, typing.Dict[builtins.str, typing.Any]]]],
    inventory_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f120fd2b8624e5f99ec5a696677ce792dc654cac8daecd5dcd3c48b7a3f51102(
    *,
    os_short_name: builtins.str,
    os_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c074b729b7d610e54bf35e43db4827daffeb65eda1094301a60eec4d7a6a7c9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8826674e85c4d4c9b3f99c9ddab976338b69637f6cfe6c32478911aa5a9b41d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b33c7aed9ffd5d861299ae1d57e83042904b09fd33312dc94acc297636b5df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0144b90cbdc53ccb3abb9a45f020576eed3038373a0b1f785a4ece935fe0b139(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4413249de279dc056e383a2b2aa272db7da810761e53c0f1757436ff593847a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54381a8108e902b5eb5a4ccce8feb7d71b39fab02ab399abe20bc3f52e6047a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb732b93ae0eec89a027ec678d5a9f8bd534357d1eeae425131ceddddb16479(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883536077b292ed761b79dc31a8cfbdfd5910f4024e4863bd2abef67a6ef7630(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5de236e2171f14f9804bc3cc531d6087f05876bdd20b4e4a16f97eed0faa6da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635fa39f7cc624107a2ee4f17ef31ab07b0ae448cac98d1427411dfbfb17d80a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173a0b3334d4670f340c0417b7ee124309f89eba60613c4aa659260304169092(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc83b69f9310d3b3708d0a36837cddf943f05df34696f4bf21de33732afc489b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d04f37e8d5af5a8f220e20fec0c6bf97039683cacda0b6758ddc4ad66c7414(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826ecbe907ac36b7bcec7b50dca1a333bf75e1c832109c6db6bb4ab59172e9f6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb9b15dc639b8711636876ae3553b845d375a3a0d556703239e244c7dcf93bf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128b6999df7feed3a4f6bbf773e90b6061623772daef9c77da37907fa321f9d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f036d48becca546b597d80aa0136f9bcb0d44ec1473a14196fad040836968bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc6d0140e680d93257f026f6d36a64bfd87e1155298ebceec0e344014ea5ba1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ebb0a0255f99715be58ef29a87a3f49ff6303dffe858f82bd3afc4ea429f88(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947a4e8057d4e33fee5e6c14b7b8f5d2384d962801608cda9913d697010e8a44(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e350c71b07ac91dc57c59ab8ae3ef5abc2048e6e3e4e1d6a5e9cb17fb4ac05(
    *,
    id: builtins.str,
    exec: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec, typing.Dict[builtins.str, typing.Any]]] = None,
    file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile, typing.Dict[builtins.str, typing.Any]]] = None,
    pkg: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg, typing.Dict[builtins.str, typing.Any]]] = None,
    repository: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fcf755620de9492e0a8dca376b0d0494579e65eeaeff36a83d5a47dd7ed5ef8(
    *,
    validate: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate, typing.Dict[builtins.str, typing.Any]],
    enforce: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162ffd9661a0d143377e577204168ad080a1c21bd50d82772fe3ae11c9abb81c(
    *,
    interpreter: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile, typing.Dict[builtins.str, typing.Any]]] = None,
    output_file_path: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7415b4cced7175da978d6ec3b05d7a38d27c093f3b92348657be322918d3ec(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2311ab998a9248c4651f378cf1fcbfce8df9de971c192a14c075fb4c259f698(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3429b17ca07b1ae6f702732bc16040fcc405000dfd9c623e918fff4567b93a6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db00c36939112adc80c3cb0e0a75b1fe3d4667f7341636339e29b85e1dfebe8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d34bb084dd5a2b55b1062599bfcda75528e7c0625acd8f156f4f5ffd1ade0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5166eb8481f18814545e400bdb46aa4a0657e8130c0fbf52b1a26602851d0341(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb731f1611501cb75ae011b439d885aa025b4ab02fec09b62481cd7627c15c3f(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f36861fe4748713aa281c737a87471764812608e5450b42b7a4a865efe22249(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddda31674a3e9aef7f07239fe8117c75a25773e37565b77a0dbb98161236c317(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1cb2c81ede405dfd2aabfb5e2d4c9888b45142f367ee5d9e6671a628b11252(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d1572ca26d1a9af930e5bb8a251e9904aa5703864d0d6e5c5c2d6e14039dcc5(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627ed0dc2a9611ba6d44e1a48f2ff7778e3ab115021001e3f80280f598ffa48a(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d8c14b7b20201fb4f503e25b9283a06744905a58f1f782fb7f2e9b4fe43f6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4799e3a62bc455f1430e06141af624ef653631733ce3b0718f0514da07c0a983(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8734062f22feb391b9ad0835c1ca05e338c39ea1782875527f1f7bc6f986f17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d965abf9235807402f4e54cf79b8cb163c70f4ec5e607aa2409de0fe99ec884(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dadf28f314d6b7c97b6dbc920cd9ceb78de0be64d6ff7a024b49da5a58ca126(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f66a4c53364f0179a8b587923b57d125476f24d693a37975e92e3e0084e6c28(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18477a6158b79197fd057dd92b6000548f034e61f3b0aa5f0d77314f16fc28b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e15856f77a9db9f53f46df5bbe02191024faa4637815401b837dab558ee7fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27819e7fcab0e9c2bf3374544b3d15f5e8e4162b3e24a28f285767edccc84c8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a70eab086943c52a395df24edd7936061c7a61ee1bbc26e73fb33130d5f419(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66dd4d0b28692f2c81901f2e201d03585eeed074c54580a982456cf3d33530b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2bfe2dc2ed33072df48e92f23482fd8b89ac6590a3212c0501f3df501b9a1a6(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3795aa607c7590d8d5a19a0ea93fa32c3addce07c9b516a3f173ac579adab9f7(
    *,
    interpreter: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile, typing.Dict[builtins.str, typing.Any]]] = None,
    output_file_path: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93fd0995fcd0e4db2c3544430b133a4ba0f18bf665f624b1b0281bc1279982f(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f692643460553138ec66b40dc38bcc7061ad2a059123ebe927b003c3eff2db1e(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787a0c0499a24d827455028db4943a5b86fffa29248fad2ba38986451ab02534(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9017eb38fd391c624976c971f2b3e8060ca3b64ea1ab388dd91f015c9d4d9c39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e683ed32703870055ec68a2cf6a01674df8422f19f62dd821b765f3ce52fbef1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf0278bd30d8ed379393129ee5c2108d3d06f45dfaff24075bc8198e70d0eb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861939b1622ce8b2cf53ed17526553ec626b11704e0a6c275293076c33fb59b1(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ecbb061552d9c1b448f334d6ae00e6e3223516794f54d0c1a6886ecab4acab3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6455a49ddcdea6c94264f87d69b71e31b3564cc0b0ebc75dd0dda54a8b0b9da8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f0a10c801a6529c3ec2f291598f3e47263c76f09624a117bd5f64476821655(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652178ef9cf712032dedec10f5cc3ee8c14182bb83c519e33600e7ea7d6c8b12(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f7ad623848ca9e9334a4c5334776f8321468750348016fa93a3ee91f3bada6(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5dc6a6da7d99297a6ac52a64549d3214ec2c5fcc8ec3d72db562cba900b2dad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0da44cdbaec90767935b78ba9565256a9fe9b3d07f7a661d6347dd5bdc56d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5195905de34ca58448cef2ac7ba6cab9c62275d9b71ba9901feb796e270f3ec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a253d4372d471aeb7a8129d151977e456890d13358475b7b62f3d617828243a(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa78e91d277b90f260247a04695a619c34f4a2792063dbbdb5583b41d8d11fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e430f1cc5da77c9de55d7666fc89aa6930b99c54169cc0c98f4a2912dc1fea05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3bd62fe1ed9f069509e093fc15fe5b67b38ccf485ee11f2ee206dbfb408728(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3436df6437c640a45832f6033d6dae2caf636d6bcea067f28884033dbd91b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2c11f470588455767fd13316571747dba3589295f36ebdb5b1ee0b3a866d4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6298cd722ee15110efd138cb9148d72746be0dc53ad906e374b382769fe57151(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e7ed8745b0e076f84e788989632a23dc3e17e3779d82b0c230030dbfc85954(
    *,
    path: builtins.str,
    state: builtins.str,
    content: typing.Optional[builtins.str] = None,
    file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77eb0cab8ff709f2fa5af9d839330ce5dc66224d20f863fae368dbea5e037ea(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97b97c13de76e054d3e6fc6bbf0667af46ebbffbd6c5dca05473f5068f2adfc(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728c565db7223b13033d0fb2863886dbb3b273c1d458607bc5268b15c866b695(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3b43a422730bc7e18480204bd7bcfeb8103a2af6b7ee9c43324f3996988aff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69a9ef8d9fef1644682d2d531b1dbe92b01c5bc805911bccff11b8b6b5921d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73f52ded4e389886c537ba0d0b63aa11590627762973a5ca3caaa39d0f996b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdef27b3f24d743a1cabb470a0d671cb96f169475306655f1c349db096f71ca9(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bec981037305249a97fb733cd3af936c9c43e7cde3b3032d12d899ac0975377(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35fc9b864e149d4a30dc54b91169eaf64eea01116bfbc1f2a9cec5beba76e131(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb92332bb01106f1a55a7b10e7221af7f122fb80ee2572fc394258c6561c637(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1baaa16944f38c009b23ca5532c7ba9d2789ce7f012d7f6dcc6db2176dd79b69(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caacc2bd56c27b3179415d11e4d2d2873bf5288c109cf1e34e4e2ce916a4691b(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb5a7304dfdc3177b707331dac13ffb56b00d5b8a0f49475be65d1a99c44701(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8352a579550f8fcff80d70244a899f98cfdbc986deb99fd87fb9dacefac6875a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b27017ca6de4b822a5855305a18135f378bfa8f25ae1a45a5b4f36e9bba281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29f579886eee694c39b97a3af957d74186913d1812d7ef7b2fed35956e3b177(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0243a022d166571aeb511687413c1a5f22a70813c1b362aa88f79e6d75b11ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50948df5d6dcca4338f01236cedaf7b86eb4c0f239441fd3c4cf4fb50543f084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a35981339f4973f98fd267da33e38ee564e46871fabd855da044c70fd7f20e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6040163821e9882d827e6928e87307e30c042874437fc84fe2d1355b4850a6e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999b8853960351c80036e8a66d07033e5123a5a77d6213ca48048e974973ac45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe778fe70644bea5a3cef18bfdb6a5f5c23127328d25374a8715dc330d1f6c27(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0540593a59cb3aabd5206bcc066204d5f1f246a5120856bb693230d6ed767a9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5929750940ce043c3bcca7f6660c52d95045e93a9decd7886329f20b6659768c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb4af5ce400a9563dc053afb2dc878bd3c11b454f766812898978ce63c9e0c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19cb57e049b8c4aadb16c67e4e213136a536006016bc1cb51c7f889327d23b0a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0412061acca854649e77c9d89fb96dbab4c4fbe105d8d85d294aa45cef8bc1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e1e974431137f45d9aecee19e6586ea7bbe5c801548dea2c526680c249a0da(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be1b2f145b043b62e866c1145b178be1b7a6b0effb95a4bd6d7491d035435e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2b3f4130f095801c399f6e7ccef90ec23386bfd8827c7cd860fbacb4f60cd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2303b5910208d7787ac2c2daa415954ba32eda9270482c6f092bb0079a59ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3467a668f94ac3c802aadc91e8b4145057081f3ed077a5fdf1c31e309943b37a(
    *,
    desired_state: builtins.str,
    apt: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt, typing.Dict[builtins.str, typing.Any]]] = None,
    deb: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb, typing.Dict[builtins.str, typing.Any]]] = None,
    googet: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget, typing.Dict[builtins.str, typing.Any]]] = None,
    msi: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi, typing.Dict[builtins.str, typing.Any]]] = None,
    rpm: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm, typing.Dict[builtins.str, typing.Any]]] = None,
    yum: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum, typing.Dict[builtins.str, typing.Any]]] = None,
    zypper: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19fa0e39c3c66f3c6a0c55391ec114922be0598848c6c1edeb1794fbad2f3f4d(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331f57f854ddd4bb5f455c8c0cc57ecbadb8445696fcb9049e5c23b30e53c172(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8c59315ed2d71edb753d030a17ad7f0dee1104ef3bfc84efa588ab810752c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095017f29bb15df89c754043a5857f680ae9f34bacc22ee004d811ce201f76c7(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51245c6ea358db3a62f170ae8987898d793ea02af79d5cf840149cdb4344fc1a(
    *,
    source: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource, typing.Dict[builtins.str, typing.Any]],
    pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696461ad069564f3310bedbc28eacc82f7d696f759dcb3309b889837a20ae0c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c01343c77f38fab27ab934f178f926894c85088b86c2f1e6e38d00bb502b1c3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ac8c2ff417b09627432fb190a7ef5a2dcd9e314a3e073e691ecb5cc71edeb7(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42fe650fabe4a4829151a9098b31591c229162eeede2fd275afff04129078e3f(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d83f3b5511ae15a6512e719cf1a5ea09b42d7cad769cfa754c8aa871451de0(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf667582db3a22d1216bf792eda95ea324c6abd1e57dbf4ae16c4d987ea1fb08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264a5c2e29179b24d8cb6d79fd57ea1ed1d1f7bf6012a0620601ade68abc8b94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6223dec4599ac85930c143ab928331be546c403584abdecca72c63424607837d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0478113683b33fff60cdc2f964a7127bb93c32a1a6d24dd3e2e4aea29de0e418(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c582eab541a5fce425f3fb7ec41b23e6315ee89809711ec865740430a6e6ed0(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c231d6f34c69d00c2e1ef2c82122012cc9390d847771f39299cddf434a4ee34c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447f89c768afba640844b65bcfca4626560e9909eb9bf4fde873dca554571dae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e878369c1b4b7b9a86c4161da7e63af3eeb5b6b82b882a632d34aeed73fe53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fe5f1478b7393fb67307a86a9c8bb4b98a8d51e98093fd35f3a8c9b8f7e65f(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865b297a2bfe7f6ac8391bcb311e50c86bf1372f1c7ac84d36d029d5391872fa(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5918ebebda77aedda136fa95dfa1db3ae0a0299a0c93e45783843ae67ce42f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eef4004338264bd91879fd911607a6122904e1c2c53643f2c9e8cd72769b45b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e371d9fc241508f9fb365a283a6f441f01ee33eb4fa923d28f916bab38d72620(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056bf3f2ce12072c0a281decccfc63ba68d8e0ddf82aeda8db94d8a7c5414fd1(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ccc3ddaa7a65657f2ccc317fbd762e86ef1ae3994e18d13d6e44a30fb64e17e(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5d5ba557f95928b761ae6edbf7e011e44ba823001020b2f6a212284dd07d81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98764a81f33f370df519173d2acde1bd6a607349060f5ad052ab7274d007d15d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb4f3b9b5b30c9f9217fb6033e059de147ea73d41175fc47efe5f128442483c6(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b990880e0292f5df7fb9870bf0dc49307f6e418e3f3b706bc173232f3049bd(
    *,
    source: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource, typing.Dict[builtins.str, typing.Any]],
    properties: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54060760f305cfb4b1473635ad74a03df05c5256362e54b5da50a8e7124207d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2832f0d1f56142e1c03cb06154f0706cb58216c47b969b31e183c3d841c7036(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c2a7522ddd5ad738bebe0e0a574257ccdc93122964ff8974413404ceed73ec(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9853023bbede6f01d45a4b7198a2737bfd4de47523a14fa9a3753a2332b4ae12(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9695a59f5a4265247e9301f0fdc85c9d8c1bb36b439632712cdf501a72500cb(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9200a50b5d8c30a039c423671645dc1c9369601c47a3ba49e0dbd392f7014d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196ab7423d1d48eb625013ad0a6ab1ad5ee4d5b986b8995c993540e0e4cefd45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8d3888a1e9da3bde5c8c04104aa4f42940b164afe246ccbbe6af7654d2b157(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76eb04ac7730e29c4615c6a104d0761c42fa5f187e8cadb91a8fc5d24a48a15e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0b044fb8d172a0aafaf1196e3ee467a2c1ae3462f0d4e14607d3b6dd28df74(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f4b733aa48b245e30749b2408d3587ee1562748c040d48c86991757e7a8339(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459df3755d5ef75af29cf00ca96cd42483e1aa86688869abb4db71cd0dc2ad0f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__277d254563764aafb43ed59ed6615343be35a8f6e893d2b0c1d51e6ca6787129(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f941e940126318b48ad64ada41407d9f4519a95ff8654c10edd315d6e56dd7(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9101e8146887972807f3f09dd5c07aeb58245c77d54128f8ecc37eedc41f9394(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f5bd5814327a70dd1260269843006b99315fa9330018e4c3cdc573b4ecd57c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3e0dedd7031cacc1b7be74c1cca95701959d11033822e61fd802cfaeab1fce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644a8e346ec3b32641fd2a3566308f41203da4bb6be582e1c0425fcd1bfb28f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09cf91a9a308f34c299778772e3705bbc7ea13f585e3bf24c2186688a8b58622(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3875752f6e0eeed9700ffbb2db0a46c246fe4ae6badbd9cfd9feeb7865d317(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab044a9a41106ec5906a892cd10e78266e40171814be7718051887057d50c728(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d041b4f0f8ff85edab7d531d2f5bf08e20b611c8e2dd7fc4a938556b848c1fba(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17350bbf58a1e593a53259318c53ff3f7ac7c1b7d33e3d8cfab8d0d219f0a0ac(
    *,
    source: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource, typing.Dict[builtins.str, typing.Any]],
    pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ebd415ebf5eecbedc10da7370e3aae68ad7d1d0b21c634332289a564631e038(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc41de812fd3eedb4d5970b908100abe9968e653ab9f1c3b5befd52ce2e9967e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0851bcb140ef17f2a09a7040a06aa3032bce6dfcac01dbc1b84825108c9a2610(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7673e2961b10a933142e202b5e26df968252e3246377f85ba61ed94f9c67def8(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b33e3610503f6dfe89f8adbf8170fe34ea208f0e02c51eaf709cd2635febd7a(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6925dfc550461a73937a018e8178cf73ff43dff31c32cc3c1d26489cd0af8f93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa44db912607e8180c831031091855eace590d49f8601e51cd04a0701ef3c9a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd274bddf82ce54393472b75cbfc0be3a93340bd657da99ff851b4d8a1494b69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688e185435ee2a5308f0eb9c11eb79fbe126da574634a128f3af3bf1231a9a91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62393ae93b81cf7a95f160a912f2cb17e88ade8cf9958a1018eb7a8c97076f08(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d25ee5194c3151b55fd804b1f74418c8dd930f15b68bb1b1e1f4c4674bd4da5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8cfdb3a36a3e13f46dc0879d53f4a260f830456d2c5a7c4218beb8f37dcf3c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390ac98ebbbadac5e678b432aaf32229f58c4e486d1b08930db5a497282a2e58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd68a35f1ed2fea3db659e3ab770c847f662880c43b9bf29f0aef26e712939a(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5e71effd2f19a8d50b14e330c8af2a4060ab752c3a810eb7e85ea10341f6a8(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb4664658e8ddc2b9c7be2f2bec6f9b80132ee44549771d28d5fb6cc5d4c32b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd82a79f07eed30c403510010ca2c79459633fbd71c10e1afef35924e7bb0de3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b701d3479433a750049ad107ed1bd9368e8574fbbe99eff1efd835335b2c8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91142acf715a20129d73e70d7d5c59209801bcf7dd55046d961fa9e3f12f324(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c33c71fdc81b5562d2659ea58ad9cf8312b73353b204026480597c1e20915b(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ac11299752e9cdd1314a2eba1db7eb00bff3251cf948dcb4dc4bdb76ebc644(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e803d56459af6e0c11378dcd7e771d91cd11869d3b4d3b9893ed3bbf247352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae3ebc3882c63c9d9867a7c2b4146de65e8e01516a9782600ee5949ba4a9f6f(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d533bb1504dfb14e998e26b8e0e690c2b5e70fe45953b597a893f6f93538d76c(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c7f7e30d18a46a52ef4280704e8715b431449d63cfc45746ccefdfc9994f89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52a9d672a90f3c5e570411ccf726b587746e968d034f891fb515c5558f9afcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5dbd361a7d6fa238a27f63ab4d434b6b0f04fb47016ebddd8c132ef43bcbf7(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b4b5e3e8470f94a4c568d51da2ca9fdca032fd32bf3d452bb2525cd5abc0e5(
    *,
    apt: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt, typing.Dict[builtins.str, typing.Any]]] = None,
    goo: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo, typing.Dict[builtins.str, typing.Any]]] = None,
    yum: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum, typing.Dict[builtins.str, typing.Any]]] = None,
    zypper: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d627d29fbd4ac3fe89499d3a76c353e1db601cd27ce3f519baaa63667141688(
    *,
    archive_type: builtins.str,
    components: typing.Sequence[builtins.str],
    distribution: builtins.str,
    uri: builtins.str,
    gpg_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f9b5ea63e31fddbef63f03e3cfa284963b19f8e0e30108b2a84305454b0455(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f49e1fdcb907cf1abae485b8c3032806d1b9d70d5267dd4f36426693f3dbd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9175a234a9f1a1dafeef4dabcd5701189e449a7c38e6be49920eb36b85eeb4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2991804b855e31fe5422b6126bfafb87348bd2636e667c3e8efe04b4b96be4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5256a87d54af28988157cb320d3eee92f8168bbab4fce06826cc662065ccbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c384d7f3f0cf8e3c79db1b109d867ff4cc383b1d616fbdae76f3c799072e7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d973c8bf5386bc429aadb6df07d9d3f7c82e5425c389999392c9fdb93955d6(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1d87ad292a9786f8d57e0866a82e7a4ecbeb1b31750543469a1eb6cf69eeb7(
    *,
    name: builtins.str,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1404fcaf81922adc287da050cfda92aef889d7e57bb63eeeb8a4ccc8860df4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8dc8dc6a9612e1a7485d1b235aa92c1cbb71ca7b167845d6d00e8624ec5ebb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff40650d090b6fc0a34167fcaf84205ad74dbeedffbf8a5d26c47a383ad987a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679bd816a9da40fd3265fc11aec9310e8de6d1c947cd166e02d116eed06dfcc3(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240862915d49ebf7bb365a0d933d66c2f115f53bcb6e2c5ea47b7ffad5609525(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0203ddbc78c047f23f948938571a9ad1dd0de34be70f78084c367f5710987d8(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0ee4b514fcc597c561302c85997d3c2cb35b6d4ccc6193c78e84dc002ae06a(
    *,
    base_url: builtins.str,
    id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb56458f77fe7aad0142164372791cf49a28969e3a23e64932ec09ba8e19773(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887cc3a6bd4786fb80cb7475c1655069cf6bbeee450afabf0ecce3f78776c810(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54029686aed74d2560fcd4486920716c7707b9005506d370cede487e65a205de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77309b5699d111b07e22fb79ab529881f96e22fd81a97c2360b821b61f2e5cf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afc3fc46a11f99e3334df02294453a2c1ededdc3254dccb17384e88ae8d6e91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9101c1ecf049bf4f3cc65d9aa4b27b0d02dcf8acb95e130a6cc0e286bc6a2b(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad197deed9e6ac7a9ca590542646a58c448a060296582a6c0ffa5cfab4b6cc3(
    *,
    base_url: builtins.str,
    id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f333adfd824d4e48df4ab54aba9929011ffb66d922bca257fa3325613cdebc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f14785cd4123ecf438661f87dbb198e3d09a75e4f5332a28585e225a0dce5b0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e727f7a8b4e377a4bf85dd6f40c4da1d085b0a52c3b58f752aa071f2b3615f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13dc0930489a9005066d9308ed3a7a9ef5895046b82628b17a29fdc266720359(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e80dab66f407989ce893fa6de45eb120c1753031932451a7385c3aed702591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d63a7b0471f32f55a02be011012a9fa6bb0c9ad65c6ef1ad67a5e4a8a5221e5(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5836ea110fcfee11e0051a136e24d880b21a2bfa70f4c3d63c81421c2491ff6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8cb37be65d6be8e9c850b59e4817c9a68d48d84f12aa21e842aeef7fc72a0dc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eadbfc5cbd2c7e5645552ffcda8a68c155bb5f171b7a3f6b59f32a10f9d44df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d0b07507b3a7aa24f0f005a40c99dbc7b68b4236801e89d5d71b11c5076450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e105e76fa460adcedb947151cf9214fb4eec94374d81a9cd621382c425cecab9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16bb31d944c00a8161d004bb8f122cffcf78493dfde929f8eb0dd382d19a352b(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1Payload],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4073396de18ef4709dc34bbd8b0cc6eeacd50e906489c7973bf046a2dc6a3af9(
    *,
    disruption_budget: typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget, typing.Dict[builtins.str, typing.Any]],
    min_wait_duration: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d37cd84a1d0d3d3695b504459f1944a69334ec60c007bdb7bfd5496b0d94bac(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e99b0bb63bdf496c924f6661447c28d2603e95682edcb1c51a73b6b7fb4151f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163a8532af351245659620d6358785628391665ce04e847f483b6c70275fc12e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69a8b8f27ec7654f57fc9a4157da5b5165a1f255909602d9e9f78830101b1cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574fc682247b3f4d303588db8fd0b95670f930f05fe613c2b0c72ab36146a682(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64306960c0999515423945ba23be9bad24dd799a158b303df08fc61fa773646e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e2f72eb4fb47eed2b0849bb39c94735d1c63e34cff14b1bb4d7d4db2450035(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c74060fd6106b6bf46dd15e1ec20a567544d1826d63dca491fdd8788c2feb1(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResourceOsPolicyAssignmentV1PayloadRollout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e428082ff3b57a488e4b3893bc8d2b57e923a15c0c96d137fb331f5f374d8cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0b211b575ecc67f3735285603f8e028a2cbee04aa9f34e96c75e4c65fedf86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6726b383f943f9f8ecc11aeecac84ff48490769637be91f6233c566df9dc0a63(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestratedResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c131c5490836949a22ea4c1b7bf74470dc1409ac38f4fe5914d27c9671b68df(
    *,
    selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__708a9037cd7c7d4fc035dbd5f174a24774dda63c862cb6e2dc6927c078f58da1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd821dfa8f50e287bd4cba548e2a3f246db1b88342b7c0ed67442919088170b7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf7b43ff4abe4951128025a37693fb112957696aa9109bab9f6f9ba20f7774f(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b35f6d2dac0c86cf51068a864fa143eaa585f4b54aa01be65e6a32c20a3e2a(
    *,
    location_selector: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_hierarchy_selector: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8fb320fe067e33359c10d5661d17919ff505e465ad923a3e826a51b8a931186(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef70baa62f0358d8130a1a6b8497d898544e1251efa392cd2fdd2f6f003a5c5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ab3af52a645e5294093d54bafc5d34e95100347aabf3dcb1560f6f069ad108(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7293808435973a5523dc945b8e9d716b1bcb62f80739da67e37a08a90b605bb0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1234a92abb939b1711181940e97b07e00c88a2c54cbda60eb6bfbfe615a99f1c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796eb1b0da50a1c2d91eff3b4db5feb6a26cae4fdfd81a105b9624a66f24db86(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79020a4af42e8e04c584cb6a1bb0e9ba9857407d11d27346d76d290bc83b19a(
    *,
    included_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c128559712bd21a322dc24e9dc58bc5b271e3c5043447569a73d8b9d729c611(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e77381c4565ccddf1118a18b5f06a6c74ac95ee49c4df03fa6c4ae3de4aa3e5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f797e339b0c32a6860d481e87849a222483a2bb5bf8fbc3f5495c79534696d87(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsLocationSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b4414bf3679a7cc4d16181321a26ae8ca9bdfa199384ffff8dd0a2edc940ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02aa378e1d1adf1173cc06cac8e07db3dc4c31553fc6e997bc10eda9516ef310(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12fc48a501f33f0a17e146b4565e0fe5d8d5b18cbb0e861c685b5acce22324b9(
    *,
    included_folders: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41d3be48776b8b5bcef0d7555ebcfee5281bdc95b8efe5b0a057929970bf6dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef983df57749477c2edcc6039e054c653762e2361715cd6274d38aaaed336b77(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51ae3927b3e178a8765b4b18b96756913e6e138f825b64a9a6a0d26715dd263(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e043fb9b19e4f6247efaaeb98eb960a6ae91b89a1052531cb477065a8d1dbf(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationScopeSelectorsResourceHierarchySelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e769430dd6c13e15d1eedcc9e9db90c3d587d7213d368fc9523b3d008697d32c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e83050cc3e9564e76537be9b66b945d27bb8431dfb4a59c8b5ef6939418cdf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6432c196d197c3054e67faeb65eb69e2934176c81ee9a2cf09d99b1402e29daa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d7faea3f60c021858a64256fdbf026a44f8b53fd580c0ef49a13f0a73a0e40(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aaa70b1f4d3797c0f0eee3da1615390905198492e0aef7e55a876d48839983c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42998e5d5c717744595f14c9cbc7354895bfeacf245f49bf8d8b25eea90f9afd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9e6ce7d448bccfdd470a7e022a582c30c440f0bdcbba035704ba03c014e690(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateErrorDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3738e1d16d62eecf616b079977ce45e9fc38258bdfa7a04af69dbc7830fb9356(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dacf65a58cc158c76ae0fcada3d4926fda39aa8f4ac7293fd48c92173f5d4798(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8271555e0972079cab2fde67987e228e4048fb246a4e31079ba753f8283fc819(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf393cd58ba26c638e37f2a4ffae1d78588fa148e3b2cc3c04a671c5fb8c9d59(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e5412ae8a0a3510c1d939fdfe37f8789e47101e6877d671de41e0156fab6fe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf68445d7dba236ed963982d3895a8bd0dc2fbb7f465597dcf8081a172c44e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ae00ca6bad3842a0c79b6e22e359468b8e3627fbf5134f0337e9b380f06af9(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationStateError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab6e614ae7ec62746224d0bac8d66f8db91e0f73e01a14337d0a467eb3e4ac6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834339f36b1d24359301837af4aeb766cd5b1107bf8282c2f2444be30bf74cee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ce7eb3e1f84bb7d97ecfa1f1018f7127a1ad3e8278868b4b8c7010466178d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06bdea621d1bbcabba6fcb8d81a9bf02719252b9d87dea733c421bd6991db09(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c5483c4b32afdb2516f07f814cb05839ab3c2fa9ea6e6cb43a336dd85c69e9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe19e5bfa5752501a4024b7ffe03df5a9a208c06b4f3c6740f93dc4dc4bd810(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118b4b1901d3a8d31695d8e4f44ea747b18ceb9866e26d83922cff63c4ebf857(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStateCurrentIterationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8204a84a23216a4e9004d71e721f55b670f9c9c264cf1b9f426133e2b63d58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66fae2875f668f37a1e07850575148a1b2b026456227b24a3cc289503ac7670c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a125a73d4543aec320e5a0c04a0335d68b6b7f81538a5f782d04e1940f33cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbcf0531a4fe1e2a8492b3b1b062ce63d99320e12e55a61d554fa779cac6e638(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d32cd3698e0dd44b7b74b3a16a1c3018794f3d1ba065d2354fa110a14f58b50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64361503f5f20621f2c804955dd15270fa500e7adb419d7855a642223839cce6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415e06fb6883f3bd129a7b657c1eb99a7fe7bc9f629e90fe3570eba08ecf92fd(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ceaf44a96649c026b9317de66a58ac1237e5c9ccc09e92ff59c260467a8607(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e9b423af7777daf114b093b5297d2cdb5df3869a8e58ac93496cdbf70878a4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38489c29d35f9cf8d145fe1c1ad12a0d657d01141b994d2b26126efe3feba8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e52031c65877826726b227789e22bf43b11baa2a47d8dec9d14f52cc5c72024(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941e1f08cc672b9e972ecbb1f6f72a19162992652f7a999510f629bbb696e2fd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc624cc409f63a581cd8f108e7e49bfcb3e28ca2086f81599e58e8293125faff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55feefadb7551a57ea4271e03ee40091fa02c644735729dc7393888953fcd7e4(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateErrorDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba71cd8662881628e9ce10ebb94adf1e7541086f45ab2f5c1aba5f66e053672c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee66f192e3c9efeb15fc8c6c31543a8214924089efada5248b5e603a6957f527(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c176356df7de35be31a108127b5d6a332f02b5fac51a218cf058b4d6e9dca4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab1968be1ff3498a468889741db45d777e4e31d5c0ecef1db84135c5b5a63ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8436bd629899ec20677caf88c9cab44973fcf7e67088a8832f5213199fb2e69b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__322ba0955d6def42a188be0e260e593d88c5ba4d390646c003fb9dc9ca47325b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c1c8450a776a74d18e854519b6ff993da1e61ac9139e1bd41edb6c07eafdd6(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationStateError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1242be5046f62539cca792017b77370dc006498e1e724749d39d554a8714516(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a8e3c87daaef291eb0b9622bce8ffbd1b912cc487eab5219e4f35555960a2b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a4b6df859bfa6a3a171b10f93ffc4a1a65a29e4c8d0b6f76c6ca5787e6e447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc18e9038abdf4fd2b3cc2763ca1dd78cf487a12a8f15b69cc8cea48947aab3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757314a8ec7c6f1085ab54a024d1a0654eefa7422387b8f8ab4730aed4edcd0f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9145f5f74b6721df0d304e181eeddb4c33e9a8d2594d06503f24eb501d412b4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf7d9ea90affce302d25bae14467f9d86aa0160f30a524a8b252c0abc3a7f34(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForOrganizationOrchestrationStatePreviousIterationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d10acec3856fbbf156b5958f08bb24d76ba3c371d919ea01c44b645437de154(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b22ef496237773a4eb541a7fde6e68521e8a0e4e80d06edc96cbfdcf872a3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f433a59901742ccedcf61518c15b58e252119e4bcc8bd84209599b0e7d819b8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d541494b1b752f387ba1cdd522efd26b63e66082a5ad12c8414cb7ef9e9aa0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb4e82fc41f91d33dca4b644afff50e04b71bea74baead550e6c2d31c6d14de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ac08c9664a510f2946e5164740f5cdb1b5ba9135c2b61f7bd63c31969596db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForOrganizationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
