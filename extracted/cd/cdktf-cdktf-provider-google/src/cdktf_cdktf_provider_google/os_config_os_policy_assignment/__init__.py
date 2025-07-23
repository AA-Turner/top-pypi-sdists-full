r'''
# `google_os_config_os_policy_assignment`

Refer to the Terraform Registry for docs: [`google_os_config_os_policy_assignment`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment).
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


class OsConfigOsPolicyAssignment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment google_os_config_os_policy_assignment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_filter: typing.Union["OsConfigOsPolicyAssignmentInstanceFilter", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentOsPolicies", typing.Dict[builtins.str, typing.Any]]]],
        rollout: typing.Union["OsConfigOsPolicyAssignmentRollout", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        skip_await_rollout: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment google_os_config_os_policy_assignment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#instance_filter OsConfigOsPolicyAssignment#instance_filter}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#location OsConfigOsPolicyAssignment#location}
        :param name: Resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        :param os_policies: os_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#os_policies OsConfigOsPolicyAssignment#os_policies}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#rollout OsConfigOsPolicyAssignment#rollout}
        :param description: OS policy assignment description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#description OsConfigOsPolicyAssignment#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#id OsConfigOsPolicyAssignment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#project OsConfigOsPolicyAssignment#project}
        :param skip_await_rollout: Set to true to skip awaiting rollout during resource creation and update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#skip_await_rollout OsConfigOsPolicyAssignment#skip_await_rollout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#timeouts OsConfigOsPolicyAssignment#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b040bd1a4082f6bf8275131da015e0999e1c2c56c082288ba7c7ef8a47dbb9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OsConfigOsPolicyAssignmentConfig(
            instance_filter=instance_filter,
            location=location,
            name=name,
            os_policies=os_policies,
            rollout=rollout,
            description=description,
            id=id,
            project=project,
            skip_await_rollout=skip_await_rollout,
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
        '''Generates CDKTF code for importing a OsConfigOsPolicyAssignment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OsConfigOsPolicyAssignment to import.
        :param import_from_id: The id of the existing OsConfigOsPolicyAssignment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OsConfigOsPolicyAssignment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac053c3e9ce9b1dbda22907a75a13dd182b8a06b3302097d1337f2f64e1398fc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInstanceFilter")
    def put_instance_filter(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentInstanceFilterInventories", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all: Target all VMs in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#all OsConfigOsPolicyAssignment#all}
        :param exclusion_labels: exclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#exclusion_labels OsConfigOsPolicyAssignment#exclusion_labels}
        :param inclusion_labels: inclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#inclusion_labels OsConfigOsPolicyAssignment#inclusion_labels}
        :param inventories: inventories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#inventories OsConfigOsPolicyAssignment#inventories}
        '''
        value = OsConfigOsPolicyAssignmentInstanceFilter(
            all=all,
            exclusion_labels=exclusion_labels,
            inclusion_labels=inclusion_labels,
            inventories=inventories,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceFilter", [value]))

    @jsii.member(jsii_name="putOsPolicies")
    def put_os_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentOsPolicies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a901d89e3ec383a25bedaa59295941949a1f1b398fac94c3fa5037758fc640e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOsPolicies", [value]))

    @jsii.member(jsii_name="putRollout")
    def put_rollout(
        self,
        *,
        disruption_budget: typing.Union["OsConfigOsPolicyAssignmentRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        min_wait_duration: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#disruption_budget OsConfigOsPolicyAssignment#disruption_budget}
        :param min_wait_duration: This determines the minimum duration of time to wait after the configuration changes are applied through the current rollout. A VM continues to count towards the 'disruption_budget' at least until this duration of time has passed after configuration changes are applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#min_wait_duration OsConfigOsPolicyAssignment#min_wait_duration}
        '''
        value = OsConfigOsPolicyAssignmentRollout(
            disruption_budget=disruption_budget, min_wait_duration=min_wait_duration
        )

        return typing.cast(None, jsii.invoke(self, "putRollout", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#create OsConfigOsPolicyAssignment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#delete OsConfigOsPolicyAssignment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#update OsConfigOsPolicyAssignment#update}.
        '''
        value = OsConfigOsPolicyAssignmentTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSkipAwaitRollout")
    def reset_skip_await_rollout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipAwaitRollout", []))

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
    ) -> "OsConfigOsPolicyAssignmentInstanceFilterOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentInstanceFilterOutputReference", jsii.get(self, "instanceFilter"))

    @builtins.property
    @jsii.member(jsii_name="osPolicies")
    def os_policies(self) -> "OsConfigOsPolicyAssignmentOsPoliciesList":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesList", jsii.get(self, "osPolicies"))

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
    def rollout(self) -> "OsConfigOsPolicyAssignmentRolloutOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentRolloutOutputReference", jsii.get(self, "rollout"))

    @builtins.property
    @jsii.member(jsii_name="rolloutState")
    def rollout_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rolloutState"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OsConfigOsPolicyAssignmentTimeoutsOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceFilterInput")
    def instance_filter_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentInstanceFilter"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentInstanceFilter"], jsii.get(self, "instanceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="osPoliciesInput")
    def os_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPolicies"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPolicies"]]], jsii.get(self, "osPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutInput")
    def rollout_input(self) -> typing.Optional["OsConfigOsPolicyAssignmentRollout"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentRollout"], jsii.get(self, "rolloutInput"))

    @builtins.property
    @jsii.member(jsii_name="skipAwaitRolloutInput")
    def skip_await_rollout_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipAwaitRolloutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OsConfigOsPolicyAssignmentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OsConfigOsPolicyAssignmentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de98324b8ffbd34e3657c3634b0f0645f1e813f991f039232aff82dd87fe118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fca1297f48dc099c8c230b17f02175a322c1c26a79682127046687c65605eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb358a0f3e6e7b575476bb3a41d78674c798d41abc876077d7b89210b967eb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1942095886d7bc683dc32067e11abe58b1bb80ca25172dec97a450fc2646b15a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3681c16d71bf039ed2e4f12aa1989758229de6dfac9312fad7282fe9ec4164d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipAwaitRollout")
    def skip_await_rollout(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipAwaitRollout"))

    @skip_await_rollout.setter
    def skip_await_rollout(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f7fcceb13661fa116d09a319572f5a3b8f5b5b6ebc5f1985f38a0311c45f3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipAwaitRollout", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance_filter": "instanceFilter",
        "location": "location",
        "name": "name",
        "os_policies": "osPolicies",
        "rollout": "rollout",
        "description": "description",
        "id": "id",
        "project": "project",
        "skip_await_rollout": "skipAwaitRollout",
        "timeouts": "timeouts",
    },
)
class OsConfigOsPolicyAssignmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance_filter: typing.Union["OsConfigOsPolicyAssignmentInstanceFilter", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentOsPolicies", typing.Dict[builtins.str, typing.Any]]]],
        rollout: typing.Union["OsConfigOsPolicyAssignmentRollout", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        skip_await_rollout: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#instance_filter OsConfigOsPolicyAssignment#instance_filter}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#location OsConfigOsPolicyAssignment#location}
        :param name: Resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        :param os_policies: os_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#os_policies OsConfigOsPolicyAssignment#os_policies}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#rollout OsConfigOsPolicyAssignment#rollout}
        :param description: OS policy assignment description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#description OsConfigOsPolicyAssignment#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#id OsConfigOsPolicyAssignment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#project OsConfigOsPolicyAssignment#project}
        :param skip_await_rollout: Set to true to skip awaiting rollout during resource creation and update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#skip_await_rollout OsConfigOsPolicyAssignment#skip_await_rollout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#timeouts OsConfigOsPolicyAssignment#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(instance_filter, dict):
            instance_filter = OsConfigOsPolicyAssignmentInstanceFilter(**instance_filter)
        if isinstance(rollout, dict):
            rollout = OsConfigOsPolicyAssignmentRollout(**rollout)
        if isinstance(timeouts, dict):
            timeouts = OsConfigOsPolicyAssignmentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2014c6192095d07ae66e206826c3e6228bc6106936888aec4b135226cf51c2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance_filter", value=instance_filter, expected_type=type_hints["instance_filter"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument os_policies", value=os_policies, expected_type=type_hints["os_policies"])
            check_type(argname="argument rollout", value=rollout, expected_type=type_hints["rollout"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument skip_await_rollout", value=skip_await_rollout, expected_type=type_hints["skip_await_rollout"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_filter": instance_filter,
            "location": location,
            "name": name,
            "os_policies": os_policies,
            "rollout": rollout,
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
        if project is not None:
            self._values["project"] = project
        if skip_await_rollout is not None:
            self._values["skip_await_rollout"] = skip_await_rollout
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
    def instance_filter(self) -> "OsConfigOsPolicyAssignmentInstanceFilter":
        '''instance_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#instance_filter OsConfigOsPolicyAssignment#instance_filter}
        '''
        result = self._values.get("instance_filter")
        assert result is not None, "Required property 'instance_filter' is missing"
        return typing.cast("OsConfigOsPolicyAssignmentInstanceFilter", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#location OsConfigOsPolicyAssignment#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def os_policies(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPolicies"]]:
        '''os_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#os_policies OsConfigOsPolicyAssignment#os_policies}
        '''
        result = self._values.get("os_policies")
        assert result is not None, "Required property 'os_policies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPolicies"]], result)

    @builtins.property
    def rollout(self) -> "OsConfigOsPolicyAssignmentRollout":
        '''rollout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#rollout OsConfigOsPolicyAssignment#rollout}
        '''
        result = self._values.get("rollout")
        assert result is not None, "Required property 'rollout' is missing"
        return typing.cast("OsConfigOsPolicyAssignmentRollout", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''OS policy assignment description. Length of the description is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#description OsConfigOsPolicyAssignment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#id OsConfigOsPolicyAssignment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#project OsConfigOsPolicyAssignment#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_await_rollout(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to skip awaiting rollout during resource creation and update.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#skip_await_rollout OsConfigOsPolicyAssignment#skip_await_rollout}
        '''
        result = self._values.get("skip_await_rollout")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OsConfigOsPolicyAssignmentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#timeouts OsConfigOsPolicyAssignment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentInstanceFilter",
    jsii_struct_bases=[],
    name_mapping={
        "all": "all",
        "exclusion_labels": "exclusionLabels",
        "inclusion_labels": "inclusionLabels",
        "inventories": "inventories",
    },
)
class OsConfigOsPolicyAssignmentInstanceFilter:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentInstanceFilterInventories", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all: Target all VMs in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#all OsConfigOsPolicyAssignment#all}
        :param exclusion_labels: exclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#exclusion_labels OsConfigOsPolicyAssignment#exclusion_labels}
        :param inclusion_labels: inclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#inclusion_labels OsConfigOsPolicyAssignment#inclusion_labels}
        :param inventories: inventories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#inventories OsConfigOsPolicyAssignment#inventories}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43746bfaec4f9ee8fb936a3c7295e0ef77f1a29e2ace3a7badcbe13164f5a0b1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#all OsConfigOsPolicyAssignment#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclusion_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels"]]]:
        '''exclusion_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#exclusion_labels OsConfigOsPolicyAssignment#exclusion_labels}
        '''
        result = self._values.get("exclusion_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels"]]], result)

    @builtins.property
    def inclusion_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels"]]]:
        '''inclusion_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#inclusion_labels OsConfigOsPolicyAssignment#inclusion_labels}
        '''
        result = self._values.get("inclusion_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels"]]], result)

    @builtins.property
    def inventories(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentInstanceFilterInventories"]]]:
        '''inventories block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#inventories OsConfigOsPolicyAssignment#inventories}
        '''
        result = self._values.get("inventories")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentInstanceFilterInventories"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentInstanceFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Labels are identified by key/value pairs in this map. A VM should contain all the key/value pairs specified in this map to be selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#labels OsConfigOsPolicyAssignment#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b341664f4f3f97f6326b01634dc4de005bf3c6bc05517943ba2e595d74ede19)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels are identified by key/value pairs in this map.

        A VM should contain all the key/value pairs specified in this map to be selected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#labels OsConfigOsPolicyAssignment#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentInstanceFilterExclusionLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentInstanceFilterExclusionLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc811d25056174a355f35f73a19c902d1fb281585c18b550c30a2683c37d5fc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigOsPolicyAssignmentInstanceFilterExclusionLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489c08a46a32796379c33c1580e56e6c12a18849ed1a8dc7f362dfe72cbc52b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigOsPolicyAssignmentInstanceFilterExclusionLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fefa3e0c7f3c3486582a052105eb260b34fe221f1f3603f53167ecb87b342cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b838f9d52bd7aa0e73d4a00c386f8c393cfa76c098933f924b33e9f0516429a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__840e5288031ffd9bd63197151638af4779e33c0bb4ab978ed087a39c465374c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec982d26e612a395446ba8c8a55f233a865c8550b537d09390ddc7a3323b094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentInstanceFilterExclusionLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentInstanceFilterExclusionLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5ce4bb799086372961e79a570b3803febe5bd96cb7dea75920290f1e7174e8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e45fd43b9651afa755d4a9194dfaac086ed8adf8dba56a23b6e33705658c80ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f03a0b71f281d670408148e3ffef390c84ba981de047da7b8ecca88bc730fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Labels are identified by key/value pairs in this map. A VM should contain all the key/value pairs specified in this map to be selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#labels OsConfigOsPolicyAssignment#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4907d06cf094d6a95d050ce7e582752a204dbac770664edefee4328734c9cb43)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels are identified by key/value pairs in this map.

        A VM should contain all the key/value pairs specified in this map to be selected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#labels OsConfigOsPolicyAssignment#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentInstanceFilterInclusionLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentInstanceFilterInclusionLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df875797187c07d1fad9ba630e52e5a16cbb14a21b57e42691d729377d49b70b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigOsPolicyAssignmentInstanceFilterInclusionLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d72a226e2afb89bbb4bc9bee511b510790378ac5295f03aaf44786896c6c98)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigOsPolicyAssignmentInstanceFilterInclusionLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8437430821cbe9ec264f8671226a55a286bed4d48faa7e23846131b5ac8891cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5350bb7619b09c7984bf4fa4e83bd484a9ecbedd87a55393e9a1039888d38b37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eca3b8e442683381009eaaa4d3eae44a6463acbe2ffeb8ae05beecacad08d414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba31f5bc21b2a07c47f2f144d42ed249259789f17e915163317573b94da9100b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentInstanceFilterInclusionLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentInstanceFilterInclusionLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98168c363b90ab5599083c37b554f110dac6675b21341ef634a858cbd76f5904)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ef3c8f894429e9124e4d19d7517118a399d47c85e1619fdefb447db19e74673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8b6c7a605478153c5726985c1bddf43be5f5cc07a00a03f01c9395e4d845bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentInstanceFilterInventories",
    jsii_struct_bases=[],
    name_mapping={"os_short_name": "osShortName", "os_version": "osVersion"},
)
class OsConfigOsPolicyAssignmentInstanceFilterInventories:
    def __init__(
        self,
        *,
        os_short_name: builtins.str,
        os_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_short_name: The OS short name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#os_short_name OsConfigOsPolicyAssignment#os_short_name}
        :param os_version: The OS version Prefix matches are supported if asterisk(*) is provided as the last character. For example, to match all versions with a major version of '7', specify the following value for this field '7.*' An empty string matches all OS versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#os_version OsConfigOsPolicyAssignment#os_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b77fb0efb958887a0008a93491806bb879355c7d29a83d7e912790693df6cc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#os_short_name OsConfigOsPolicyAssignment#os_short_name}
        '''
        result = self._values.get("os_short_name")
        assert result is not None, "Required property 'os_short_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def os_version(self) -> typing.Optional[builtins.str]:
        '''The OS version Prefix matches are supported if asterisk(*) is provided as the last character.

        For example, to match all versions with a major version of '7', specify the following value for this field '7.*' An empty string matches all OS versions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#os_version OsConfigOsPolicyAssignment#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentInstanceFilterInventories(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentInstanceFilterInventoriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentInstanceFilterInventoriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85f884ce1ab412707b604d8fc6a2c46d53e50765a7bf79a71367aafb9d239349)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigOsPolicyAssignmentInstanceFilterInventoriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9758d43d4aea457af3a5b3bee454cd022d0e7b3018be01065be6df6e2d0f611e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigOsPolicyAssignmentInstanceFilterInventoriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88bb24d3c8e1872d499e9efeffb9297ba30419b8eb1e6bac82469df8b55a638)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2a2644ceee5b5ede3ec81a0328901ec2905458999f8a2149521c3c302e67e19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e2a2833f34bf2957152e59f53052aea9b2893038251a59f7276a4c85d7db6f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterInventories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterInventories]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterInventories]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa423392881791cd3304712d3c49f73c10f025a1db76567a0a62ad0dedca067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentInstanceFilterInventoriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentInstanceFilterInventoriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db0d7c65ed5a8b853fa2a22b7d56140d8c33e6fe5314c6d716d39321da652f55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d143d01d0e31eabf02fe79c7cfdba0efe7d80f25a2d3a0421a60a16318d46f71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osShortName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d82ebcc9ac48ba862e9497eb0b0e129b4f232072c559da07182b8604cff6b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentInstanceFilterInventories]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentInstanceFilterInventories]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentInstanceFilterInventories]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91a3d0fdeebc0b92d2f02787067a2a4b34f14208a51a18db3cd4c63fac3b87ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentInstanceFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentInstanceFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae77deaf400089d4672210bc708f8d5d4ca20a6622ce0c62925808c2e3f12136)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusionLabels")
    def put_exclusion_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93bba52827a03ac7fb9050e85faf668df68ee0cc07c1ca6cfe0622c84c692b76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusionLabels", [value]))

    @jsii.member(jsii_name="putInclusionLabels")
    def put_inclusion_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41bc4cf4d59478652907fc21250a068c99277c7bd488d5b6c10ebf6c3f22eb9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInclusionLabels", [value]))

    @jsii.member(jsii_name="putInventories")
    def put_inventories(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0434a4c748d4b556fbb6a8eb79dbef39abebb6c5e6568dbcf05de3cf4e5ec0)
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
    ) -> OsConfigOsPolicyAssignmentInstanceFilterExclusionLabelsList:
        return typing.cast(OsConfigOsPolicyAssignmentInstanceFilterExclusionLabelsList, jsii.get(self, "exclusionLabels"))

    @builtins.property
    @jsii.member(jsii_name="inclusionLabels")
    def inclusion_labels(
        self,
    ) -> OsConfigOsPolicyAssignmentInstanceFilterInclusionLabelsList:
        return typing.cast(OsConfigOsPolicyAssignmentInstanceFilterInclusionLabelsList, jsii.get(self, "inclusionLabels"))

    @builtins.property
    @jsii.member(jsii_name="inventories")
    def inventories(self) -> OsConfigOsPolicyAssignmentInstanceFilterInventoriesList:
        return typing.cast(OsConfigOsPolicyAssignmentInstanceFilterInventoriesList, jsii.get(self, "inventories"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels]]], jsii.get(self, "exclusionLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="inclusionLabelsInput")
    def inclusion_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels]]], jsii.get(self, "inclusionLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="inventoriesInput")
    def inventories_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterInventories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterInventories]]], jsii.get(self, "inventoriesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__504cdcce063b3f66651c5755147528b422018a0c7f1b87f4dd6c0eccce8c8447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentInstanceFilter]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentInstanceFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentInstanceFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37fe8571127048929312879afdd566e7ccb7185c8c39039fdaeebdb841b4237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "mode": "mode",
        "resource_groups": "resourceGroups",
        "allow_no_resource_group_match": "allowNoResourceGroupMatch",
        "description": "description",
    },
)
class OsConfigOsPolicyAssignmentOsPolicies:
    def __init__(
        self,
        *,
        id: builtins.str,
        mode: builtins.str,
        resource_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroups", typing.Dict[builtins.str, typing.Any]]]],
        allow_no_resource_group_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The id of the OS policy with the following restrictions: * Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#id OsConfigOsPolicyAssignment#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mode: Policy mode Possible values: ["MODE_UNSPECIFIED", "VALIDATION", "ENFORCEMENT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#mode OsConfigOsPolicyAssignment#mode}
        :param resource_groups: resource_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#resource_groups OsConfigOsPolicyAssignment#resource_groups}
        :param allow_no_resource_group_match: This flag determines the OS policy compliance status when none of the resource groups within the policy are applicable for a VM. Set this value to 'true' if the policy needs to be reported as compliant even if the policy has nothing to validate or enforce. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_no_resource_group_match OsConfigOsPolicyAssignment#allow_no_resource_group_match}
        :param description: Policy description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#description OsConfigOsPolicyAssignment#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e25b3ac630b9b43d238277910b1396dfa8a54f26da465fb5fb4ad4b620167b)
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
        '''The id of the OS policy with the following restrictions: * Must contain only lowercase letters, numbers, and hyphens.

        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#id OsConfigOsPolicyAssignment#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''Policy mode Possible values: ["MODE_UNSPECIFIED", "VALIDATION", "ENFORCEMENT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#mode OsConfigOsPolicyAssignment#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_groups(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPoliciesResourceGroups"]]:
        '''resource_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#resource_groups OsConfigOsPolicyAssignment#resource_groups}
        '''
        result = self._values.get("resource_groups")
        assert result is not None, "Required property 'resource_groups' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPoliciesResourceGroups"]], result)

    @builtins.property
    def allow_no_resource_group_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag determines the OS policy compliance status when none of the resource groups within the policy are applicable for a VM.

        Set this value to 'true' if the policy needs to be reported as compliant even if the policy has nothing to validate or enforce.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_no_resource_group_match OsConfigOsPolicyAssignment#allow_no_resource_group_match}
        '''
        result = self._values.get("allow_no_resource_group_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Policy description. Length of the description is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#description OsConfigOsPolicyAssignment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e1c4578bb552851a4daa6d51710f9c9abc0ce7110bc3eb07bedb991bdf280e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a86a3144072fc468e8653d32573fa4525a7b3c5d28db19ee9770d86eb820fe1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2693c573507f98fba742af31ac6d12a665dff67c2041b5eef3ef98fd432b747e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d420f32770f9354a0a40c97243dd4faff4f20dedf2906523008b0e2f82126b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d628e7501825b8b2aeabff2f48e7d91350e1cdc3f074bc21c95d03b98ef89cf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9212b8827002d1823182cb1ce94ecb70630ab2d434c99ad887980e5a6f6463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__263a48520f6c9f1eedd3ed5714935da0501fa8f15e3a8c7ad6ce9daa8a3e8fea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putResourceGroups")
    def put_resource_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroups", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__255da8f3a4d6952f8caf36fb3173915d6799226e88f00cbaeaee9b5e2dd79327)
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
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsList":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsList", jsii.get(self, "resourceGroups"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPoliciesResourceGroups"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPoliciesResourceGroups"]]], jsii.get(self, "resourceGroupsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c04d1568d52c5b44f13326ecff69a0189ff634a1bd1de39b4587cd0570c32970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowNoResourceGroupMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5258fb8c27d818ecb3a49c6dc9781557d6253a6de56766e5e9c564a7b3162ee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4866f61e95621190bb0ac1ab6c2ec3d0933f5c1d969ecc7664403428d94c2a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac6afb6e14f567b6ce77428bbc865eb715af255124b839ebcecc85c6d3dfd64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b6a57a82f90d68e973f7d16a7455db8012440f1129c0adcfa241d35c1463b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroups",
    jsii_struct_bases=[],
    name_mapping={"resources": "resources", "inventory_filters": "inventoryFilters"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroups:
    def __init__(
        self,
        *,
        resources: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources", typing.Dict[builtins.str, typing.Any]]]],
        inventory_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#resources OsConfigOsPolicyAssignment#resources}
        :param inventory_filters: inventory_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#inventory_filters OsConfigOsPolicyAssignment#inventory_filters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca2b2c45c064db466138092f55de202517e6f10af3f3e861bee0e9a9a7199278)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources"]]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#resources OsConfigOsPolicyAssignment#resources}
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources"]], result)

    @builtins.property
    def inventory_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters"]]]:
        '''inventory_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#inventory_filters OsConfigOsPolicyAssignment#inventory_filters}
        '''
        result = self._values.get("inventory_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters",
    jsii_struct_bases=[],
    name_mapping={"os_short_name": "osShortName", "os_version": "osVersion"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters:
    def __init__(
        self,
        *,
        os_short_name: builtins.str,
        os_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_short_name: The OS short name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#os_short_name OsConfigOsPolicyAssignment#os_short_name}
        :param os_version: The OS version Prefix matches are supported if asterisk(*) is provided as the last character. For example, to match all versions with a major version of '7', specify the following value for this field '7.*' An empty string matches all OS versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#os_version OsConfigOsPolicyAssignment#os_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2df9e7bffda2da0e82a7fe4216b79f8bfaf67f15900818a5fc96112809a076f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#os_short_name OsConfigOsPolicyAssignment#os_short_name}
        '''
        result = self._values.get("os_short_name")
        assert result is not None, "Required property 'os_short_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def os_version(self) -> typing.Optional[builtins.str]:
        '''The OS version Prefix matches are supported if asterisk(*) is provided as the last character.

        For example, to match all versions with a major version of '7', specify the following value for this field '7.*'
        An empty string matches all OS versions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#os_version OsConfigOsPolicyAssignment#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3be9c11a391d8e7fb9086c3e1b6da95dd1af60358e0f40e73c41a24b14e3d1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05740f9c16ae1454b34b08aa73ec4513be1d2031d949341369a6c6002f0b9756)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b252fb1dee20eea8177f090ff072cc2b80c3cbd948cc8c7f208747319f234e2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d261b517f119904505d4f6e78bfe6651b0f61ee6012db9d4d1c378e51ecc8984)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b705c6c5139462aaa4d4e4c94d18f25d441b52b37671d6ed72fb0d3ce5b9883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e96d75485f9a4d1bce588de8a3080d352c1a1fbb17e976532a77d32b9d1945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25b949d380c15846ae5e33bbf4c8ed9e8b7897fd8382306cab35dc9e282d59f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2810cfeaaa78f068f8a6dbede9a379130ed80d048391802cfa7dbfe8dd39cc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osShortName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48a543a43c8e0ea75de8a2d0a7b4b2e7492cf87249f0938f19e6aa913a3324cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c657bc5d151642138e344e4b528a41ba83f93b55f614eef060e265641322e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1aa8a9846e51e9d81f81ea56ad131beab988c7a6be2d4059694c08a6b67fb40f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b672cdf14ed9455f3151d0480c1625cf30cddc3d5fc8295838f3ecfc75e996c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a2cf57be225a991ebb9cdedbe8062d5ae93e3c74deae52b9c63c03e70534bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3828645fe2d42d12d1e1d03537db7b0dfff2dd9102cf25ff180c65cb7ca69f56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0a639f815f8d1dcaf2724fe4cd7d518c55b4987baa22508a22c783f514cfb45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c2a560d14c4db4e47b3973bbcc4020bdbd8d682cfd1bf1ab3e66ee74b913d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc3307fc6c8efcdd3cd4e412dd93cff7c171fd1782bebff6aec055a049d62073)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInventoryFilters")
    def put_inventory_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ea44654fe1e8ad8f2427662117bc1d435a6c75aa4910e3f612381a9c72d323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInventoryFilters", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3094a4643e67a0a36d5aebfecd26b4897aaec715b94791583686d047823e8e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="resetInventoryFilters")
    def reset_inventory_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInventoryFilters", []))

    @builtins.property
    @jsii.member(jsii_name="inventoryFilters")
    def inventory_filters(
        self,
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFiltersList:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFiltersList, jsii.get(self, "inventoryFilters"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesList":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesList", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="inventoryFiltersInput")
    def inventory_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters]]], jsii.get(self, "inventoryFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources"]]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPoliciesResourceGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPoliciesResourceGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPoliciesResourceGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827f0e5cbfb3244fc0335b58d84bec39d82a1985b5f18cd58752d4f7b6ce3f2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "exec": "exec",
        "file": "file",
        "pkg": "pkg",
        "repository": "repository",
    },
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources:
    def __init__(
        self,
        *,
        id: builtins.str,
        exec: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile", typing.Dict[builtins.str, typing.Any]]] = None,
        pkg: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg", typing.Dict[builtins.str, typing.Any]]] = None,
        repository: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: The id of the resource with the following restrictions: * Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the OS policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#id OsConfigOsPolicyAssignment#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#exec OsConfigOsPolicyAssignment#exec}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#file OsConfigOsPolicyAssignment#file}
        :param pkg: pkg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#pkg OsConfigOsPolicyAssignment#pkg}
        :param repository: repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#repository OsConfigOsPolicyAssignment#repository}
        '''
        if isinstance(exec, dict):
            exec = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec(**exec)
        if isinstance(file, dict):
            file = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile(**file)
        if isinstance(pkg, dict):
            pkg = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg(**pkg)
        if isinstance(repository, dict):
            repository = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository(**repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42c4d9db6723cb5e11d0973e9939e92b3af7121ebc17dc0bab71c7be46e672f)
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
        '''The id of the resource with the following restrictions: * Must contain only lowercase letters, numbers, and hyphens.

        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the OS policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#id OsConfigOsPolicyAssignment#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exec(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec"]:
        '''exec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#exec OsConfigOsPolicyAssignment#exec}
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec"], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#file OsConfigOsPolicyAssignment#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile"], result)

    @builtins.property
    def pkg(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg"]:
        '''pkg block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#pkg OsConfigOsPolicyAssignment#pkg}
        '''
        result = self._values.get("pkg")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg"], result)

    @builtins.property
    def repository(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository"]:
        '''repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#repository OsConfigOsPolicyAssignment#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec",
    jsii_struct_bases=[],
    name_mapping={"validate": "validate", "enforce": "enforce"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec:
    def __init__(
        self,
        *,
        validate: typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate", typing.Dict[builtins.str, typing.Any]],
        enforce: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param validate: validate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#validate OsConfigOsPolicyAssignment#validate}
        :param enforce: enforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#enforce OsConfigOsPolicyAssignment#enforce}
        '''
        if isinstance(validate, dict):
            validate = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate(**validate)
        if isinstance(enforce, dict):
            enforce = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce(**enforce)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63129cf81507b9af52ea018e1ccdd2f17f6fab92e1d51c9b7edc47915046312b)
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
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate":
        '''validate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#validate OsConfigOsPolicyAssignment#validate}
        '''
        result = self._values.get("validate")
        assert result is not None, "Required property 'validate' is missing"
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate", result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce"]:
        '''enforce block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#enforce OsConfigOsPolicyAssignment#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce",
    jsii_struct_bases=[],
    name_mapping={
        "interpreter": "interpreter",
        "args": "args",
        "file": "file",
        "output_file_path": "outputFilePath",
        "script": "script",
    },
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce:
    def __init__(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: The script interpreter to use. Possible values: ["INTERPRETER_UNSPECIFIED", "NONE", "SHELL", "POWERSHELL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#interpreter OsConfigOsPolicyAssignment#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#args OsConfigOsPolicyAssignment#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#file OsConfigOsPolicyAssignment#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 100K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#output_file_path OsConfigOsPolicyAssignment#output_file_path}
        :param script: An inline script. The size of the script is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#script OsConfigOsPolicyAssignment#script}
        '''
        if isinstance(file, dict):
            file = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006f8abca2016ac13407b16d4943109d0ecc1eb136e85da268fba60ae3ecee26)
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
        '''The script interpreter to use. Possible values: ["INTERPRETER_UNSPECIFIED", "NONE", "SHELL", "POWERSHELL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#interpreter OsConfigOsPolicyAssignment#interpreter}
        '''
        result = self._values.get("interpreter")
        assert result is not None, "Required property 'interpreter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional arguments to pass to the source during execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#args OsConfigOsPolicyAssignment#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#file OsConfigOsPolicyAssignment#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile"], result)

    @builtins.property
    def output_file_path(self) -> typing.Optional[builtins.str]:
        '''Only recorded for enforce Exec.

        Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 100K bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#output_file_path OsConfigOsPolicyAssignment#output_file_path}
        '''
        result = self._values.get("output_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''An inline script. The size of the script is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#script OsConfigOsPolicyAssignment#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9701b900a4ccb816b9c299819813fdcffc846d8826c2d34ebac18676c17c98)
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
        '''Defaults to false.

        When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef0f2cb47746a9af8dfc756a4a5bea4d9097dee69ced88ba5f6175183899cdb1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[jsii.Number]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ace4d62e6b80d8c1112c31fbe0bd7a17e36d5c7c58ada13bc5cd3b43b631631)
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
    def generation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "generationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c9db24d2b316464a242cd204120299aabb86bb9d09d522648c2bd0dc7869dcac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__774adc1d249918333de88177b6ef3be46d13df77590da503d6e2758a9955863e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78555b3610ae8b51fa544b605bd947932a8ab1c803ffc39abd9b2a2891d1d2b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4632db73ebbccddc48f9e19439c20edcda07c72474afd55992ff787393cdaff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d918ed9999267caafba876f5ca541d294f0c813e13b112d7f8b2fba1e6189cda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(
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
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__28572bb233c10bfbf11fc59974c147ed28e6498fc4a67b7c5c8438af541ccd52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b509a09313cc55584c6f39b8e365692f2dbb9b8b7bccb75b0c14bb191f5d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e16acc2b073914730037e89d9579c2e4776db520a0b3ad2ecbeadd4ac9d227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d63b411731f6553a789ba4fe87e9e053046a14db8618225e492aac7d27a2d3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4f57325e7e346080c2f8a608764f8edeb13695e0638da0e933b18b2b96a0b48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe3728c5bd2c3e80a8c2a5ede2c7e6a0291ca48462757247d5ae401c949cf5fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db87c43b0aec8e5d4861c5cb68d1b0262f272c5fd6aaf10371ac051f95b74013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788d5663c1c053cfd5f58633747fc05c3b8cea31d64220972194358289a23b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00151899d28d5c808a8f71777d450d8a4ea3610616fedc826057e9eae215482b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile(
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
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile], jsii.get(self, "fileInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__40b1826a4f3e02c1ce9977a33108d98a9d434ec3326fd6a12afee0afd576e28e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e493e67d17c5d1445eb085aa77c7cbc0e133a409a2015c991fae97215e4da30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFilePath")
    def output_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFilePath"))

    @output_file_path.setter
    def output_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3509cdd887671d9cce34bb95c8e13046e40948660bb78cc6e87c90e13b8d43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d737c633e5c789bf9ac9f3cf33db67844a5ff6f5d3ccd68e084cbb2c4bfa903)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9e5df5433fec43847eaca3bee4338773df327eed77eead94ddc0e0fd7e5787)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c705c056b0b2c246fccfd35041904f10aefa0202ae3221af737d8428bad1e0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnforce")
    def put_enforce(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile, typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: The script interpreter to use. Possible values: ["INTERPRETER_UNSPECIFIED", "NONE", "SHELL", "POWERSHELL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#interpreter OsConfigOsPolicyAssignment#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#args OsConfigOsPolicyAssignment#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#file OsConfigOsPolicyAssignment#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 100K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#output_file_path OsConfigOsPolicyAssignment#output_file_path}
        :param script: An inline script. The size of the script is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#script OsConfigOsPolicyAssignment#script}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce(
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
        file: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: The script interpreter to use. Possible values: ["INTERPRETER_UNSPECIFIED", "NONE", "SHELL", "POWERSHELL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#interpreter OsConfigOsPolicyAssignment#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#args OsConfigOsPolicyAssignment#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#file OsConfigOsPolicyAssignment#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 100K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#output_file_path OsConfigOsPolicyAssignment#output_file_path}
        :param script: An inline script. The size of the script is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#script OsConfigOsPolicyAssignment#script}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate(
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
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceOutputReference, jsii.get(self, "enforce"))

    @builtins.property
    @jsii.member(jsii_name="validate")
    def validate(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateOutputReference", jsii.get(self, "validate"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="validateInput")
    def validate_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate"], jsii.get(self, "validateInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4860cdd9de480d07a3cc7e0ff4b541c293eb12e2a1616385843db9470d1b6fff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate",
    jsii_struct_bases=[],
    name_mapping={
        "interpreter": "interpreter",
        "args": "args",
        "file": "file",
        "output_file_path": "outputFilePath",
        "script": "script",
    },
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate:
    def __init__(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: The script interpreter to use. Possible values: ["INTERPRETER_UNSPECIFIED", "NONE", "SHELL", "POWERSHELL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#interpreter OsConfigOsPolicyAssignment#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#args OsConfigOsPolicyAssignment#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#file OsConfigOsPolicyAssignment#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 100K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#output_file_path OsConfigOsPolicyAssignment#output_file_path}
        :param script: An inline script. The size of the script is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#script OsConfigOsPolicyAssignment#script}
        '''
        if isinstance(file, dict):
            file = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c85ee25fe6100f2743a5a7a19d0d654b014f439d86e4a6a2f6ca86b8c9f52f)
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
        '''The script interpreter to use. Possible values: ["INTERPRETER_UNSPECIFIED", "NONE", "SHELL", "POWERSHELL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#interpreter OsConfigOsPolicyAssignment#interpreter}
        '''
        result = self._values.get("interpreter")
        assert result is not None, "Required property 'interpreter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional arguments to pass to the source during execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#args OsConfigOsPolicyAssignment#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#file OsConfigOsPolicyAssignment#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile"], result)

    @builtins.property
    def output_file_path(self) -> typing.Optional[builtins.str]:
        '''Only recorded for enforce Exec.

        Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 100K bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#output_file_path OsConfigOsPolicyAssignment#output_file_path}
        '''
        result = self._values.get("output_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''An inline script. The size of the script is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#script OsConfigOsPolicyAssignment#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a8b8741e3c87f3aaec1d773d07ef756d5e810af71f31f9c0b5f5f1713e95cd1)
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
        '''Defaults to false.

        When false, files are subject to validations based on the file type:
        Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b271f774e5e88e80bfe54e4c8628690e0e030f9ae780ac07448d2bce263587)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[jsii.Number]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee15199446a8075331193c9dc5bce827b53c1af34f8956d86aff41ae0e5247e2)
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
    def generation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "generationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cd2e60f9b63bf19932f80447b485308b43b3de4180272bdb5fbf7501ab9c673c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42b91233e086917e525fae8a457e950a5bf206645109bc97854e5546a4d79f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7741369c3242e8d58ecad1bf1b44b94427ded7156836f576a6a22c1f8d0df03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab0d4c6014509408774bb9fb79e355973f16c8541d832e4deff06ec2deb219c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbbe06c149e9f4aee08892b655507b1be90d694f8854566e3f147b8b5d7cd4e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote(
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
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__caa416aa44d6d0c0d0f9ea91d46c6599844ef2240badc4817695195a0cf84f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9439d4c3c25ef3f43c3eb4bafd5e2dbd1c8486b01b93fd4e5fd28ccfba97e16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515146d695a0d4a162d1385a896c35e05edd5da40af8e506e6e421a3a631df9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca796599a0eb0da7c4d03739ef2379acd16f26c7f9685519665cf45b5009a54)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84f3bc7c12e4071a48b575544d116ea066184433d078f3d341086b7fe521d10a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03c9def3d1064ebbde645c5ee7018f869c8cbb23c468c4ef935a66f2d76ea328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5222e8542f065190561b42aaef2b9f29ddbf564f9c9c12a9be805c82342b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3488218e943e452c56a7f1020210c3c9a0b6e88a38f2ba6e44f9b497e290d68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5f37691edac738acc7471b9102cb78ca7229766559b68b65d645523d70df389)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile(
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
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile], jsii.get(self, "fileInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fb3b16c00cec64def563b75500849fe28ae34dae6536d7481df010562f318fe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4fd8f665709a640eea3697c87ab3cd015aa901fdd06807e6fce8ac46486f6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFilePath")
    def output_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFilePath"))

    @output_file_path.setter
    def output_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98201a4dc9ca30ce45a1c75514d396ab152b39dd0242ef0b6d5e6c32859bceed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c052d57df353e4bef73d28076589d6878d0c69ba9ae86232432a2f9375acc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74564d8567897c4f690669c27e9f3fb4810775ccf0975cb20a0cc28fee992a2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "state": "state",
        "content": "content",
        "file": "file",
    },
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile:
    def __init__(
        self,
        *,
        path: builtins.str,
        state: builtins.str,
        content: typing.Optional[builtins.str] = None,
        file: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param path: The absolute path of the file within the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#path OsConfigOsPolicyAssignment#path}
        :param state: Desired state of the file. Possible values: ["DESIRED_STATE_UNSPECIFIED", "PRESENT", "ABSENT", "CONTENTS_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#state OsConfigOsPolicyAssignment#state}
        :param content: A a file with this content. The size of the content is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#content OsConfigOsPolicyAssignment#content}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#file OsConfigOsPolicyAssignment#file}
        '''
        if isinstance(file, dict):
            file = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96a72bafd87717aeadc8e3629a9cd09f707d23963819e92fc59482804c590d8)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "state": state,
        }
        if content is not None:
            self._values["content"] = content
        if file is not None:
            self._values["file"] = file

    @builtins.property
    def path(self) -> builtins.str:
        '''The absolute path of the file within the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#path OsConfigOsPolicyAssignment#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''Desired state of the file. Possible values: ["DESIRED_STATE_UNSPECIFIED", "PRESENT", "ABSENT", "CONTENTS_MATCH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#state OsConfigOsPolicyAssignment#state}
        '''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''A a file with this content. The size of the content is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#content OsConfigOsPolicyAssignment#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#file OsConfigOsPolicyAssignment#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab79aad00adb4f010bb7ec52e73a9fb2dfbf18231f2b8e3ae1bf21befa76cf0a)
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
        '''Defaults to false.

        When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e49b500dfd6f1fb59d19ed9f51576bdf76b0f765adeaa806634c88634c279002)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[jsii.Number]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0360114d2f0724926e4d8cb9d88e3017e30df274da3e29e850cd595c7d18914e)
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
    def generation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "generationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a6da2abca89f9d00d08c66cfe9f5b0465539addd5ad21ce1b1035817f015a53d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e2bd7a207d7186219918cb04e8c9843c7bae2907ef62d99cde5428aba0e736c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9b140a25f396cde74d578ddb53d5db1b3ae2c593543e2a1f3f9a930b39189f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2996e3a534ab1aa45f4cf86e79752572a2f968940f90236e1b073de240d49fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__069bbd34ce8801f00eb0388005c9cdeb451ab6ecc0556c38d29602eeb48a3321)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote(
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
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7dd8a20bae45f732581bfd8c32c7d91a3e552de75eeb57638f42a3467479c710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1020367dd20200d2780664159b0725800c6aca926f0909063b0b9563544bcb75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96df7c8b7af0088f9e11dee0f7b606fd72019e167d78671799c9097647de121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7dd0dae18f9d4a47aa7ba340b0d5102e4532233767862f044da1e8a799b8bba)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e93f1d509df74942dce0cd26478cc40a74302434522a9da5666dd4aa96a234e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6e9bd6c7b390da7847f0e556cc82de5c82cb347409d25bee3f5332d6e382674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9138004b9bb61f1013958463bb703d7538b70df09559d594e1a34d5faebc732a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3825399acbf37cc99ba2aba42f36c5ac792e6c7983048997be8f73684b68d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98d3b35ab88036751dc60f2092bec15e8fa0525ecdfb7e2dba573b19f1a6bbf2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile(
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

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1ac222421c683acf44eb9fbe3ab6c4859cdecb4822b6380fc190ca34a2a847bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb61f02f3b76102b9a94d0c1d9396d37323cea49afd1b00584b131fb9b15265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e8cb863e950f5c0ae3ee975b214376058d4b5874de992d64bed7edc4adf90b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccfd887101b586b66086b04ef96c9150d8cafb29d81b6e83cfbb5e3ff7576ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f213137638be89c02f307db636f0af5c4bd8e7ab9d406c1375776683e36c9d9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a644f6f16bd29a832a31603bc80f5a75b0308dc9c38b4a7c523f3cfe1e2f7022)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd3081d045ff259d54504abb2670c2eb9af6ce12a1b12f74176e4eac24f58f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b479a15edebe26cb2433a5f0b45825811a1fa135ad76758cc008cbdf89c13f53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00e191c9cfeb2055eed1f2b81765f04fdd57726d844b10f753c4153cd4baddc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af3743212079593249e31e9e2c467a61f5647f6cbb72b0ea020fb82187dfa3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b82df947d8234c180fcefc97dbc263e19e1ed1219fc25475ca9c0fa867ee6e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExec")
    def put_exec(
        self,
        *,
        validate: typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate, typing.Dict[builtins.str, typing.Any]],
        enforce: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param validate: validate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#validate OsConfigOsPolicyAssignment#validate}
        :param enforce: enforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#enforce OsConfigOsPolicyAssignment#enforce}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec(
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
        file: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param path: The absolute path of the file within the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#path OsConfigOsPolicyAssignment#path}
        :param state: Desired state of the file. Possible values: ["DESIRED_STATE_UNSPECIFIED", "PRESENT", "ABSENT", "CONTENTS_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#state OsConfigOsPolicyAssignment#state}
        :param content: A a file with this content. The size of the content is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#content OsConfigOsPolicyAssignment#content}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#file OsConfigOsPolicyAssignment#file}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile(
            path=path, state=state, content=content, file=file
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="putPkg")
    def put_pkg(
        self,
        *,
        desired_state: builtins.str,
        apt: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt", typing.Dict[builtins.str, typing.Any]]] = None,
        deb: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb", typing.Dict[builtins.str, typing.Any]]] = None,
        googet: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget", typing.Dict[builtins.str, typing.Any]]] = None,
        msi: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi", typing.Dict[builtins.str, typing.Any]]] = None,
        rpm: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param desired_state: The desired state the agent should maintain for this package. Possible values: ["DESIRED_STATE_UNSPECIFIED", "INSTALLED", "REMOVED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#desired_state OsConfigOsPolicyAssignment#desired_state}
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#apt OsConfigOsPolicyAssignment#apt}
        :param deb: deb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#deb OsConfigOsPolicyAssignment#deb}
        :param googet: googet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#googet OsConfigOsPolicyAssignment#googet}
        :param msi: msi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#msi OsConfigOsPolicyAssignment#msi}
        :param rpm: rpm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#rpm OsConfigOsPolicyAssignment#rpm}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#yum OsConfigOsPolicyAssignment#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#zypper OsConfigOsPolicyAssignment#zypper}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg(
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
        apt: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#apt OsConfigOsPolicyAssignment#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#goo OsConfigOsPolicyAssignment#goo}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#yum OsConfigOsPolicyAssignment#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#zypper OsConfigOsPolicyAssignment#zypper}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository(
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
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecOutputReference, jsii.get(self, "exec"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="pkg")
    def pkg(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgOutputReference", jsii.get(self, "pkg"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryOutputReference", jsii.get(self, "repository"))

    @builtins.property
    @jsii.member(jsii_name="execInput")
    def exec_input(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec], jsii.get(self, "execInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="pkgInput")
    def pkg_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg"], jsii.get(self, "pkgInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository"], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3acd3e6dadf57dc953ced6e5063642732b4e1813f49b8c5528bf43b56285fe98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7943b8ad41e5d00c78a6140221318f3272e8c6d26aa4e7269a7db998c4212d62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg",
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
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg:
    def __init__(
        self,
        *,
        desired_state: builtins.str,
        apt: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt", typing.Dict[builtins.str, typing.Any]]] = None,
        deb: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb", typing.Dict[builtins.str, typing.Any]]] = None,
        googet: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget", typing.Dict[builtins.str, typing.Any]]] = None,
        msi: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi", typing.Dict[builtins.str, typing.Any]]] = None,
        rpm: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param desired_state: The desired state the agent should maintain for this package. Possible values: ["DESIRED_STATE_UNSPECIFIED", "INSTALLED", "REMOVED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#desired_state OsConfigOsPolicyAssignment#desired_state}
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#apt OsConfigOsPolicyAssignment#apt}
        :param deb: deb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#deb OsConfigOsPolicyAssignment#deb}
        :param googet: googet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#googet OsConfigOsPolicyAssignment#googet}
        :param msi: msi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#msi OsConfigOsPolicyAssignment#msi}
        :param rpm: rpm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#rpm OsConfigOsPolicyAssignment#rpm}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#yum OsConfigOsPolicyAssignment#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#zypper OsConfigOsPolicyAssignment#zypper}
        '''
        if isinstance(apt, dict):
            apt = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt(**apt)
        if isinstance(deb, dict):
            deb = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb(**deb)
        if isinstance(googet, dict):
            googet = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget(**googet)
        if isinstance(msi, dict):
            msi = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi(**msi)
        if isinstance(rpm, dict):
            rpm = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm(**rpm)
        if isinstance(yum, dict):
            yum = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum(**yum)
        if isinstance(zypper, dict):
            zypper = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper(**zypper)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853dbbd12cdef94f1564385b54856e3ca5d93f50048bde9dae28cf36a1a4043d)
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
        '''The desired state the agent should maintain for this package. Possible values: ["DESIRED_STATE_UNSPECIFIED", "INSTALLED", "REMOVED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#desired_state OsConfigOsPolicyAssignment#desired_state}
        '''
        result = self._values.get("desired_state")
        assert result is not None, "Required property 'desired_state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def apt(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt"]:
        '''apt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#apt OsConfigOsPolicyAssignment#apt}
        '''
        result = self._values.get("apt")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt"], result)

    @builtins.property
    def deb(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb"]:
        '''deb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#deb OsConfigOsPolicyAssignment#deb}
        '''
        result = self._values.get("deb")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb"], result)

    @builtins.property
    def googet(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget"]:
        '''googet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#googet OsConfigOsPolicyAssignment#googet}
        '''
        result = self._values.get("googet")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget"], result)

    @builtins.property
    def msi(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi"]:
        '''msi block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#msi OsConfigOsPolicyAssignment#msi}
        '''
        result = self._values.get("msi")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi"], result)

    @builtins.property
    def rpm(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm"]:
        '''rpm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#rpm OsConfigOsPolicyAssignment#rpm}
        '''
        result = self._values.get("rpm")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm"], result)

    @builtins.property
    def yum(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum"]:
        '''yum block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#yum OsConfigOsPolicyAssignment#yum}
        '''
        result = self._values.get("yum")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum"], result)

    @builtins.property
    def zypper(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper"]:
        '''zypper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#zypper OsConfigOsPolicyAssignment#zypper}
        '''
        result = self._values.get("zypper")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d312926ff33295a897534c05bf30b3b432e168f04dd1bc29fdf928d41711258)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgAptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgAptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d68883c6cf56e5bc7a4222f55ed2475365e260a3ef415c8b10aa9d737eede49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c38e13a749e4c04322169b2d75bb5668f149893aec24ba461df7a8808c7d1fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6977ee0510db2c01f2fa92d8862f26493882fa275a063947807709a14253c8ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "pull_deps": "pullDeps"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb:
    def __init__(
        self,
        *,
        source: typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#source OsConfigOsPolicyAssignment#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'dpkg -i package' - install when true: 'apt-get update && apt-get -y install package.deb' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#pull_deps OsConfigOsPolicyAssignment#pull_deps}
        '''
        if isinstance(source, dict):
            source = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb08d97dda3112ecfb90e5a4b166082cde848d373a0f790a44d929b3d3ed5f82)
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
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#source OsConfigOsPolicyAssignment#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource", result)

    @builtins.property
    def pull_deps(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether dependencies should also be installed.

        - install when false: 'dpkg -i package' - install when true: 'apt-get update && apt-get -y install package.deb'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#pull_deps OsConfigOsPolicyAssignment#pull_deps}
        '''
        result = self._values.get("pull_deps")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43ce03f783fd11bd5d08cd40c8d823b3a5462c20b3ebca6fe0c15d9a06140554)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource(
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
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference", jsii.get(self, "source"))

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
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource"], jsii.get(self, "sourceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f8bf44783c2743b207ca23d34104fd7af5d5f9668daa81ffe445a8ac6d585ea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullDeps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__525031c5cd07c1ea3dadb4f929d42016333fab9d850c36bccce347f6816aace4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02402ce04b3c445ca448e1069482e99f579fa1b65dec9387189206e4b668aeeb)
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
        '''Defaults to false.

        When false, files are subject to validations based on the file type:
        Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7ab1620c060b32b778bd4046c9febaf3ca8e5e5a92d6395a2975a6bceeecf0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[jsii.Number]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__869e16a45698c162b218e8fad01b3b287640a490a52b2b58bf9d3fa3f3f11a90)
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
    def generation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "generationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bb98028814219869cf9afd0010d257174fa83b4b6e6bbb76970a959011323bba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd485253e140627a5270acab1c474184e372db962dd269726bdb994601e692e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5898964874fafdc1458af78ab5c956970dd707a836fd81374d2f5e7f485d63a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a927de27ab49dd493765c179651eeee057648cb066900b41f192b4b72b05e8b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cbd886b2068be09d10fb557ab4b932f718ee084a4e4d34598fe18bc574660ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(
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
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__367852f071de68883c63f00e227ad67238de9ce86950d66c9507ea8b6e3873fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c49dc91eb581ce951026128df7909892a7657aa37c297d06446e4da0e4ee6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c6f2f1dafc627928d0b38e8da66ff7bd91efb571a1184a155bad48278832d3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ea5525d8cd05d1fb7a9aa78536ce1227b76deca0c70b98a0bf473636dc7172)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__883a608684c923deb8dcf76ea199bbe502b154cb5cf7dc015aae7f16e238ac95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__097351658c0d315d7097e5aa6c50a8b8a1e95a1599e711e585ea3063dca205dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457b6a798e0e80e3f5bb1b2c1bf644f1004de62a5521928a8315acd08c0d49de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c79986bb7ab3fe30d32d0d3e7a1c91e5e593e7ec14d4eab5c7ecf5ffdfbff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22088305c4cf5f768d253a7eb63455ef114517d61ad65987ab30e85fd19f87d6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0e5f150e02371f21900bd6d8fb5a67b370c2bd5d447b02afb6c9cd20683f76b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed75e07e5770d74a65a545443c3b2c12a6eec0efa27a3d9ab9cbfbdeb9464a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d2d97ab0d57f2af3157123e74c1aad11cf475cd4488d69e7af343516769ffca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "properties": "properties"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi:
    def __init__(
        self,
        *,
        source: typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource", typing.Dict[builtins.str, typing.Any]],
        properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#source OsConfigOsPolicyAssignment#source}
        :param properties: Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#properties OsConfigOsPolicyAssignment#properties}
        '''
        if isinstance(source, dict):
            source = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f8752a43e6effcae0c2cd31930f85650276a2bd9f467c50abaeb12048f3ec9)
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
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#source OsConfigOsPolicyAssignment#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource", result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional properties to use during installation.

        This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#properties OsConfigOsPolicyAssignment#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35289c2ac75e78b71f28a4128fbff03b1d36ad1a5e471c3c6814b0548e462c12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource(
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
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0155fee8dfdaf43207b2c0db63ee02db23147dd8a0cca76688b00172beb2d8f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b4a4a7b772c93c7703c33ba06032659aad9cd905529b2d55f36681b6b85433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e0b6d34d1924ea29933ad58bc8dc79c6778d4bd041b8fd27033453701af9d7)
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
        '''Defaults to false.

        When false, files are subject to validations based on the file type:
        Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b51bb33629699ce3b4882048a778eeac3a844b64b49675fc21e7c561b621a70)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[jsii.Number]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c99b3857091ae9b6424151e3d89fac57af9db7bb78f53bf3488ec85eabc65fc8)
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
    def generation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "generationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__eb43e22b019ffecffcd7f40cfe50d00f0d23767fa764d29e6dd4b26f4684d065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d288309d241bb35eeca503040d7d72ee1a10f2488f25005b71484db4ee749d1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed003ea6f6d2c83fb7b8d0764499efaa86dafbf1d8c6359d99badda9fe22ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6800702aa74f22b25d4f8504a5f7d3cffe25004569511bbe272d0ac83df4dbd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e960e75402b18a50b1dae9cfa14be580b3598cb1ef7e121e78fcd9c019ccc9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(
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
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0982d49d682014b3dc1af02d1f5936bfc8eed0c12f54abcd659f8375f63081c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65dd6965318b5db597348c01cdca0e9ef809e9d086e1ee23ed5e36ffdc0ecedc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eacfbf7a1cf218f445af572daa2d1c3e8999e52e68eceba14dda033bbfcfb73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021909e4db0f060225b88aec88501c3dee9d8641b99f3ceddb033f88e5f2877b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9be34a26e2b918b4a5bd1105e1f93069167c18c1f3bf3601c95021726ea5b69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe093f86dc604a4221c38dbf2db6b6adde1bd64d9a86956f669d098a5db7ca10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1107aebe108761bc5271925ea9fc9678d02dc5f6debca5fd6d49a63e4f73f9c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d436a31e55ad143b8e9bb8fe4428d47a200d2fd4b8b92be334d1bffe1bc375fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06a2527670ddb2be3a373921314de145c10bd57d775ad13ec4f26c9845b6311b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApt")
    def put_apt(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putApt", [value]))

    @jsii.member(jsii_name="putDeb")
    def put_deb(
        self,
        *,
        source: typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource, typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#source OsConfigOsPolicyAssignment#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'dpkg -i package' - install when true: 'apt-get update && apt-get -y install package.deb' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#pull_deps OsConfigOsPolicyAssignment#pull_deps}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb(
            source=source, pull_deps=pull_deps
        )

        return typing.cast(None, jsii.invoke(self, "putDeb", [value]))

    @jsii.member(jsii_name="putGooget")
    def put_googet(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putGooget", [value]))

    @jsii.member(jsii_name="putMsi")
    def put_msi(
        self,
        *,
        source: typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource, typing.Dict[builtins.str, typing.Any]],
        properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#source OsConfigOsPolicyAssignment#source}
        :param properties: Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#properties OsConfigOsPolicyAssignment#properties}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi(
            source=source, properties=properties
        )

        return typing.cast(None, jsii.invoke(self, "putMsi", [value]))

    @jsii.member(jsii_name="putRpm")
    def put_rpm(
        self,
        *,
        source: typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#source OsConfigOsPolicyAssignment#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'rpm --upgrade --replacepkgs package.rpm' - install when true: 'yum -y install package.rpm' or 'zypper -y install package.rpm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#pull_deps OsConfigOsPolicyAssignment#pull_deps}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm(
            source=source, pull_deps=pull_deps
        )

        return typing.cast(None, jsii.invoke(self, "putRpm", [value]))

    @jsii.member(jsii_name="putYum")
    def put_yum(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putYum", [value]))

    @jsii.member(jsii_name="putZypper")
    def put_zypper(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper(
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
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgAptOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgAptOutputReference, jsii.get(self, "apt"))

    @builtins.property
    @jsii.member(jsii_name="deb")
    def deb(
        self,
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebOutputReference, jsii.get(self, "deb"))

    @builtins.property
    @jsii.member(jsii_name="googet")
    def googet(
        self,
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference, jsii.get(self, "googet"))

    @builtins.property
    @jsii.member(jsii_name="msi")
    def msi(
        self,
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiOutputReference, jsii.get(self, "msi"))

    @builtins.property
    @jsii.member(jsii_name="rpm")
    def rpm(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmOutputReference", jsii.get(self, "rpm"))

    @builtins.property
    @jsii.member(jsii_name="yum")
    def yum(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYumOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYumOutputReference", jsii.get(self, "yum"))

    @builtins.property
    @jsii.member(jsii_name="zypper")
    def zypper(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypperOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypperOutputReference", jsii.get(self, "zypper"))

    @builtins.property
    @jsii.member(jsii_name="aptInput")
    def apt_input(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt], jsii.get(self, "aptInput"))

    @builtins.property
    @jsii.member(jsii_name="debInput")
    def deb_input(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb], jsii.get(self, "debInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="googetInput")
    def googet_input(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget], jsii.get(self, "googetInput"))

    @builtins.property
    @jsii.member(jsii_name="msiInput")
    def msi_input(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi], jsii.get(self, "msiInput"))

    @builtins.property
    @jsii.member(jsii_name="rpmInput")
    def rpm_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm"], jsii.get(self, "rpmInput"))

    @builtins.property
    @jsii.member(jsii_name="yumInput")
    def yum_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum"], jsii.get(self, "yumInput"))

    @builtins.property
    @jsii.member(jsii_name="zypperInput")
    def zypper_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper"], jsii.get(self, "zypperInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3888933c22231dd1b6d29bd318af51d2715d3225a9c1ee406f6e78a2f0a42cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10b730678b15ebeaa4df9bf13242a25fa642a4f4291420d22cbce66166fb134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "pull_deps": "pullDeps"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm:
    def __init__(
        self,
        *,
        source: typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#source OsConfigOsPolicyAssignment#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'rpm --upgrade --replacepkgs package.rpm' - install when true: 'yum -y install package.rpm' or 'zypper -y install package.rpm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#pull_deps OsConfigOsPolicyAssignment#pull_deps}
        '''
        if isinstance(source, dict):
            source = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc15217a040ea720fc76136d766422a96f5a287a60531d78f89fad09453ce15d)
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
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#source OsConfigOsPolicyAssignment#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource", result)

    @builtins.property
    def pull_deps(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether dependencies should also be installed.

        - install when false: 'rpm --upgrade --replacepkgs package.rpm' - install when true: 'yum -y install package.rpm' or 'zypper -y install package.rpm'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#pull_deps OsConfigOsPolicyAssignment#pull_deps}
        '''
        result = self._values.get("pull_deps")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f99d36bf2bef7215b73d84dca750d843cac44e83624eb332aa0f458a3885899)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource(
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
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference", jsii.get(self, "source"))

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
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource"], jsii.get(self, "sourceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4ec08997cf6a763fc5fed92107bdb755e7716f0f6ab2a7bf99357033a547fcae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullDeps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97fb1bab942cb32e37e7b69867b62b06c0a5f2ae0730fc117567114844502a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type: Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1366847537a4ffc926993bae99b952cc71c3f4c6b5ffef874bbc2b6c41de3c95)
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
        '''Defaults to false.

        When false, files are subject to validations based on the file type:
        Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#allow_insecure OsConfigOsPolicyAssignment#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gcs OsConfigOsPolicyAssignment#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#local_path OsConfigOsPolicyAssignment#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#remote OsConfigOsPolicyAssignment#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da5c83cdf681022aad4492f58caa4446475fa21bdb3f5fc34ef6cb5ab0b2c7b2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[jsii.Number]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__263b1d3dacdb46bf944347074f13a77ce999dadaeebf35b6ba4ebf30591cfa78)
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
    def generation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "generationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__58c89587ddacfa1e6fa05d37627a101f7435f17ac08f6388b0fbc7dc8a6d80b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc2f7e67a82c1f85d89e73e39f9510c2072a6dec2aa21701a98303b682ffa8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd9909db01968505a1021172bec2918ca717a7c0c0d7d77edc87ed60ecaa655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__822856183a396830bfcbda328018bef30b1929caadd0290851a8f54312c5305f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dd57b90cfeafb732baeb03c77ccbabd9c7a5a1b784fb5e308b5b6e1a2fc4bda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#bucket OsConfigOsPolicyAssignment#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#object OsConfigOsPolicyAssignment#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#generation OsConfigOsPolicyAssignment#generation}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(
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
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2b0aea430500995299618f882d6d27c046b7548e16c73e1ba1d74cb9c5118725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc950482aa2312c6761029f142dc0310d5137a12740e83ff5d4cd5d1a938cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb1b322c91aecb4e46911579fc7f5de71aa6fc061d3fbd25cc574ccb6bccf15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66a918603f86ab63b8998637da410d9a5e5667d1016b5a7c785b656d3f2566a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#sha256_checksum OsConfigOsPolicyAssignment#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2f797fc6143bfe2fbeb1caab20760b030628921d55ab1bae3a617bcde6e2a16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__119ce704ccd3f7bdca70a66ceeeb3060dac2f8fef356c5e4701a53b449280cf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe8641d49a4715ad919eb2524df0bf8185d84c9c0bb5f219f72d9af6eba41cb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2896f059568f8b85265870fe5eb01036150d2ac62f5d34e2525066c19a656e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32218af49b99c1f221b260eb22afbc50a9c7c729f5278f75079146dd588ac668)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYumOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYumOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b6506dcca50f9f679195726f2e9b5370537e58057f1c5d929379d56a51f6cbc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1f92ff6d70f6b0d73d9ef59f97bc6414b81b67fcab29a5fb9ffce847f0749c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcbfaf90e09faeada2297ff0f57099ec96dd192eb165fa6ad691428b9106b44c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2af9aa47418fd8b2c96b088c8aa9d3997b5ac861c4d2eb3a71e588a96ef3a874)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6a463116d538d81a8f302248b259f091ec7fec567db24596e1c9bc5941dbc54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5f65dccab8d88576d415516cc374a6be6d2c8cf38893df3b9283cd2b072867c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7923e7722ef250e57937d29487fb356c219d52c286a667a0ea4ae6638774bbb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository",
    jsii_struct_bases=[],
    name_mapping={"apt": "apt", "goo": "goo", "yum": "yum", "zypper": "zypper"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository:
    def __init__(
        self,
        *,
        apt: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#apt OsConfigOsPolicyAssignment#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#goo OsConfigOsPolicyAssignment#goo}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#yum OsConfigOsPolicyAssignment#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#zypper OsConfigOsPolicyAssignment#zypper}
        '''
        if isinstance(apt, dict):
            apt = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt(**apt)
        if isinstance(goo, dict):
            goo = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo(**goo)
        if isinstance(yum, dict):
            yum = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum(**yum)
        if isinstance(zypper, dict):
            zypper = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper(**zypper)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bea4abcc8ab43cb02373706dc6e999b7b4ce489c7994466867b3ed139c916b9)
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
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt"]:
        '''apt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#apt OsConfigOsPolicyAssignment#apt}
        '''
        result = self._values.get("apt")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt"], result)

    @builtins.property
    def goo(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo"]:
        '''goo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#goo OsConfigOsPolicyAssignment#goo}
        '''
        result = self._values.get("goo")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo"], result)

    @builtins.property
    def yum(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum"]:
        '''yum block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#yum OsConfigOsPolicyAssignment#yum}
        '''
        result = self._values.get("yum")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum"], result)

    @builtins.property
    def zypper(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper"]:
        '''zypper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#zypper OsConfigOsPolicyAssignment#zypper}
        '''
        result = self._values.get("zypper")
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt",
    jsii_struct_bases=[],
    name_mapping={
        "archive_type": "archiveType",
        "components": "components",
        "distribution": "distribution",
        "uri": "uri",
        "gpg_key": "gpgKey",
    },
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt:
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
        :param archive_type: Type of archive files in this repository. Possible values: ["ARCHIVE_TYPE_UNSPECIFIED", "DEB", "DEB_SRC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#archive_type OsConfigOsPolicyAssignment#archive_type}
        :param components: List of components for this repository. Must contain at least one item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#components OsConfigOsPolicyAssignment#components}
        :param distribution: Distribution of this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#distribution OsConfigOsPolicyAssignment#distribution}
        :param uri: URI for this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param gpg_key: URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gpg_key OsConfigOsPolicyAssignment#gpg_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11270c395540160990927d077d677ad564c836f9ab224e8c12ade9b94ccd4dfc)
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
        '''Type of archive files in this repository. Possible values: ["ARCHIVE_TYPE_UNSPECIFIED", "DEB", "DEB_SRC"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#archive_type OsConfigOsPolicyAssignment#archive_type}
        '''
        result = self._values.get("archive_type")
        assert result is not None, "Required property 'archive_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def components(self) -> typing.List[builtins.str]:
        '''List of components for this repository. Must contain at least one item.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#components OsConfigOsPolicyAssignment#components}
        '''
        result = self._values.get("components")
        assert result is not None, "Required property 'components' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def distribution(self) -> builtins.str:
        '''Distribution of this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#distribution OsConfigOsPolicyAssignment#distribution}
        '''
        result = self._values.get("distribution")
        assert result is not None, "Required property 'distribution' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI for this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gpg_key(self) -> typing.Optional[builtins.str]:
        '''URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gpg_key OsConfigOsPolicyAssignment#gpg_key}
        '''
        result = self._values.get("gpg_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44609df4efd23132931a2e75bc722fe251f95de09d9f052e86e833f658479099)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e518b875e43bafaa1906b006525fb5a445d7041beb56c6d0c4e847a950c3b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "components"))

    @components.setter
    def components(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27acee01b6674de77258fa8f0385c7b66ac311b717c278c623439b81d4666627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distribution"))

    @distribution.setter
    def distribution(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc039bdf9bda195ef64ffe8e6230abb4b618bf6ff5a3d3b6da635c9bc83046b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distribution", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKey")
    def gpg_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpgKey"))

    @gpg_key.setter
    def gpg_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591e1f3fd2b62ba60322eebf952e89cf758bc6cacc185dc22f8c186f9fade466)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92badb12b6ec5d03f5d5de2e9d23a20e617d43963477be5bad04aad9f676f62a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40610a73c91a214a2ba0f2142567f1ad448a8b1fe7e3aefe5520929392491a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "url": "url"},
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo:
    def __init__(self, *, name: builtins.str, url: builtins.str) -> None:
        '''
        :param name: The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        :param url: The url of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#url OsConfigOsPolicyAssignment#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da91c9afa0b3c10f7176ae14eb40a11eaf8c491dc55c10064a5aacf665f02e4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "url": url,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The url of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#url OsConfigOsPolicyAssignment#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c24b68d7c3ddd7d1352144c5d63764dce6d61c464745e182edbcd889ea35f484)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30ce9568eb349bc3e702968d41f1be8e972cbfe40b3e20a4593d78cf9ffc3be1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3b06419f913db0ce8e5eecfd44f5ea3f8798792f1047f3633e42b6d8b50599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37aff432268c809e9b7ef88ef3706e6f705ede7988f69dd1d514386c470c1ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c631f3ece4a5a3873673c848ab64b119b453d0823d22f5e9a34b7a8a7eb26a5)
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
        :param archive_type: Type of archive files in this repository. Possible values: ["ARCHIVE_TYPE_UNSPECIFIED", "DEB", "DEB_SRC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#archive_type OsConfigOsPolicyAssignment#archive_type}
        :param components: List of components for this repository. Must contain at least one item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#components OsConfigOsPolicyAssignment#components}
        :param distribution: Distribution of this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#distribution OsConfigOsPolicyAssignment#distribution}
        :param uri: URI for this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#uri OsConfigOsPolicyAssignment#uri}
        :param gpg_key: URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gpg_key OsConfigOsPolicyAssignment#gpg_key}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt(
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
        :param name: The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#name OsConfigOsPolicyAssignment#name}
        :param url: The url of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#url OsConfigOsPolicyAssignment#url}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo(
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
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#base_url OsConfigOsPolicyAssignment#base_url}
        :param id: A one word, unique name for this repository. This is the 'repo id' in the yum config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for resource conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#id OsConfigOsPolicyAssignment#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#display_name OsConfigOsPolicyAssignment#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gpg_keys OsConfigOsPolicyAssignment#gpg_keys}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum(
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
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#base_url OsConfigOsPolicyAssignment#base_url}
        :param id: A one word, unique name for this repository. This is the 'repo id' in the zypper config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for GuestPolicy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#id OsConfigOsPolicyAssignment#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#display_name OsConfigOsPolicyAssignment#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gpg_keys OsConfigOsPolicyAssignment#gpg_keys}
        '''
        value = OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper(
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
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference, jsii.get(self, "apt"))

    @builtins.property
    @jsii.member(jsii_name="goo")
    def goo(
        self,
    ) -> OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference, jsii.get(self, "goo"))

    @builtins.property
    @jsii.member(jsii_name="yum")
    def yum(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference", jsii.get(self, "yum"))

    @builtins.property
    @jsii.member(jsii_name="zypper")
    def zypper(
        self,
    ) -> "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference":
        return typing.cast("OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference", jsii.get(self, "zypper"))

    @builtins.property
    @jsii.member(jsii_name="aptInput")
    def apt_input(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt], jsii.get(self, "aptInput"))

    @builtins.property
    @jsii.member(jsii_name="gooInput")
    def goo_input(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo], jsii.get(self, "gooInput"))

    @builtins.property
    @jsii.member(jsii_name="yumInput")
    def yum_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum"], jsii.get(self, "yumInput"))

    @builtins.property
    @jsii.member(jsii_name="zypperInput")
    def zypper_input(
        self,
    ) -> typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper"]:
        return typing.cast(typing.Optional["OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper"], jsii.get(self, "zypperInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb068c846d45ab45e958003e62a59a5d4f71bdad34de1269606d9c6b57133e5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum",
    jsii_struct_bases=[],
    name_mapping={
        "base_url": "baseUrl",
        "id": "id",
        "display_name": "displayName",
        "gpg_keys": "gpgKeys",
    },
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum:
    def __init__(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#base_url OsConfigOsPolicyAssignment#base_url}
        :param id: A one word, unique name for this repository. This is the 'repo id' in the yum config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for resource conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#id OsConfigOsPolicyAssignment#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#display_name OsConfigOsPolicyAssignment#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gpg_keys OsConfigOsPolicyAssignment#gpg_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8362911ee6382db2a69c25c21fa3f3cf3aa3f5c169849bddad3fe2ac613fdf9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#base_url OsConfigOsPolicyAssignment#base_url}
        '''
        result = self._values.get("base_url")
        assert result is not None, "Required property 'base_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''A one word, unique name for this repository.

        This is the 'repo id' in the yum config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for resource conflicts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#id OsConfigOsPolicyAssignment#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#display_name OsConfigOsPolicyAssignment#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URIs of GPG keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gpg_keys OsConfigOsPolicyAssignment#gpg_keys}
        '''
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55ab59228b3b9a658291a0d6905ea7fc14f648edd0030cdaf64d7149cf15f57d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a574a83a339dcc23df90bd1ef84b905a8f1555359d79bf2bd7adc77d397bd5d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0f4af2d1115436c903426211197b50c15fb8db287a12897899b88c3db9ee99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKeys")
    def gpg_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gpgKeys"))

    @gpg_keys.setter
    def gpg_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5efb2728c39020898d85dcd13b4b474df0ac153433fe1c623155344a4f21b130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f90226ccc2899bd74fd2b989adcb818876ed09442d75b71c3cac1b66f1bffba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57eff4c26d52f95ce31bc398a299f93d751f131377e44a3966e2fa506b3e8fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper",
    jsii_struct_bases=[],
    name_mapping={
        "base_url": "baseUrl",
        "id": "id",
        "display_name": "displayName",
        "gpg_keys": "gpgKeys",
    },
)
class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper:
    def __init__(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#base_url OsConfigOsPolicyAssignment#base_url}
        :param id: A one word, unique name for this repository. This is the 'repo id' in the zypper config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for GuestPolicy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#id OsConfigOsPolicyAssignment#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#display_name OsConfigOsPolicyAssignment#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gpg_keys OsConfigOsPolicyAssignment#gpg_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a389804257b4acda98b03c6574029443c0fa00032296b322836d7bd7c6bac6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#base_url OsConfigOsPolicyAssignment#base_url}
        '''
        result = self._values.get("base_url")
        assert result is not None, "Required property 'base_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''A one word, unique name for this repository.

        This is the 'repo id' in the zypper config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for GuestPolicy conflicts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#id OsConfigOsPolicyAssignment#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#display_name OsConfigOsPolicyAssignment#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URIs of GPG keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#gpg_keys OsConfigOsPolicyAssignment#gpg_keys}
        '''
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbd827c7f30d151fc7eb3d570cbacbf62416e7b244f2aeed8dbacdf7072db5b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7a6a9964cf0313aa8ad3e19d191597564bb6f7840f3cc13a3aaa844ce2c79de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0dcb05326f4b44f34ffc2eb5ab2b940a6bd370a7a3b12447a407e6d926b2d49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKeys")
    def gpg_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gpgKeys"))

    @gpg_keys.setter
    def gpg_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cabad121947b901421f2d56988ba4ae92fad7157d610d45fddc7f41308678a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9489ed0cd171746ebcc54f7162a729fe732cc89b85a09c95bb4a8cfc2cb1a317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c3fd5c5342581e760784428d1b1076b14f989166d408d536bc6dbb0ccc8417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentRollout",
    jsii_struct_bases=[],
    name_mapping={
        "disruption_budget": "disruptionBudget",
        "min_wait_duration": "minWaitDuration",
    },
)
class OsConfigOsPolicyAssignmentRollout:
    def __init__(
        self,
        *,
        disruption_budget: typing.Union["OsConfigOsPolicyAssignmentRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        min_wait_duration: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#disruption_budget OsConfigOsPolicyAssignment#disruption_budget}
        :param min_wait_duration: This determines the minimum duration of time to wait after the configuration changes are applied through the current rollout. A VM continues to count towards the 'disruption_budget' at least until this duration of time has passed after configuration changes are applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#min_wait_duration OsConfigOsPolicyAssignment#min_wait_duration}
        '''
        if isinstance(disruption_budget, dict):
            disruption_budget = OsConfigOsPolicyAssignmentRolloutDisruptionBudget(**disruption_budget)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb13b70c5d3df5053f7c30afd35c9fb36303b4c4cfcd2e30ad04e4ef083310d)
            check_type(argname="argument disruption_budget", value=disruption_budget, expected_type=type_hints["disruption_budget"])
            check_type(argname="argument min_wait_duration", value=min_wait_duration, expected_type=type_hints["min_wait_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disruption_budget": disruption_budget,
            "min_wait_duration": min_wait_duration,
        }

    @builtins.property
    def disruption_budget(self) -> "OsConfigOsPolicyAssignmentRolloutDisruptionBudget":
        '''disruption_budget block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#disruption_budget OsConfigOsPolicyAssignment#disruption_budget}
        '''
        result = self._values.get("disruption_budget")
        assert result is not None, "Required property 'disruption_budget' is missing"
        return typing.cast("OsConfigOsPolicyAssignmentRolloutDisruptionBudget", result)

    @builtins.property
    def min_wait_duration(self) -> builtins.str:
        '''This determines the minimum duration of time to wait after the configuration changes are applied through the current rollout.

        A VM continues to count towards the 'disruption_budget' at least until this duration of time has passed after configuration changes are applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#min_wait_duration OsConfigOsPolicyAssignment#min_wait_duration}
        '''
        result = self._values.get("min_wait_duration")
        assert result is not None, "Required property 'min_wait_duration' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentRollout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentRolloutDisruptionBudget",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class OsConfigOsPolicyAssignmentRolloutDisruptionBudget:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#fixed OsConfigOsPolicyAssignment#fixed}
        :param percent: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#percent OsConfigOsPolicyAssignment#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f735d3b5bd8cdde9e8b89955e3e847fffb7980560b5bb5eb5821c6b74c53c42e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#fixed OsConfigOsPolicyAssignment#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies the relative value defined as a percentage, which will be multiplied by a reference value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#percent OsConfigOsPolicyAssignment#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentRolloutDisruptionBudget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentRolloutDisruptionBudgetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentRolloutDisruptionBudgetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bc5660dbb8559d9eb4f978de6fe823af2c4fece9def8f7d589deb15f5b6b202)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91184b43cc3124770acf42f27ccd41795b3044cb5f66d84ad6dce99f237793e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602ac46a5b428bc633738f327ca39141e4661fea91d1b675d092863489fe0f0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentRolloutDisruptionBudget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentRolloutDisruptionBudget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3914ef1a8f587b9d7c658648f26b186d9f509bc224ee760d704386ffdd9822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigOsPolicyAssignmentRolloutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentRolloutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adcb2eed66ab99a7b6ef2a1e37b023d76fe451b5db2c268e55fdbbefb626dd51)
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
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#fixed OsConfigOsPolicyAssignment#fixed}
        :param percent: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#percent OsConfigOsPolicyAssignment#percent}
        '''
        value = OsConfigOsPolicyAssignmentRolloutDisruptionBudget(
            fixed=fixed, percent=percent
        )

        return typing.cast(None, jsii.invoke(self, "putDisruptionBudget", [value]))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudget")
    def disruption_budget(
        self,
    ) -> OsConfigOsPolicyAssignmentRolloutDisruptionBudgetOutputReference:
        return typing.cast(OsConfigOsPolicyAssignmentRolloutDisruptionBudgetOutputReference, jsii.get(self, "disruptionBudget"))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudgetInput")
    def disruption_budget_input(
        self,
    ) -> typing.Optional[OsConfigOsPolicyAssignmentRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentRolloutDisruptionBudget], jsii.get(self, "disruptionBudgetInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0b3e7f037b89597c48a98c52d7e534add7f2af2341d15dea8a04bbe5bde1dd5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minWaitDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OsConfigOsPolicyAssignmentRollout]:
        return typing.cast(typing.Optional[OsConfigOsPolicyAssignmentRollout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigOsPolicyAssignmentRollout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1279438b11ad696f96063930e49dd1cecfe5dc3b28b5a5ad1cb626081b61733e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class OsConfigOsPolicyAssignmentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#create OsConfigOsPolicyAssignment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#delete OsConfigOsPolicyAssignment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#update OsConfigOsPolicyAssignment#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6056946e41837e2af73d80f5dd231b978e4ede11f5d6cea0e39ca5f8f9d6b048)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#create OsConfigOsPolicyAssignment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#delete OsConfigOsPolicyAssignment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_os_policy_assignment#update OsConfigOsPolicyAssignment#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigOsPolicyAssignmentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigOsPolicyAssignmentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigOsPolicyAssignment.OsConfigOsPolicyAssignmentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e09d441dd5b985b603a164d3bb2ffb9e2a798caf93f2756def20a4f5163c3890)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86defd756f7f2c559f9e03f22df57b3296f38bd5dff21f2ad648c71ec53ec6f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9a5dc308e9723e658b90ef4d6823e65cb59f7e8ba4273bb45e6b1940d0c6b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d252dd4004b14f51a3ff686df07d34c3182b0b9c903c32eb770216fb234fb8f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd040ef87b11d92af5bf0c86198f82acb82e0312619cc31c80cfbf75a14be5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OsConfigOsPolicyAssignment",
    "OsConfigOsPolicyAssignmentConfig",
    "OsConfigOsPolicyAssignmentInstanceFilter",
    "OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels",
    "OsConfigOsPolicyAssignmentInstanceFilterExclusionLabelsList",
    "OsConfigOsPolicyAssignmentInstanceFilterExclusionLabelsOutputReference",
    "OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels",
    "OsConfigOsPolicyAssignmentInstanceFilterInclusionLabelsList",
    "OsConfigOsPolicyAssignmentInstanceFilterInclusionLabelsOutputReference",
    "OsConfigOsPolicyAssignmentInstanceFilterInventories",
    "OsConfigOsPolicyAssignmentInstanceFilterInventoriesList",
    "OsConfigOsPolicyAssignmentInstanceFilterInventoriesOutputReference",
    "OsConfigOsPolicyAssignmentInstanceFilterOutputReference",
    "OsConfigOsPolicyAssignmentOsPolicies",
    "OsConfigOsPolicyAssignmentOsPoliciesList",
    "OsConfigOsPolicyAssignmentOsPoliciesOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroups",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFiltersList",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFiltersOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsList",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesList",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgAptOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYumOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypperOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper",
    "OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference",
    "OsConfigOsPolicyAssignmentRollout",
    "OsConfigOsPolicyAssignmentRolloutDisruptionBudget",
    "OsConfigOsPolicyAssignmentRolloutDisruptionBudgetOutputReference",
    "OsConfigOsPolicyAssignmentRolloutOutputReference",
    "OsConfigOsPolicyAssignmentTimeouts",
    "OsConfigOsPolicyAssignmentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c2b040bd1a4082f6bf8275131da015e0999e1c2c56c082288ba7c7ef8a47dbb9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_filter: typing.Union[OsConfigOsPolicyAssignmentInstanceFilter, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
    rollout: typing.Union[OsConfigOsPolicyAssignmentRollout, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    skip_await_rollout: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ac053c3e9ce9b1dbda22907a75a13dd182b8a06b3302097d1337f2f64e1398fc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a901d89e3ec383a25bedaa59295941949a1f1b398fac94c3fa5037758fc640e2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de98324b8ffbd34e3657c3634b0f0645f1e813f991f039232aff82dd87fe118(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fca1297f48dc099c8c230b17f02175a322c1c26a79682127046687c65605eca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb358a0f3e6e7b575476bb3a41d78674c798d41abc876077d7b89210b967eb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1942095886d7bc683dc32067e11abe58b1bb80ca25172dec97a450fc2646b15a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3681c16d71bf039ed2e4f12aa1989758229de6dfac9312fad7282fe9ec4164d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f7fcceb13661fa116d09a319572f5a3b8f5b5b6ebc5f1985f38a0311c45f3f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2014c6192095d07ae66e206826c3e6228bc6106936888aec4b135226cf51c2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_filter: typing.Union[OsConfigOsPolicyAssignmentInstanceFilter, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
    rollout: typing.Union[OsConfigOsPolicyAssignmentRollout, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    skip_await_rollout: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43746bfaec4f9ee8fb936a3c7295e0ef77f1a29e2ace3a7badcbe13164f5a0b1(
    *,
    all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b341664f4f3f97f6326b01634dc4de005bf3c6bc05517943ba2e595d74ede19(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc811d25056174a355f35f73a19c902d1fb281585c18b550c30a2683c37d5fc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489c08a46a32796379c33c1580e56e6c12a18849ed1a8dc7f362dfe72cbc52b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fefa3e0c7f3c3486582a052105eb260b34fe221f1f3603f53167ecb87b342cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b838f9d52bd7aa0e73d4a00c386f8c393cfa76c098933f924b33e9f0516429a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840e5288031ffd9bd63197151638af4779e33c0bb4ab978ed087a39c465374c8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec982d26e612a395446ba8c8a55f233a865c8550b537d09390ddc7a3323b094(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ce4bb799086372961e79a570b3803febe5bd96cb7dea75920290f1e7174e8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e45fd43b9651afa755d4a9194dfaac086ed8adf8dba56a23b6e33705658c80ca(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f03a0b71f281d670408148e3ffef390c84ba981de047da7b8ecca88bc730fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4907d06cf094d6a95d050ce7e582752a204dbac770664edefee4328734c9cb43(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df875797187c07d1fad9ba630e52e5a16cbb14a21b57e42691d729377d49b70b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d72a226e2afb89bbb4bc9bee511b510790378ac5295f03aaf44786896c6c98(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8437430821cbe9ec264f8671226a55a286bed4d48faa7e23846131b5ac8891cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5350bb7619b09c7984bf4fa4e83bd484a9ecbedd87a55393e9a1039888d38b37(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca3b8e442683381009eaaa4d3eae44a6463acbe2ffeb8ae05beecacad08d414(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba31f5bc21b2a07c47f2f144d42ed249259789f17e915163317573b94da9100b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98168c363b90ab5599083c37b554f110dac6675b21341ef634a858cbd76f5904(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef3c8f894429e9124e4d19d7517118a399d47c85e1619fdefb447db19e74673(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8b6c7a605478153c5726985c1bddf43be5f5cc07a00a03f01c9395e4d845bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b77fb0efb958887a0008a93491806bb879355c7d29a83d7e912790693df6cc(
    *,
    os_short_name: builtins.str,
    os_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f884ce1ab412707b604d8fc6a2c46d53e50765a7bf79a71367aafb9d239349(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9758d43d4aea457af3a5b3bee454cd022d0e7b3018be01065be6df6e2d0f611e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88bb24d3c8e1872d499e9efeffb9297ba30419b8eb1e6bac82469df8b55a638(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a2644ceee5b5ede3ec81a0328901ec2905458999f8a2149521c3c302e67e19(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2a2833f34bf2957152e59f53052aea9b2893038251a59f7276a4c85d7db6f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa423392881791cd3304712d3c49f73c10f025a1db76567a0a62ad0dedca067(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentInstanceFilterInventories]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0d7c65ed5a8b853fa2a22b7d56140d8c33e6fe5314c6d716d39321da652f55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d143d01d0e31eabf02fe79c7cfdba0efe7d80f25a2d3a0421a60a16318d46f71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d82ebcc9ac48ba862e9497eb0b0e129b4f232072c559da07182b8604cff6b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a3d0fdeebc0b92d2f02787067a2a4b34f14208a51a18db3cd4c63fac3b87ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentInstanceFilterInventories]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae77deaf400089d4672210bc708f8d5d4ca20a6622ce0c62925808c2e3f12136(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93bba52827a03ac7fb9050e85faf668df68ee0cc07c1ca6cfe0622c84c692b76(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41bc4cf4d59478652907fc21250a068c99277c7bd488d5b6c10ebf6c3f22eb9f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0434a4c748d4b556fbb6a8eb79dbef39abebb6c5e6568dbcf05de3cf4e5ec0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504cdcce063b3f66651c5755147528b422018a0c7f1b87f4dd6c0eccce8c8447(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37fe8571127048929312879afdd566e7ccb7185c8c39039fdaeebdb841b4237(
    value: typing.Optional[OsConfigOsPolicyAssignmentInstanceFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e25b3ac630b9b43d238277910b1396dfa8a54f26da465fb5fb4ad4b620167b(
    *,
    id: builtins.str,
    mode: builtins.str,
    resource_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroups, typing.Dict[builtins.str, typing.Any]]]],
    allow_no_resource_group_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1c4578bb552851a4daa6d51710f9c9abc0ce7110bc3eb07bedb991bdf280e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a86a3144072fc468e8653d32573fa4525a7b3c5d28db19ee9770d86eb820fe1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2693c573507f98fba742af31ac6d12a665dff67c2041b5eef3ef98fd432b747e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d420f32770f9354a0a40c97243dd4faff4f20dedf2906523008b0e2f82126b6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d628e7501825b8b2aeabff2f48e7d91350e1cdc3f074bc21c95d03b98ef89cf7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9212b8827002d1823182cb1ce94ecb70630ab2d434c99ad887980e5a6f6463(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263a48520f6c9f1eedd3ed5714935da0501fa8f15e3a8c7ad6ce9daa8a3e8fea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255da8f3a4d6952f8caf36fb3173915d6799226e88f00cbaeaee9b5e2dd79327(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04d1568d52c5b44f13326ecff69a0189ff634a1bd1de39b4587cd0570c32970(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5258fb8c27d818ecb3a49c6dc9781557d6253a6de56766e5e9c564a7b3162ee8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4866f61e95621190bb0ac1ab6c2ec3d0933f5c1d969ecc7664403428d94c2a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac6afb6e14f567b6ce77428bbc865eb715af255124b839ebcecc85c6d3dfd64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b6a57a82f90d68e973f7d16a7455db8012440f1129c0adcfa241d35c1463b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2b2c45c064db466138092f55de202517e6f10af3f3e861bee0e9a9a7199278(
    *,
    resources: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources, typing.Dict[builtins.str, typing.Any]]]],
    inventory_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2df9e7bffda2da0e82a7fe4216b79f8bfaf67f15900818a5fc96112809a076f(
    *,
    os_short_name: builtins.str,
    os_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3be9c11a391d8e7fb9086c3e1b6da95dd1af60358e0f40e73c41a24b14e3d1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05740f9c16ae1454b34b08aa73ec4513be1d2031d949341369a6c6002f0b9756(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b252fb1dee20eea8177f090ff072cc2b80c3cbd948cc8c7f208747319f234e2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d261b517f119904505d4f6e78bfe6651b0f61ee6012db9d4d1c378e51ecc8984(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b705c6c5139462aaa4d4e4c94d18f25d441b52b37671d6ed72fb0d3ce5b9883(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e96d75485f9a4d1bce588de8a3080d352c1a1fbb17e976532a77d32b9d1945(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b949d380c15846ae5e33bbf4c8ed9e8b7897fd8382306cab35dc9e282d59f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2810cfeaaa78f068f8a6dbede9a379130ed80d048391802cfa7dbfe8dd39cc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a543a43c8e0ea75de8a2d0a7b4b2e7492cf87249f0938f19e6aa913a3324cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c657bc5d151642138e344e4b528a41ba83f93b55f614eef060e265641322e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa8a9846e51e9d81f81ea56ad131beab988c7a6be2d4059694c08a6b67fb40f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b672cdf14ed9455f3151d0480c1625cf30cddc3d5fc8295838f3ecfc75e996c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a2cf57be225a991ebb9cdedbe8062d5ae93e3c74deae52b9c63c03e70534bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3828645fe2d42d12d1e1d03537db7b0dfff2dd9102cf25ff180c65cb7ca69f56(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a639f815f8d1dcaf2724fe4cd7d518c55b4987baa22508a22c783f514cfb45(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2a560d14c4db4e47b3973bbcc4020bdbd8d682cfd1bf1ab3e66ee74b913d6d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3307fc6c8efcdd3cd4e412dd93cff7c171fd1782bebff6aec055a049d62073(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ea44654fe1e8ad8f2427662117bc1d435a6c75aa4910e3f612381a9c72d323(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3094a4643e67a0a36d5aebfecd26b4897aaec715b94791583686d047823e8e9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827f0e5cbfb3244fc0335b58d84bec39d82a1985b5f18cd58752d4f7b6ce3f2f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPoliciesResourceGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42c4d9db6723cb5e11d0973e9939e92b3af7121ebc17dc0bab71c7be46e672f(
    *,
    id: builtins.str,
    exec: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec, typing.Dict[builtins.str, typing.Any]]] = None,
    file: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile, typing.Dict[builtins.str, typing.Any]]] = None,
    pkg: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg, typing.Dict[builtins.str, typing.Any]]] = None,
    repository: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63129cf81507b9af52ea018e1ccdd2f17f6fab92e1d51c9b7edc47915046312b(
    *,
    validate: typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate, typing.Dict[builtins.str, typing.Any]],
    enforce: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006f8abca2016ac13407b16d4943109d0ecc1eb136e85da268fba60ae3ecee26(
    *,
    interpreter: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile, typing.Dict[builtins.str, typing.Any]]] = None,
    output_file_path: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9701b900a4ccb816b9c299819813fdcffc846d8826c2d34ebac18676c17c98(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0f2cb47746a9af8dfc756a4a5bea4d9097dee69ced88ba5f6175183899cdb1(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ace4d62e6b80d8c1112c31fbe0bd7a17e36d5c7c58ada13bc5cd3b43b631631(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9db24d2b316464a242cd204120299aabb86bb9d09d522648c2bd0dc7869dcac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774adc1d249918333de88177b6ef3be46d13df77590da503d6e2758a9955863e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78555b3610ae8b51fa544b605bd947932a8ab1c803ffc39abd9b2a2891d1d2b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4632db73ebbccddc48f9e19439c20edcda07c72474afd55992ff787393cdaff7(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d918ed9999267caafba876f5ca541d294f0c813e13b112d7f8b2fba1e6189cda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28572bb233c10bfbf11fc59974c147ed28e6498fc4a67b7c5c8438af541ccd52(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b509a09313cc55584c6f39b8e365692f2dbb9b8b7bccb75b0c14bb191f5d06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e16acc2b073914730037e89d9579c2e4776db520a0b3ad2ecbeadd4ac9d227(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d63b411731f6553a789ba4fe87e9e053046a14db8618225e492aac7d27a2d3(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f57325e7e346080c2f8a608764f8edeb13695e0638da0e933b18b2b96a0b48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3728c5bd2c3e80a8c2a5ede2c7e6a0291ca48462757247d5ae401c949cf5fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db87c43b0aec8e5d4861c5cb68d1b0262f272c5fd6aaf10371ac051f95b74013(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788d5663c1c053cfd5f58633747fc05c3b8cea31d64220972194358289a23b1c(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforceFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00151899d28d5c808a8f71777d450d8a4ea3610616fedc826057e9eae215482b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b1826a4f3e02c1ce9977a33108d98a9d434ec3326fd6a12afee0afd576e28e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e493e67d17c5d1445eb085aa77c7cbc0e133a409a2015c991fae97215e4da30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3509cdd887671d9cce34bb95c8e13046e40948660bb78cc6e87c90e13b8d43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d737c633e5c789bf9ac9f3cf33db67844a5ff6f5d3ccd68e084cbb2c4bfa903(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9e5df5433fec43847eaca3bee4338773df327eed77eead94ddc0e0fd7e5787(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecEnforce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c705c056b0b2c246fccfd35041904f10aefa0202ae3221af737d8428bad1e0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4860cdd9de480d07a3cc7e0ff4b541c293eb12e2a1616385843db9470d1b6fff(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c85ee25fe6100f2743a5a7a19d0d654b014f439d86e4a6a2f6ca86b8c9f52f(
    *,
    interpreter: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile, typing.Dict[builtins.str, typing.Any]]] = None,
    output_file_path: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8b8741e3c87f3aaec1d773d07ef756d5e810af71f31f9c0b5f5f1713e95cd1(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b271f774e5e88e80bfe54e4c8628690e0e030f9ae780ac07448d2bce263587(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee15199446a8075331193c9dc5bce827b53c1af34f8956d86aff41ae0e5247e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2e60f9b63bf19932f80447b485308b43b3de4180272bdb5fbf7501ab9c673c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42b91233e086917e525fae8a457e950a5bf206645109bc97854e5546a4d79f9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7741369c3242e8d58ecad1bf1b44b94427ded7156836f576a6a22c1f8d0df03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0d4c6014509408774bb9fb79e355973f16c8541d832e4deff06ec2deb219c5(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbbe06c149e9f4aee08892b655507b1be90d694f8854566e3f147b8b5d7cd4e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa416aa44d6d0c0d0f9ea91d46c6599844ef2240badc4817695195a0cf84f1b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9439d4c3c25ef3f43c3eb4bafd5e2dbd1c8486b01b93fd4e5fd28ccfba97e16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515146d695a0d4a162d1385a896c35e05edd5da40af8e506e6e421a3a631df9c(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca796599a0eb0da7c4d03739ef2379acd16f26c7f9685519665cf45b5009a54(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f3bc7c12e4071a48b575544d116ea066184433d078f3d341086b7fe521d10a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c9def3d1064ebbde645c5ee7018f869c8cbb23c468c4ef935a66f2d76ea328(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5222e8542f065190561b42aaef2b9f29ddbf564f9c9c12a9be805c82342b6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3488218e943e452c56a7f1020210c3c9a0b6e88a38f2ba6e44f9b497e290d68f(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidateFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f37691edac738acc7471b9102cb78ca7229766559b68b65d645523d70df389(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3b16c00cec64def563b75500849fe28ae34dae6536d7481df010562f318fe9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4fd8f665709a640eea3697c87ab3cd015aa901fdd06807e6fce8ac46486f6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98201a4dc9ca30ce45a1c75514d396ab152b39dd0242ef0b6d5e6c32859bceed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c052d57df353e4bef73d28076589d6878d0c69ba9ae86232432a2f9375acc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74564d8567897c4f690669c27e9f3fb4810775ccf0975cb20a0cc28fee992a2d(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesExecValidate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96a72bafd87717aeadc8e3629a9cd09f707d23963819e92fc59482804c590d8(
    *,
    path: builtins.str,
    state: builtins.str,
    content: typing.Optional[builtins.str] = None,
    file: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab79aad00adb4f010bb7ec52e73a9fb2dfbf18231f2b8e3ae1bf21befa76cf0a(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e49b500dfd6f1fb59d19ed9f51576bdf76b0f765adeaa806634c88634c279002(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0360114d2f0724926e4d8cb9d88e3017e30df274da3e29e850cd595c7d18914e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6da2abca89f9d00d08c66cfe9f5b0465539addd5ad21ce1b1035817f015a53d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2bd7a207d7186219918cb04e8c9843c7bae2907ef62d99cde5428aba0e736c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9b140a25f396cde74d578ddb53d5db1b3ae2c593543e2a1f3f9a930b39189f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2996e3a534ab1aa45f4cf86e79752572a2f968940f90236e1b073de240d49fb(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069bbd34ce8801f00eb0388005c9cdeb451ab6ecc0556c38d29602eeb48a3321(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd8a20bae45f732581bfd8c32c7d91a3e552de75eeb57638f42a3467479c710(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1020367dd20200d2780664159b0725800c6aca926f0909063b0b9563544bcb75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96df7c8b7af0088f9e11dee0f7b606fd72019e167d78671799c9097647de121(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7dd0dae18f9d4a47aa7ba340b0d5102e4532233767862f044da1e8a799b8bba(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e93f1d509df74942dce0cd26478cc40a74302434522a9da5666dd4aa96a234e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e9bd6c7b390da7847f0e556cc82de5c82cb347409d25bee3f5332d6e382674(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9138004b9bb61f1013958463bb703d7538b70df09559d594e1a34d5faebc732a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3825399acbf37cc99ba2aba42f36c5ac792e6c7983048997be8f73684b68d4(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFileFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d3b35ab88036751dc60f2092bec15e8fa0525ecdfb7e2dba573b19f1a6bbf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac222421c683acf44eb9fbe3ab6c4859cdecb4822b6380fc190ca34a2a847bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb61f02f3b76102b9a94d0c1d9396d37323cea49afd1b00584b131fb9b15265(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e8cb863e950f5c0ae3ee975b214376058d4b5874de992d64bed7edc4adf90b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccfd887101b586b66086b04ef96c9150d8cafb29d81b6e83cfbb5e3ff7576ef5(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f213137638be89c02f307db636f0af5c4bd8e7ab9d406c1375776683e36c9d9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a644f6f16bd29a832a31603bc80f5a75b0308dc9c38b4a7c523f3cfe1e2f7022(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd3081d045ff259d54504abb2670c2eb9af6ce12a1b12f74176e4eac24f58f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b479a15edebe26cb2433a5f0b45825811a1fa135ad76758cc008cbdf89c13f53(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e191c9cfeb2055eed1f2b81765f04fdd57726d844b10f753c4153cd4baddc1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af3743212079593249e31e9e2c467a61f5647f6cbb72b0ea020fb82187dfa3c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b82df947d8234c180fcefc97dbc263e19e1ed1219fc25475ca9c0fa867ee6e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3acd3e6dadf57dc953ced6e5063642732b4e1813f49b8c5528bf43b56285fe98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7943b8ad41e5d00c78a6140221318f3272e8c6d26aa4e7269a7db998c4212d62(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853dbbd12cdef94f1564385b54856e3ca5d93f50048bde9dae28cf36a1a4043d(
    *,
    desired_state: builtins.str,
    apt: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt, typing.Dict[builtins.str, typing.Any]]] = None,
    deb: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb, typing.Dict[builtins.str, typing.Any]]] = None,
    googet: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget, typing.Dict[builtins.str, typing.Any]]] = None,
    msi: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi, typing.Dict[builtins.str, typing.Any]]] = None,
    rpm: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm, typing.Dict[builtins.str, typing.Any]]] = None,
    yum: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum, typing.Dict[builtins.str, typing.Any]]] = None,
    zypper: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d312926ff33295a897534c05bf30b3b432e168f04dd1bc29fdf928d41711258(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d68883c6cf56e5bc7a4222f55ed2475365e260a3ef415c8b10aa9d737eede49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c38e13a749e4c04322169b2d75bb5668f149893aec24ba461df7a8808c7d1fa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6977ee0510db2c01f2fa92d8862f26493882fa275a063947807709a14253c8ec(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgApt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb08d97dda3112ecfb90e5a4b166082cde848d373a0f790a44d929b3d3ed5f82(
    *,
    source: typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource, typing.Dict[builtins.str, typing.Any]],
    pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ce03f783fd11bd5d08cd40c8d823b3a5462c20b3ebca6fe0c15d9a06140554(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8bf44783c2743b207ca23d34104fd7af5d5f9668daa81ffe445a8ac6d585ea1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525031c5cd07c1ea3dadb4f929d42016333fab9d850c36bccce347f6816aace4(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDeb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02402ce04b3c445ca448e1069482e99f579fa1b65dec9387189206e4b668aeeb(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7ab1620c060b32b778bd4046c9febaf3ca8e5e5a92d6395a2975a6bceeecf0(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__869e16a45698c162b218e8fad01b3b287640a490a52b2b58bf9d3fa3f3f11a90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb98028814219869cf9afd0010d257174fa83b4b6e6bbb76970a959011323bba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd485253e140627a5270acab1c474184e372db962dd269726bdb994601e692e8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5898964874fafdc1458af78ab5c956970dd707a836fd81374d2f5e7f485d63a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a927de27ab49dd493765c179651eeee057648cb066900b41f192b4b72b05e8b8(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbd886b2068be09d10fb557ab4b932f718ee084a4e4d34598fe18bc574660ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367852f071de68883c63f00e227ad67238de9ce86950d66c9507ea8b6e3873fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c49dc91eb581ce951026128df7909892a7657aa37c297d06446e4da0e4ee6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6f2f1dafc627928d0b38e8da66ff7bd91efb571a1184a155bad48278832d3f(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ea5525d8cd05d1fb7a9aa78536ce1227b76deca0c70b98a0bf473636dc7172(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883a608684c923deb8dcf76ea199bbe502b154cb5cf7dc015aae7f16e238ac95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097351658c0d315d7097e5aa6c50a8b8a1e95a1599e711e585ea3063dca205dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457b6a798e0e80e3f5bb1b2c1bf644f1004de62a5521928a8315acd08c0d49de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c79986bb7ab3fe30d32d0d3e7a1c91e5e593e7ec14d4eab5c7ecf5ffdfbff2(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgDebSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22088305c4cf5f768d253a7eb63455ef114517d61ad65987ab30e85fd19f87d6(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e5f150e02371f21900bd6d8fb5a67b370c2bd5d447b02afb6c9cd20683f76b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed75e07e5770d74a65a545443c3b2c12a6eec0efa27a3d9ab9cbfbdeb9464a3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2d97ab0d57f2af3157123e74c1aad11cf475cd4488d69e7af343516769ffca(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgGooget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f8752a43e6effcae0c2cd31930f85650276a2bd9f467c50abaeb12048f3ec9(
    *,
    source: typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource, typing.Dict[builtins.str, typing.Any]],
    properties: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35289c2ac75e78b71f28a4128fbff03b1d36ad1a5e471c3c6814b0548e462c12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0155fee8dfdaf43207b2c0db63ee02db23147dd8a0cca76688b00172beb2d8f6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b4a4a7b772c93c7703c33ba06032659aad9cd905529b2d55f36681b6b85433(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsi],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e0b6d34d1924ea29933ad58bc8dc79c6778d4bd041b8fd27033453701af9d7(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b51bb33629699ce3b4882048a778eeac3a844b64b49675fc21e7c561b621a70(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99b3857091ae9b6424151e3d89fac57af9db7bb78f53bf3488ec85eabc65fc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb43e22b019ffecffcd7f40cfe50d00f0d23767fa764d29e6dd4b26f4684d065(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d288309d241bb35eeca503040d7d72ee1a10f2488f25005b71484db4ee749d1c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed003ea6f6d2c83fb7b8d0764499efaa86dafbf1d8c6359d99badda9fe22ed6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6800702aa74f22b25d4f8504a5f7d3cffe25004569511bbe272d0ac83df4dbd9(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e960e75402b18a50b1dae9cfa14be580b3598cb1ef7e121e78fcd9c019ccc9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0982d49d682014b3dc1af02d1f5936bfc8eed0c12f54abcd659f8375f63081c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65dd6965318b5db597348c01cdca0e9ef809e9d086e1ee23ed5e36ffdc0ecedc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eacfbf7a1cf218f445af572daa2d1c3e8999e52e68eceba14dda033bbfcfb73(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021909e4db0f060225b88aec88501c3dee9d8641b99f3ceddb033f88e5f2877b(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9be34a26e2b918b4a5bd1105e1f93069167c18c1f3bf3601c95021726ea5b69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe093f86dc604a4221c38dbf2db6b6adde1bd64d9a86956f669d098a5db7ca10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1107aebe108761bc5271925ea9fc9678d02dc5f6debca5fd6d49a63e4f73f9c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d436a31e55ad143b8e9bb8fe4428d47a200d2fd4b8b92be334d1bffe1bc375fb(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a2527670ddb2be3a373921314de145c10bd57d775ad13ec4f26c9845b6311b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3888933c22231dd1b6d29bd318af51d2715d3225a9c1ee406f6e78a2f0a42cc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10b730678b15ebeaa4df9bf13242a25fa642a4f4291420d22cbce66166fb134(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkg],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc15217a040ea720fc76136d766422a96f5a287a60531d78f89fad09453ce15d(
    *,
    source: typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource, typing.Dict[builtins.str, typing.Any]],
    pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f99d36bf2bef7215b73d84dca750d843cac44e83624eb332aa0f458a3885899(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec08997cf6a763fc5fed92107bdb755e7716f0f6ab2a7bf99357033a547fcae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97fb1bab942cb32e37e7b69867b62b06c0a5f2ae0730fc117567114844502a48(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1366847537a4ffc926993bae99b952cc71c3f4c6b5ffef874bbc2b6c41de3c95(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5c83cdf681022aad4492f58caa4446475fa21bdb3f5fc34ef6cb5ab0b2c7b2(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263b1d3dacdb46bf944347074f13a77ce999dadaeebf35b6ba4ebf30591cfa78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c89587ddacfa1e6fa05d37627a101f7435f17ac08f6388b0fbc7dc8a6d80b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc2f7e67a82c1f85d89e73e39f9510c2072a6dec2aa21701a98303b682ffa8b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd9909db01968505a1021172bec2918ca717a7c0c0d7d77edc87ed60ecaa655(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822856183a396830bfcbda328018bef30b1929caadd0290851a8f54312c5305f(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd57b90cfeafb732baeb03c77ccbabd9c7a5a1b784fb5e308b5b6e1a2fc4bda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0aea430500995299618f882d6d27c046b7548e16c73e1ba1d74cb9c5118725(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc950482aa2312c6761029f142dc0310d5137a12740e83ff5d4cd5d1a938cc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb1b322c91aecb4e46911579fc7f5de71aa6fc061d3fbd25cc574ccb6bccf15(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66a918603f86ab63b8998637da410d9a5e5667d1016b5a7c785b656d3f2566a(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f797fc6143bfe2fbeb1caab20760b030628921d55ab1bae3a617bcde6e2a16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119ce704ccd3f7bdca70a66ceeeb3060dac2f8fef356c5e4701a53b449280cf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe8641d49a4715ad919eb2524df0bf8185d84c9c0bb5f219f72d9af6eba41cb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2896f059568f8b85265870fe5eb01036150d2ac62f5d34e2525066c19a656e0(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32218af49b99c1f221b260eb22afbc50a9c7c729f5278f75079146dd588ac668(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6506dcca50f9f679195726f2e9b5370537e58057f1c5d929379d56a51f6cbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f92ff6d70f6b0d73d9ef59f97bc6414b81b67fcab29a5fb9ffce847f0749c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbfaf90e09faeada2297ff0f57099ec96dd192eb165fa6ad691428b9106b44c(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgYum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af9aa47418fd8b2c96b088c8aa9d3997b5ac861c4d2eb3a71e588a96ef3a874(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a463116d538d81a8f302248b259f091ec7fec567db24596e1c9bc5941dbc54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f65dccab8d88576d415516cc374a6be6d2c8cf38893df3b9283cd2b072867c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7923e7722ef250e57937d29487fb356c219d52c286a667a0ea4ae6638774bbb5(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesPkgZypper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bea4abcc8ab43cb02373706dc6e999b7b4ce489c7994466867b3ed139c916b9(
    *,
    apt: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt, typing.Dict[builtins.str, typing.Any]]] = None,
    goo: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo, typing.Dict[builtins.str, typing.Any]]] = None,
    yum: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum, typing.Dict[builtins.str, typing.Any]]] = None,
    zypper: typing.Optional[typing.Union[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11270c395540160990927d077d677ad564c836f9ab224e8c12ade9b94ccd4dfc(
    *,
    archive_type: builtins.str,
    components: typing.Sequence[builtins.str],
    distribution: builtins.str,
    uri: builtins.str,
    gpg_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44609df4efd23132931a2e75bc722fe251f95de09d9f052e86e833f658479099(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e518b875e43bafaa1906b006525fb5a445d7041beb56c6d0c4e847a950c3b77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27acee01b6674de77258fa8f0385c7b66ac311b717c278c623439b81d4666627(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc039bdf9bda195ef64ffe8e6230abb4b618bf6ff5a3d3b6da635c9bc83046b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591e1f3fd2b62ba60322eebf952e89cf758bc6cacc185dc22f8c186f9fade466(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92badb12b6ec5d03f5d5de2e9d23a20e617d43963477be5bad04aad9f676f62a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40610a73c91a214a2ba0f2142567f1ad448a8b1fe7e3aefe5520929392491a5(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryApt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da91c9afa0b3c10f7176ae14eb40a11eaf8c491dc55c10064a5aacf665f02e4(
    *,
    name: builtins.str,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c24b68d7c3ddd7d1352144c5d63764dce6d61c464745e182edbcd889ea35f484(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ce9568eb349bc3e702968d41f1be8e972cbfe40b3e20a4593d78cf9ffc3be1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3b06419f913db0ce8e5eecfd44f5ea3f8798792f1047f3633e42b6d8b50599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37aff432268c809e9b7ef88ef3706e6f705ede7988f69dd1d514386c470c1ae2(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryGoo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c631f3ece4a5a3873673c848ab64b119b453d0823d22f5e9a34b7a8a7eb26a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb068c846d45ab45e958003e62a59a5d4f71bdad34de1269606d9c6b57133e5f(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8362911ee6382db2a69c25c21fa3f3cf3aa3f5c169849bddad3fe2ac613fdf9(
    *,
    base_url: builtins.str,
    id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ab59228b3b9a658291a0d6905ea7fc14f648edd0030cdaf64d7149cf15f57d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a574a83a339dcc23df90bd1ef84b905a8f1555359d79bf2bd7adc77d397bd5d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0f4af2d1115436c903426211197b50c15fb8db287a12897899b88c3db9ee99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5efb2728c39020898d85dcd13b4b474df0ac153433fe1c623155344a4f21b130(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f90226ccc2899bd74fd2b989adcb818876ed09442d75b71c3cac1b66f1bffba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57eff4c26d52f95ce31bc398a299f93d751f131377e44a3966e2fa506b3e8fb(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryYum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a389804257b4acda98b03c6574029443c0fa00032296b322836d7bd7c6bac6(
    *,
    base_url: builtins.str,
    id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd827c7f30d151fc7eb3d570cbacbf62416e7b244f2aeed8dbacdf7072db5b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a6a9964cf0313aa8ad3e19d191597564bb6f7840f3cc13a3aaa844ce2c79de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0dcb05326f4b44f34ffc2eb5ab2b940a6bd370a7a3b12447a407e6d926b2d49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cabad121947b901421f2d56988ba4ae92fad7157d610d45fddc7f41308678a3b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9489ed0cd171746ebcc54f7162a729fe732cc89b85a09c95bb4a8cfc2cb1a317(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c3fd5c5342581e760784428d1b1076b14f989166d408d536bc6dbb0ccc8417(
    value: typing.Optional[OsConfigOsPolicyAssignmentOsPoliciesResourceGroupsResourcesRepositoryZypper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb13b70c5d3df5053f7c30afd35c9fb36303b4c4cfcd2e30ad04e4ef083310d(
    *,
    disruption_budget: typing.Union[OsConfigOsPolicyAssignmentRolloutDisruptionBudget, typing.Dict[builtins.str, typing.Any]],
    min_wait_duration: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f735d3b5bd8cdde9e8b89955e3e847fffb7980560b5bb5eb5821c6b74c53c42e(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc5660dbb8559d9eb4f978de6fe823af2c4fece9def8f7d589deb15f5b6b202(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91184b43cc3124770acf42f27ccd41795b3044cb5f66d84ad6dce99f237793e8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602ac46a5b428bc633738f327ca39141e4661fea91d1b675d092863489fe0f0d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3914ef1a8f587b9d7c658648f26b186d9f509bc224ee760d704386ffdd9822(
    value: typing.Optional[OsConfigOsPolicyAssignmentRolloutDisruptionBudget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adcb2eed66ab99a7b6ef2a1e37b023d76fe451b5db2c268e55fdbbefb626dd51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3e7f037b89597c48a98c52d7e534add7f2af2341d15dea8a04bbe5bde1dd5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1279438b11ad696f96063930e49dd1cecfe5dc3b28b5a5ad1cb626081b61733e(
    value: typing.Optional[OsConfigOsPolicyAssignmentRollout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6056946e41837e2af73d80f5dd231b978e4ede11f5d6cea0e39ca5f8f9d6b048(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09d441dd5b985b603a164d3bb2ffb9e2a798caf93f2756def20a4f5163c3890(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86defd756f7f2c559f9e03f22df57b3296f38bd5dff21f2ad648c71ec53ec6f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9a5dc308e9723e658b90ef4d6823e65cb59f7e8ba4273bb45e6b1940d0c6b95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d252dd4004b14f51a3ff686df07d34c3182b0b9c903c32eb770216fb234fb8f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd040ef87b11d92af5bf0c86198f82acb82e0312619cc31c80cfbf75a14be5b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigOsPolicyAssignmentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
