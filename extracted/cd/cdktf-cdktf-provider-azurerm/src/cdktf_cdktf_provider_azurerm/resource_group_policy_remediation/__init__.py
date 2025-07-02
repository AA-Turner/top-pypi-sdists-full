r'''
# `azurerm_resource_group_policy_remediation`

Refer to the Terraform Registry for docs: [`azurerm_resource_group_policy_remediation`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation).
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


class ResourceGroupPolicyRemediation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceGroupPolicyRemediation.ResourceGroupPolicyRemediation",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation azurerm_resource_group_policy_remediation}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        policy_assignment_id: builtins.str,
        resource_group_id: builtins.str,
        failure_percentage: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        location_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        parallel_deployments: typing.Optional[jsii.Number] = None,
        policy_definition_reference_id: typing.Optional[builtins.str] = None,
        resource_count: typing.Optional[jsii.Number] = None,
        resource_discovery_mode: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ResourceGroupPolicyRemediationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation azurerm_resource_group_policy_remediation} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#name ResourceGroupPolicyRemediation#name}.
        :param policy_assignment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#policy_assignment_id ResourceGroupPolicyRemediation#policy_assignment_id}.
        :param resource_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#resource_group_id ResourceGroupPolicyRemediation#resource_group_id}.
        :param failure_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#failure_percentage ResourceGroupPolicyRemediation#failure_percentage}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#id ResourceGroupPolicyRemediation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location_filters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#location_filters ResourceGroupPolicyRemediation#location_filters}.
        :param parallel_deployments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#parallel_deployments ResourceGroupPolicyRemediation#parallel_deployments}.
        :param policy_definition_reference_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#policy_definition_reference_id ResourceGroupPolicyRemediation#policy_definition_reference_id}.
        :param resource_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#resource_count ResourceGroupPolicyRemediation#resource_count}.
        :param resource_discovery_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#resource_discovery_mode ResourceGroupPolicyRemediation#resource_discovery_mode}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#timeouts ResourceGroupPolicyRemediation#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebef8f96a74e83c23d9cc62bc6d86dd88accaf021b98a424201be33a5ba3dc36)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ResourceGroupPolicyRemediationConfig(
            name=name,
            policy_assignment_id=policy_assignment_id,
            resource_group_id=resource_group_id,
            failure_percentage=failure_percentage,
            id=id,
            location_filters=location_filters,
            parallel_deployments=parallel_deployments,
            policy_definition_reference_id=policy_definition_reference_id,
            resource_count=resource_count,
            resource_discovery_mode=resource_discovery_mode,
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
        '''Generates CDKTF code for importing a ResourceGroupPolicyRemediation resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ResourceGroupPolicyRemediation to import.
        :param import_from_id: The id of the existing ResourceGroupPolicyRemediation that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ResourceGroupPolicyRemediation to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e54d1cddd26c51d3facd9368cb7bb9ec05c1aba7e7195e8c120ce4f1b0603e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#create ResourceGroupPolicyRemediation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#delete ResourceGroupPolicyRemediation#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#read ResourceGroupPolicyRemediation#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#update ResourceGroupPolicyRemediation#update}.
        '''
        value = ResourceGroupPolicyRemediationTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetFailurePercentage")
    def reset_failure_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailurePercentage", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocationFilters")
    def reset_location_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationFilters", []))

    @jsii.member(jsii_name="resetParallelDeployments")
    def reset_parallel_deployments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelDeployments", []))

    @jsii.member(jsii_name="resetPolicyDefinitionReferenceId")
    def reset_policy_definition_reference_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyDefinitionReferenceId", []))

    @jsii.member(jsii_name="resetResourceCount")
    def reset_resource_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceCount", []))

    @jsii.member(jsii_name="resetResourceDiscoveryMode")
    def reset_resource_discovery_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceDiscoveryMode", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ResourceGroupPolicyRemediationTimeoutsOutputReference":
        return typing.cast("ResourceGroupPolicyRemediationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="failurePercentageInput")
    def failure_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failurePercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationFiltersInput")
    def location_filters_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelDeploymentsInput")
    def parallel_deployments_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelDeploymentsInput"))

    @builtins.property
    @jsii.member(jsii_name="policyAssignmentIdInput")
    def policy_assignment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyAssignmentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="policyDefinitionReferenceIdInput")
    def policy_definition_reference_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDefinitionReferenceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceCountInput")
    def resource_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "resourceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceDiscoveryModeInput")
    def resource_discovery_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceDiscoveryModeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupIdInput")
    def resource_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ResourceGroupPolicyRemediationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ResourceGroupPolicyRemediationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="failurePercentage")
    def failure_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failurePercentage"))

    @failure_percentage.setter
    def failure_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11971293a2756cf4263edb4eeee3a32bd72ab791246914a3f13812a8f2e8334b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failurePercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604dc65dfcd4529aa3821004599c0b229b8cc13cf6486c9ce322c19b72ed9779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locationFilters")
    def location_filters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locationFilters"))

    @location_filters.setter
    def location_filters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d423c7b60007ba7e7309dc5b3b18246c65dfa1324e18a41508e978ae759db5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationFilters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__629d526bf9ba7a6a1282a4381b12fbdb6cac1b1870cca11d2b3052b3e05a4b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelDeployments")
    def parallel_deployments(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelDeployments"))

    @parallel_deployments.setter
    def parallel_deployments(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2310fc46cc25449c23603e5387f283dda27711b2ec36bf65c33ac2613a441247)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelDeployments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyAssignmentId")
    def policy_assignment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyAssignmentId"))

    @policy_assignment_id.setter
    def policy_assignment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e912ce64e8eb5cf0fe6838bd2c617aa7158cdc0a4e7fbd53f51d63e3d0c74363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyAssignmentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyDefinitionReferenceId")
    def policy_definition_reference_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDefinitionReferenceId"))

    @policy_definition_reference_id.setter
    def policy_definition_reference_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96b20b39bc27905764762371cc38af0537ed1aba5f5d34c20b8fd570614ca45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDefinitionReferenceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceCount")
    def resource_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "resourceCount"))

    @resource_count.setter
    def resource_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a7360720cb28cf9e1e6c93dc5ad82f1017376ea2b4a8842d30a4704e6c4c74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceDiscoveryMode")
    def resource_discovery_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceDiscoveryMode"))

    @resource_discovery_mode.setter
    def resource_discovery_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec15d9ce326edba827722806fc1382320bec7c167d5965a2e6a2ce17f8a22a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceDiscoveryMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupId")
    def resource_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupId"))

    @resource_group_id.setter
    def resource_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f2dd1f539424567583875bdc7a7737dd3861216e3b075abd47da4d0805939a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceGroupPolicyRemediation.ResourceGroupPolicyRemediationConfig",
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
        "policy_assignment_id": "policyAssignmentId",
        "resource_group_id": "resourceGroupId",
        "failure_percentage": "failurePercentage",
        "id": "id",
        "location_filters": "locationFilters",
        "parallel_deployments": "parallelDeployments",
        "policy_definition_reference_id": "policyDefinitionReferenceId",
        "resource_count": "resourceCount",
        "resource_discovery_mode": "resourceDiscoveryMode",
        "timeouts": "timeouts",
    },
)
class ResourceGroupPolicyRemediationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        policy_assignment_id: builtins.str,
        resource_group_id: builtins.str,
        failure_percentage: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        location_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        parallel_deployments: typing.Optional[jsii.Number] = None,
        policy_definition_reference_id: typing.Optional[builtins.str] = None,
        resource_count: typing.Optional[jsii.Number] = None,
        resource_discovery_mode: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ResourceGroupPolicyRemediationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#name ResourceGroupPolicyRemediation#name}.
        :param policy_assignment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#policy_assignment_id ResourceGroupPolicyRemediation#policy_assignment_id}.
        :param resource_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#resource_group_id ResourceGroupPolicyRemediation#resource_group_id}.
        :param failure_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#failure_percentage ResourceGroupPolicyRemediation#failure_percentage}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#id ResourceGroupPolicyRemediation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param location_filters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#location_filters ResourceGroupPolicyRemediation#location_filters}.
        :param parallel_deployments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#parallel_deployments ResourceGroupPolicyRemediation#parallel_deployments}.
        :param policy_definition_reference_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#policy_definition_reference_id ResourceGroupPolicyRemediation#policy_definition_reference_id}.
        :param resource_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#resource_count ResourceGroupPolicyRemediation#resource_count}.
        :param resource_discovery_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#resource_discovery_mode ResourceGroupPolicyRemediation#resource_discovery_mode}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#timeouts ResourceGroupPolicyRemediation#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ResourceGroupPolicyRemediationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b63aee0b02eb1e1747f1e39161b133aea7dfb3a069b6db46d8ddb845a91024)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy_assignment_id", value=policy_assignment_id, expected_type=type_hints["policy_assignment_id"])
            check_type(argname="argument resource_group_id", value=resource_group_id, expected_type=type_hints["resource_group_id"])
            check_type(argname="argument failure_percentage", value=failure_percentage, expected_type=type_hints["failure_percentage"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument location_filters", value=location_filters, expected_type=type_hints["location_filters"])
            check_type(argname="argument parallel_deployments", value=parallel_deployments, expected_type=type_hints["parallel_deployments"])
            check_type(argname="argument policy_definition_reference_id", value=policy_definition_reference_id, expected_type=type_hints["policy_definition_reference_id"])
            check_type(argname="argument resource_count", value=resource_count, expected_type=type_hints["resource_count"])
            check_type(argname="argument resource_discovery_mode", value=resource_discovery_mode, expected_type=type_hints["resource_discovery_mode"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "policy_assignment_id": policy_assignment_id,
            "resource_group_id": resource_group_id,
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
        if failure_percentage is not None:
            self._values["failure_percentage"] = failure_percentage
        if id is not None:
            self._values["id"] = id
        if location_filters is not None:
            self._values["location_filters"] = location_filters
        if parallel_deployments is not None:
            self._values["parallel_deployments"] = parallel_deployments
        if policy_definition_reference_id is not None:
            self._values["policy_definition_reference_id"] = policy_definition_reference_id
        if resource_count is not None:
            self._values["resource_count"] = resource_count
        if resource_discovery_mode is not None:
            self._values["resource_discovery_mode"] = resource_discovery_mode
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#name ResourceGroupPolicyRemediation#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_assignment_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#policy_assignment_id ResourceGroupPolicyRemediation#policy_assignment_id}.'''
        result = self._values.get("policy_assignment_id")
        assert result is not None, "Required property 'policy_assignment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#resource_group_id ResourceGroupPolicyRemediation#resource_group_id}.'''
        result = self._values.get("resource_group_id")
        assert result is not None, "Required property 'resource_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failure_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#failure_percentage ResourceGroupPolicyRemediation#failure_percentage}.'''
        result = self._values.get("failure_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#id ResourceGroupPolicyRemediation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location_filters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#location_filters ResourceGroupPolicyRemediation#location_filters}.'''
        result = self._values.get("location_filters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parallel_deployments(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#parallel_deployments ResourceGroupPolicyRemediation#parallel_deployments}.'''
        result = self._values.get("parallel_deployments")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def policy_definition_reference_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#policy_definition_reference_id ResourceGroupPolicyRemediation#policy_definition_reference_id}.'''
        result = self._values.get("policy_definition_reference_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#resource_count ResourceGroupPolicyRemediation#resource_count}.'''
        result = self._values.get("resource_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_discovery_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#resource_discovery_mode ResourceGroupPolicyRemediation#resource_discovery_mode}.'''
        result = self._values.get("resource_discovery_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ResourceGroupPolicyRemediationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#timeouts ResourceGroupPolicyRemediation#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ResourceGroupPolicyRemediationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceGroupPolicyRemediationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.resourceGroupPolicyRemediation.ResourceGroupPolicyRemediationTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ResourceGroupPolicyRemediationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#create ResourceGroupPolicyRemediation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#delete ResourceGroupPolicyRemediation#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#read ResourceGroupPolicyRemediation#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#update ResourceGroupPolicyRemediation#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d42319fe5d264080b847e9259185f52a4297b24493335ba6f614f4fc3fac27)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#create ResourceGroupPolicyRemediation#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#delete ResourceGroupPolicyRemediation#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#read ResourceGroupPolicyRemediation#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/resource_group_policy_remediation#update ResourceGroupPolicyRemediation#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceGroupPolicyRemediationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourceGroupPolicyRemediationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.resourceGroupPolicyRemediation.ResourceGroupPolicyRemediationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__223f619f80f53cb542803ae2fad147558f7ece7c4a00f4876f1ff790a306639a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2575e0006dd40b35027e78282be8f616d614654234effbf1b05b393d8b5e6920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556b5492450cbf0b2c685e11dad7a0ac4840f391964d9a7999ed476926ad05e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84b040d6eb78793190b9fcf4393c804489bc2166a46ddc4ff95e1cb10295d89f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d04fecc5c39f0f6b286dc14526b9494dfab52b3ca14499ee2868482d4ae8085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceGroupPolicyRemediationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceGroupPolicyRemediationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceGroupPolicyRemediationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652bf0edd04ba01cc7b864ec7353fc315d2f4eb6cbed67851034d5094d1bf062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ResourceGroupPolicyRemediation",
    "ResourceGroupPolicyRemediationConfig",
    "ResourceGroupPolicyRemediationTimeouts",
    "ResourceGroupPolicyRemediationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ebef8f96a74e83c23d9cc62bc6d86dd88accaf021b98a424201be33a5ba3dc36(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    policy_assignment_id: builtins.str,
    resource_group_id: builtins.str,
    failure_percentage: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    location_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    parallel_deployments: typing.Optional[jsii.Number] = None,
    policy_definition_reference_id: typing.Optional[builtins.str] = None,
    resource_count: typing.Optional[jsii.Number] = None,
    resource_discovery_mode: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ResourceGroupPolicyRemediationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d3e54d1cddd26c51d3facd9368cb7bb9ec05c1aba7e7195e8c120ce4f1b0603e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11971293a2756cf4263edb4eeee3a32bd72ab791246914a3f13812a8f2e8334b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604dc65dfcd4529aa3821004599c0b229b8cc13cf6486c9ce322c19b72ed9779(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d423c7b60007ba7e7309dc5b3b18246c65dfa1324e18a41508e978ae759db5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629d526bf9ba7a6a1282a4381b12fbdb6cac1b1870cca11d2b3052b3e05a4b5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2310fc46cc25449c23603e5387f283dda27711b2ec36bf65c33ac2613a441247(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e912ce64e8eb5cf0fe6838bd2c617aa7158cdc0a4e7fbd53f51d63e3d0c74363(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96b20b39bc27905764762371cc38af0537ed1aba5f5d34c20b8fd570614ca45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a7360720cb28cf9e1e6c93dc5ad82f1017376ea2b4a8842d30a4704e6c4c74(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec15d9ce326edba827722806fc1382320bec7c167d5965a2e6a2ce17f8a22a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f2dd1f539424567583875bdc7a7737dd3861216e3b075abd47da4d0805939a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b63aee0b02eb1e1747f1e39161b133aea7dfb3a069b6db46d8ddb845a91024(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    policy_assignment_id: builtins.str,
    resource_group_id: builtins.str,
    failure_percentage: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    location_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    parallel_deployments: typing.Optional[jsii.Number] = None,
    policy_definition_reference_id: typing.Optional[builtins.str] = None,
    resource_count: typing.Optional[jsii.Number] = None,
    resource_discovery_mode: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ResourceGroupPolicyRemediationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d42319fe5d264080b847e9259185f52a4297b24493335ba6f614f4fc3fac27(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223f619f80f53cb542803ae2fad147558f7ece7c4a00f4876f1ff790a306639a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2575e0006dd40b35027e78282be8f616d614654234effbf1b05b393d8b5e6920(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556b5492450cbf0b2c685e11dad7a0ac4840f391964d9a7999ed476926ad05e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b040d6eb78793190b9fcf4393c804489bc2166a46ddc4ff95e1cb10295d89f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d04fecc5c39f0f6b286dc14526b9494dfab52b3ca14499ee2868482d4ae8085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652bf0edd04ba01cc7b864ec7353fc315d2f4eb6cbed67851034d5094d1bf062(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ResourceGroupPolicyRemediationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
