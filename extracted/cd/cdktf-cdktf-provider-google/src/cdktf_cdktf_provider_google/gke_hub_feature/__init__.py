r'''
# `google_gke_hub_feature`

Refer to the Terraform Registry for docs: [`google_gke_hub_feature`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature).
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


class GkeHubFeature(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeature",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature google_gke_hub_feature}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        fleet_default_member_config: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["GkeHubFeatureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GkeHubFeatureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature google_gke_hub_feature} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#location GkeHubFeature#location}
        :param fleet_default_member_config: fleet_default_member_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#fleet_default_member_config GkeHubFeature#fleet_default_member_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#id GkeHubFeature#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: GCP labels for this Feature. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#labels GkeHubFeature#labels}
        :param name: The full, unique name of this Feature resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#name GkeHubFeature#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#project GkeHubFeature#project}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#spec GkeHubFeature#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#timeouts GkeHubFeature#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15da6eaa3ff0c55b3dff385d70176ea2bd8835bf45ef327deb74c261fd6ac44a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GkeHubFeatureConfig(
            location=location,
            fleet_default_member_config=fleet_default_member_config,
            id=id,
            labels=labels,
            name=name,
            project=project,
            spec=spec,
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
        '''Generates CDKTF code for importing a GkeHubFeature resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeHubFeature to import.
        :param import_from_id: The id of the existing GkeHubFeature that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeHubFeature to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aaea1ebfac8ca28455fa4c0f1b0f746f0c3797b35647135f50498c8df8812c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFleetDefaultMemberConfig")
    def put_fleet_default_member_config(
        self,
        *,
        configmanagement: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigConfigmanagement", typing.Dict[builtins.str, typing.Any]]] = None,
        mesh: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        policycontroller: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontroller", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configmanagement: configmanagement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#configmanagement GkeHubFeature#configmanagement}
        :param mesh: mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#mesh GkeHubFeature#mesh}
        :param policycontroller: policycontroller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policycontroller GkeHubFeature#policycontroller}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfig(
            configmanagement=configmanagement,
            mesh=mesh,
            policycontroller=policycontroller,
        )

        return typing.cast(None, jsii.invoke(self, "putFleetDefaultMemberConfig", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        clusterupgrade: typing.Optional[typing.Union["GkeHubFeatureSpecClusterupgrade", typing.Dict[builtins.str, typing.Any]]] = None,
        fleetobservability: typing.Optional[typing.Union["GkeHubFeatureSpecFleetobservability", typing.Dict[builtins.str, typing.Any]]] = None,
        multiclusteringress: typing.Optional[typing.Union["GkeHubFeatureSpecMulticlusteringress", typing.Dict[builtins.str, typing.Any]]] = None,
        rbacrolebindingactuation: typing.Optional[typing.Union["GkeHubFeatureSpecRbacrolebindingactuation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param clusterupgrade: clusterupgrade block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#clusterupgrade GkeHubFeature#clusterupgrade}
        :param fleetobservability: fleetobservability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#fleetobservability GkeHubFeature#fleetobservability}
        :param multiclusteringress: multiclusteringress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#multiclusteringress GkeHubFeature#multiclusteringress}
        :param rbacrolebindingactuation: rbacrolebindingactuation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#rbacrolebindingactuation GkeHubFeature#rbacrolebindingactuation}
        '''
        value = GkeHubFeatureSpec(
            clusterupgrade=clusterupgrade,
            fleetobservability=fleetobservability,
            multiclusteringress=multiclusteringress,
            rbacrolebindingactuation=rbacrolebindingactuation,
        )

        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#create GkeHubFeature#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#delete GkeHubFeature#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#update GkeHubFeature#update}.
        '''
        value = GkeHubFeatureTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetFleetDefaultMemberConfig")
    def reset_fleet_default_member_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFleetDefaultMemberConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSpec")
    def reset_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpec", []))

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
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="fleetDefaultMemberConfig")
    def fleet_default_member_config(
        self,
    ) -> "GkeHubFeatureFleetDefaultMemberConfigOutputReference":
        return typing.cast("GkeHubFeatureFleetDefaultMemberConfigOutputReference", jsii.get(self, "fleetDefaultMemberConfig"))

    @builtins.property
    @jsii.member(jsii_name="resourceState")
    def resource_state(self) -> "GkeHubFeatureResourceStateList":
        return typing.cast("GkeHubFeatureResourceStateList", jsii.get(self, "resourceState"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "GkeHubFeatureSpecOutputReference":
        return typing.cast("GkeHubFeatureSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> "GkeHubFeatureStateList":
        return typing.cast("GkeHubFeatureStateList", jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GkeHubFeatureTimeoutsOutputReference":
        return typing.cast("GkeHubFeatureTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="fleetDefaultMemberConfigInput")
    def fleet_default_member_config_input(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfig"]:
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfig"], jsii.get(self, "fleetDefaultMemberConfigInput"))

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
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["GkeHubFeatureSpec"]:
        return typing.cast(typing.Optional["GkeHubFeatureSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeHubFeatureTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeHubFeatureTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae9a2ce391dcaa8ee000a5107c326540f8b9c30bea48ffb61b5cfdf21e4bda2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1c4356cc9f935ee9239eef88ebf69a26f09857659e653ec9afc97c6f1a3084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87906e5e9de78c2b73f818d12a9adc4ece5fdcb25a576b7c847697b305fdfbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86172f659954d4ad2a80245204f7c53fc1b655e13d03eba59c7731da1117141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__922739c77119c248f5d1192543d5aff17fef63c95a65453f19cd71901acbfc37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "fleet_default_member_config": "fleetDefaultMemberConfig",
        "id": "id",
        "labels": "labels",
        "name": "name",
        "project": "project",
        "spec": "spec",
        "timeouts": "timeouts",
    },
)
class GkeHubFeatureConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        fleet_default_member_config: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["GkeHubFeatureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GkeHubFeatureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#location GkeHubFeature#location}
        :param fleet_default_member_config: fleet_default_member_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#fleet_default_member_config GkeHubFeature#fleet_default_member_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#id GkeHubFeature#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: GCP labels for this Feature. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#labels GkeHubFeature#labels}
        :param name: The full, unique name of this Feature resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#name GkeHubFeature#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#project GkeHubFeature#project}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#spec GkeHubFeature#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#timeouts GkeHubFeature#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(fleet_default_member_config, dict):
            fleet_default_member_config = GkeHubFeatureFleetDefaultMemberConfig(**fleet_default_member_config)
        if isinstance(spec, dict):
            spec = GkeHubFeatureSpec(**spec)
        if isinstance(timeouts, dict):
            timeouts = GkeHubFeatureTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a972c15bd6c1e15f9e9f64da9624d0c473d944f00af1591b7529f310c108616)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument fleet_default_member_config", value=fleet_default_member_config, expected_type=type_hints["fleet_default_member_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
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
        if fleet_default_member_config is not None:
            self._values["fleet_default_member_config"] = fleet_default_member_config
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name
        if project is not None:
            self._values["project"] = project
        if spec is not None:
            self._values["spec"] = spec
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
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#location GkeHubFeature#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fleet_default_member_config(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfig"]:
        '''fleet_default_member_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#fleet_default_member_config GkeHubFeature#fleet_default_member_config}
        '''
        result = self._values.get("fleet_default_member_config")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#id GkeHubFeature#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''GCP labels for this Feature.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#labels GkeHubFeature#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The full, unique name of this Feature resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#name GkeHubFeature#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#project GkeHubFeature#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(self) -> typing.Optional["GkeHubFeatureSpec"]:
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#spec GkeHubFeature#spec}
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["GkeHubFeatureSpec"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeHubFeatureTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#timeouts GkeHubFeature#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeHubFeatureTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfig",
    jsii_struct_bases=[],
    name_mapping={
        "configmanagement": "configmanagement",
        "mesh": "mesh",
        "policycontroller": "policycontroller",
    },
)
class GkeHubFeatureFleetDefaultMemberConfig:
    def __init__(
        self,
        *,
        configmanagement: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigConfigmanagement", typing.Dict[builtins.str, typing.Any]]] = None,
        mesh: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        policycontroller: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontroller", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configmanagement: configmanagement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#configmanagement GkeHubFeature#configmanagement}
        :param mesh: mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#mesh GkeHubFeature#mesh}
        :param policycontroller: policycontroller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policycontroller GkeHubFeature#policycontroller}
        '''
        if isinstance(configmanagement, dict):
            configmanagement = GkeHubFeatureFleetDefaultMemberConfigConfigmanagement(**configmanagement)
        if isinstance(mesh, dict):
            mesh = GkeHubFeatureFleetDefaultMemberConfigMesh(**mesh)
        if isinstance(policycontroller, dict):
            policycontroller = GkeHubFeatureFleetDefaultMemberConfigPolicycontroller(**policycontroller)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c6c3cb298d5d3abbba7b33fc9cea3023e11cac6602ef4726ff31d133391199)
            check_type(argname="argument configmanagement", value=configmanagement, expected_type=type_hints["configmanagement"])
            check_type(argname="argument mesh", value=mesh, expected_type=type_hints["mesh"])
            check_type(argname="argument policycontroller", value=policycontroller, expected_type=type_hints["policycontroller"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configmanagement is not None:
            self._values["configmanagement"] = configmanagement
        if mesh is not None:
            self._values["mesh"] = mesh
        if policycontroller is not None:
            self._values["policycontroller"] = policycontroller

    @builtins.property
    def configmanagement(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagement"]:
        '''configmanagement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#configmanagement GkeHubFeature#configmanagement}
        '''
        result = self._values.get("configmanagement")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagement"], result)

    @builtins.property
    def mesh(self) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigMesh"]:
        '''mesh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#mesh GkeHubFeature#mesh}
        '''
        result = self._values.get("mesh")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigMesh"], result)

    @builtins.property
    def policycontroller(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontroller"]:
        '''policycontroller block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policycontroller GkeHubFeature#policycontroller}
        '''
        result = self._values.get("policycontroller")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontroller"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagement",
    jsii_struct_bases=[],
    name_mapping={
        "config_sync": "configSync",
        "management": "management",
        "version": "version",
    },
)
class GkeHubFeatureFleetDefaultMemberConfigConfigmanagement:
    def __init__(
        self,
        *,
        config_sync: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync", typing.Dict[builtins.str, typing.Any]]] = None,
        management: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config_sync: config_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#config_sync GkeHubFeature#config_sync}
        :param management: Set this field to MANAGEMENT_AUTOMATIC to enable Config Sync auto-upgrades, and set this field to MANAGEMENT_MANUAL or MANAGEMENT_UNSPECIFIED to disable Config Sync auto-upgrades. Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#management GkeHubFeature#management}
        :param version: Version of Config Sync installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        if isinstance(config_sync, dict):
            config_sync = GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync(**config_sync)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b2618b3fdf90fc25064fbb89ebddfdaa38c42afff93f3abdc040773f5ee8ea)
            check_type(argname="argument config_sync", value=config_sync, expected_type=type_hints["config_sync"])
            check_type(argname="argument management", value=management, expected_type=type_hints["management"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_sync is not None:
            self._values["config_sync"] = config_sync
        if management is not None:
            self._values["management"] = management
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def config_sync(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync"]:
        '''config_sync block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#config_sync GkeHubFeature#config_sync}
        '''
        result = self._values.get("config_sync")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync"], result)

    @builtins.property
    def management(self) -> typing.Optional[builtins.str]:
        '''Set this field to MANAGEMENT_AUTOMATIC to enable Config Sync auto-upgrades, and set this field to MANAGEMENT_MANUAL or MANAGEMENT_UNSPECIFIED to disable Config Sync auto-upgrades.

        Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#management GkeHubFeature#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of Config Sync installed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigConfigmanagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "git": "git",
        "metrics_gcp_service_account_email": "metricsGcpServiceAccountEmail",
        "oci": "oci",
        "prevent_drift": "preventDrift",
        "source_format": "sourceFormat",
    },
)
class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        git: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit", typing.Dict[builtins.str, typing.Any]]] = None,
        metrics_gcp_service_account_email: typing.Optional[builtins.str] = None,
        oci: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci", typing.Dict[builtins.str, typing.Any]]] = None,
        prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enables the installation of ConfigSync. If set to true, ConfigSync resources will be created and the other ConfigSync fields will be applied if exist. If set to false, all other ConfigSync fields will be ignored, ConfigSync resources will be deleted. If omitted, ConfigSync resources will be managed depends on the presence of the git or oci field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#enabled GkeHubFeature#enabled}
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#git GkeHubFeature#git}
        :param metrics_gcp_service_account_email: The Email of the Google Cloud Service Account (GSA) used for exporting Config Sync metrics to Cloud Monitoring. The GSA should have the Monitoring Metric Writer(roles/monitoring.metricWriter) IAM role. The Kubernetes ServiceAccount 'default' in the namespace 'config-management-monitoring' should be bound to the GSA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#metrics_gcp_service_account_email GkeHubFeature#metrics_gcp_service_account_email}
        :param oci: oci block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#oci GkeHubFeature#oci}
        :param prevent_drift: Set to true to enable the Config Sync admission webhook to prevent drifts. If set to 'false', disables the Config Sync admission webhook and does not prevent drifts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#prevent_drift GkeHubFeature#prevent_drift}
        :param source_format: Specifies whether the Config Sync Repo is in hierarchical or unstructured mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#source_format GkeHubFeature#source_format}
        '''
        if isinstance(git, dict):
            git = GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit(**git)
        if isinstance(oci, dict):
            oci = GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci(**oci)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c0aea23d86f0a5e0b6e17a11161be2637487e29297ebb1b70f545ad223a337)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument git", value=git, expected_type=type_hints["git"])
            check_type(argname="argument metrics_gcp_service_account_email", value=metrics_gcp_service_account_email, expected_type=type_hints["metrics_gcp_service_account_email"])
            check_type(argname="argument oci", value=oci, expected_type=type_hints["oci"])
            check_type(argname="argument prevent_drift", value=prevent_drift, expected_type=type_hints["prevent_drift"])
            check_type(argname="argument source_format", value=source_format, expected_type=type_hints["source_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if git is not None:
            self._values["git"] = git
        if metrics_gcp_service_account_email is not None:
            self._values["metrics_gcp_service_account_email"] = metrics_gcp_service_account_email
        if oci is not None:
            self._values["oci"] = oci
        if prevent_drift is not None:
            self._values["prevent_drift"] = prevent_drift
        if source_format is not None:
            self._values["source_format"] = source_format

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the installation of ConfigSync.

        If set to true, ConfigSync resources will be created and the other ConfigSync fields will be applied if exist. If set to false, all other ConfigSync fields will be ignored, ConfigSync resources will be deleted. If omitted, ConfigSync resources will be managed depends on the presence of the git or oci field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#enabled GkeHubFeature#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def git(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit"]:
        '''git block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#git GkeHubFeature#git}
        '''
        result = self._values.get("git")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit"], result)

    @builtins.property
    def metrics_gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''The Email of the Google Cloud Service Account (GSA) used for exporting Config Sync metrics to Cloud Monitoring.

        The GSA should have the Monitoring Metric Writer(roles/monitoring.metricWriter) IAM role. The Kubernetes ServiceAccount 'default' in the namespace 'config-management-monitoring' should be bound to the GSA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#metrics_gcp_service_account_email GkeHubFeature#metrics_gcp_service_account_email}
        '''
        result = self._values.get("metrics_gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oci(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci"]:
        '''oci block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#oci GkeHubFeature#oci}
        '''
        result = self._values.get("oci")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci"], result)

    @builtins.property
    def prevent_drift(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to enable the Config Sync admission webhook to prevent drifts.

        If set to 'false', disables the Config Sync admission webhook and does not prevent drifts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#prevent_drift GkeHubFeature#prevent_drift}
        '''
        result = self._values.get("prevent_drift")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_format(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the Config Sync Repo is in hierarchical or unstructured mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#source_format GkeHubFeature#source_format}
        '''
        result = self._values.get("source_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit",
    jsii_struct_bases=[],
    name_mapping={
        "secret_type": "secretType",
        "gcp_service_account_email": "gcpServiceAccountEmail",
        "https_proxy": "httpsProxy",
        "policy_dir": "policyDir",
        "sync_branch": "syncBranch",
        "sync_repo": "syncRepo",
        "sync_rev": "syncRev",
        "sync_wait_secs": "syncWaitSecs",
    },
)
class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit:
    def __init__(
        self,
        *,
        secret_type: builtins.str,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        sync_branch: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_rev: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_type: Type of secret configured for access to the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#secret_type GkeHubFeature#secret_type}
        :param gcp_service_account_email: The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#gcp_service_account_email GkeHubFeature#gcp_service_account_email}
        :param https_proxy: URL for the HTTPS Proxy to be used when communicating with the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#https_proxy GkeHubFeature#https_proxy}
        :param policy_dir: The path within the Git repository that represents the top level of the repo to sync. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policy_dir GkeHubFeature#policy_dir}
        :param sync_branch: The branch of the repository to sync from. Default: master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_branch GkeHubFeature#sync_branch}
        :param sync_repo: The URL of the Git repository to use as the source of truth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_repo GkeHubFeature#sync_repo}
        :param sync_rev: Git revision (tag or hash) to check out. Default HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_rev GkeHubFeature#sync_rev}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_wait_secs GkeHubFeature#sync_wait_secs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c84c552a77e21b661dc33c9bf0f36cf74727c9adf91b4d2601ab26a2c27556)
            check_type(argname="argument secret_type", value=secret_type, expected_type=type_hints["secret_type"])
            check_type(argname="argument gcp_service_account_email", value=gcp_service_account_email, expected_type=type_hints["gcp_service_account_email"])
            check_type(argname="argument https_proxy", value=https_proxy, expected_type=type_hints["https_proxy"])
            check_type(argname="argument policy_dir", value=policy_dir, expected_type=type_hints["policy_dir"])
            check_type(argname="argument sync_branch", value=sync_branch, expected_type=type_hints["sync_branch"])
            check_type(argname="argument sync_repo", value=sync_repo, expected_type=type_hints["sync_repo"])
            check_type(argname="argument sync_rev", value=sync_rev, expected_type=type_hints["sync_rev"])
            check_type(argname="argument sync_wait_secs", value=sync_wait_secs, expected_type=type_hints["sync_wait_secs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_type": secret_type,
        }
        if gcp_service_account_email is not None:
            self._values["gcp_service_account_email"] = gcp_service_account_email
        if https_proxy is not None:
            self._values["https_proxy"] = https_proxy
        if policy_dir is not None:
            self._values["policy_dir"] = policy_dir
        if sync_branch is not None:
            self._values["sync_branch"] = sync_branch
        if sync_repo is not None:
            self._values["sync_repo"] = sync_repo
        if sync_rev is not None:
            self._values["sync_rev"] = sync_rev
        if sync_wait_secs is not None:
            self._values["sync_wait_secs"] = sync_wait_secs

    @builtins.property
    def secret_type(self) -> builtins.str:
        '''Type of secret configured for access to the Git repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#secret_type GkeHubFeature#secret_type}
        '''
        result = self._values.get("secret_type")
        assert result is not None, "Required property 'secret_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#gcp_service_account_email GkeHubFeature#gcp_service_account_email}
        '''
        result = self._values.get("gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_proxy(self) -> typing.Optional[builtins.str]:
        '''URL for the HTTPS Proxy to be used when communicating with the Git repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#https_proxy GkeHubFeature#https_proxy}
        '''
        result = self._values.get("https_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_dir(self) -> typing.Optional[builtins.str]:
        '''The path within the Git repository that represents the top level of the repo to sync.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policy_dir GkeHubFeature#policy_dir}
        '''
        result = self._values.get("policy_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_branch(self) -> typing.Optional[builtins.str]:
        '''The branch of the repository to sync from. Default: master.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_branch GkeHubFeature#sync_branch}
        '''
        result = self._values.get("sync_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_repo(self) -> typing.Optional[builtins.str]:
        '''The URL of the Git repository to use as the source of truth.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_repo GkeHubFeature#sync_repo}
        '''
        result = self._values.get("sync_repo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_rev(self) -> typing.Optional[builtins.str]:
        '''Git revision (tag or hash) to check out. Default HEAD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_rev GkeHubFeature#sync_rev}
        '''
        result = self._values.get("sync_rev")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_wait_secs(self) -> typing.Optional[builtins.str]:
        '''Period in seconds between consecutive syncs. Default: 15.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_wait_secs GkeHubFeature#sync_wait_secs}
        '''
        result = self._values.get("sync_wait_secs")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff91e5395c7d8494383f90cd73c09d2dd8b49f8b0408245612c2b52b9815babc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGcpServiceAccountEmail")
    def reset_gcp_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpServiceAccountEmail", []))

    @jsii.member(jsii_name="resetHttpsProxy")
    def reset_https_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsProxy", []))

    @jsii.member(jsii_name="resetPolicyDir")
    def reset_policy_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyDir", []))

    @jsii.member(jsii_name="resetSyncBranch")
    def reset_sync_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncBranch", []))

    @jsii.member(jsii_name="resetSyncRepo")
    def reset_sync_repo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncRepo", []))

    @jsii.member(jsii_name="resetSyncRev")
    def reset_sync_rev(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncRev", []))

    @jsii.member(jsii_name="resetSyncWaitSecs")
    def reset_sync_wait_secs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncWaitSecs", []))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmailInput")
    def gcp_service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpServiceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsProxyInput")
    def https_proxy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="policyDirInput")
    def policy_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDirInput"))

    @builtins.property
    @jsii.member(jsii_name="secretTypeInput")
    def secret_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="syncBranchInput")
    def sync_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="syncRepoInput")
    def sync_repo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncRepoInput"))

    @builtins.property
    @jsii.member(jsii_name="syncRevInput")
    def sync_rev_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncRevInput"))

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecsInput")
    def sync_wait_secs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncWaitSecsInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmail")
    def gcp_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccountEmail"))

    @gcp_service_account_email.setter
    def gcp_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__196b0d51f9f540fe5bc003f1a4a3f5f830a78f245d58b6df67a8291babedd3c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsProxy")
    def https_proxy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsProxy"))

    @https_proxy.setter
    def https_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b40806f21bec7a33a3d0a05adc0db6118625cea44a8ed6e7f93c17938cacbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyDir")
    def policy_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDir"))

    @policy_dir.setter
    def policy_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787a7c1a4723d01285e104ffc9a78e7c0fc4878f37dfa1b7c033a4647f59d339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretType")
    def secret_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretType"))

    @secret_type.setter
    def secret_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55d2b640c416d2540e2b93c5d6420d7642ec244062ce1819f1962ddb0a343d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncBranch")
    def sync_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncBranch"))

    @sync_branch.setter
    def sync_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb5515e78bff91ea3fb4fe1bcb228d6579445fb10a28bdd077e74e40b2f0b81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncRepo")
    def sync_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRepo"))

    @sync_repo.setter
    def sync_repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41515055982a396422d049350ebb71da25079c1e73696caa73461890b0467bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRepo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncRev")
    def sync_rev(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRev"))

    @sync_rev.setter
    def sync_rev(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8216d27dda54e295217b0a394961ae66152058b7f93adc6c4a18471bed346862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRev", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecs")
    def sync_wait_secs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncWaitSecs"))

    @sync_wait_secs.setter
    def sync_wait_secs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c2a3cc7605b23f3132ed161966b87a9c1677f4fc79584b44168df3e8c646e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncWaitSecs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdd6231f4960552f423fbff7d1fc3c8ebc66edccb859514c866c5876b6c0dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci",
    jsii_struct_bases=[],
    name_mapping={
        "secret_type": "secretType",
        "gcp_service_account_email": "gcpServiceAccountEmail",
        "policy_dir": "policyDir",
        "sync_repo": "syncRepo",
        "sync_wait_secs": "syncWaitSecs",
        "version": "version",
    },
)
class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci:
    def __init__(
        self,
        *,
        secret_type: builtins.str,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_type: Type of secret configured for access to the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#secret_type GkeHubFeature#secret_type}
        :param gcp_service_account_email: The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#gcp_service_account_email GkeHubFeature#gcp_service_account_email}
        :param policy_dir: The absolute path of the directory that contains the local resources. Default: the root directory of the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policy_dir GkeHubFeature#policy_dir}
        :param sync_repo: The OCI image repository URL for the package to sync from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_repo GkeHubFeature#sync_repo}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_wait_secs GkeHubFeature#sync_wait_secs}
        :param version: Version of Config Sync installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce9168f80bcbf2ed6498d161e113a23c96a174d7f2ebd50d3fd19c0bc5180d0)
            check_type(argname="argument secret_type", value=secret_type, expected_type=type_hints["secret_type"])
            check_type(argname="argument gcp_service_account_email", value=gcp_service_account_email, expected_type=type_hints["gcp_service_account_email"])
            check_type(argname="argument policy_dir", value=policy_dir, expected_type=type_hints["policy_dir"])
            check_type(argname="argument sync_repo", value=sync_repo, expected_type=type_hints["sync_repo"])
            check_type(argname="argument sync_wait_secs", value=sync_wait_secs, expected_type=type_hints["sync_wait_secs"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_type": secret_type,
        }
        if gcp_service_account_email is not None:
            self._values["gcp_service_account_email"] = gcp_service_account_email
        if policy_dir is not None:
            self._values["policy_dir"] = policy_dir
        if sync_repo is not None:
            self._values["sync_repo"] = sync_repo
        if sync_wait_secs is not None:
            self._values["sync_wait_secs"] = sync_wait_secs
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def secret_type(self) -> builtins.str:
        '''Type of secret configured for access to the Git repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#secret_type GkeHubFeature#secret_type}
        '''
        result = self._values.get("secret_type")
        assert result is not None, "Required property 'secret_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#gcp_service_account_email GkeHubFeature#gcp_service_account_email}
        '''
        result = self._values.get("gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_dir(self) -> typing.Optional[builtins.str]:
        '''The absolute path of the directory that contains the local resources. Default: the root directory of the image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policy_dir GkeHubFeature#policy_dir}
        '''
        result = self._values.get("policy_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_repo(self) -> typing.Optional[builtins.str]:
        '''The OCI image repository URL for the package to sync from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_repo GkeHubFeature#sync_repo}
        '''
        result = self._values.get("sync_repo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_wait_secs(self) -> typing.Optional[builtins.str]:
        '''Period in seconds between consecutive syncs. Default: 15.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_wait_secs GkeHubFeature#sync_wait_secs}
        '''
        result = self._values.get("sync_wait_secs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of Config Sync installed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31c15e3ca25981c7f03e2408f1ac7a88101b6a3cebd01fb356eea913dd96892b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGcpServiceAccountEmail")
    def reset_gcp_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpServiceAccountEmail", []))

    @jsii.member(jsii_name="resetPolicyDir")
    def reset_policy_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyDir", []))

    @jsii.member(jsii_name="resetSyncRepo")
    def reset_sync_repo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncRepo", []))

    @jsii.member(jsii_name="resetSyncWaitSecs")
    def reset_sync_wait_secs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncWaitSecs", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmailInput")
    def gcp_service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpServiceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="policyDirInput")
    def policy_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDirInput"))

    @builtins.property
    @jsii.member(jsii_name="secretTypeInput")
    def secret_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="syncRepoInput")
    def sync_repo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncRepoInput"))

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecsInput")
    def sync_wait_secs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncWaitSecsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmail")
    def gcp_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccountEmail"))

    @gcp_service_account_email.setter
    def gcp_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21ec10a1a4ba51ef2af5fec57de8407c6721ed69dd52aa9e03a4b07fbc762b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyDir")
    def policy_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDir"))

    @policy_dir.setter
    def policy_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d5997a29f7a9eed5397903e2a0630110e9d3a9ef9503bd2a4fe6a166593de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretType")
    def secret_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretType"))

    @secret_type.setter
    def secret_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2308501d92e0f66a791e4d27daddfd971712e3a1034dd35a5e98810a5eea6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncRepo")
    def sync_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRepo"))

    @sync_repo.setter
    def sync_repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0925139c6ba0bd061b4ae3c8e19e7eea4c89fd800a55b8d8e638e59bef70ff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRepo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecs")
    def sync_wait_secs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncWaitSecs"))

    @sync_wait_secs.setter
    def sync_wait_secs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c1d3c4621f9d7c9f1a2aca9621a651d5f5027c7e314896431269896fdfedd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncWaitSecs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c2299add112fd41088c3fb23b0e5d70ab93879bdb52c2e1ec3665e6a259868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323b074cd209eb6944e126eb1514a94dac1f8ce03c40a2bab080388f6be6bc4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10866afd9d433a8facfa7d40612b05ad041b1bc7563026466a83f65fa3e15b38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGit")
    def put_git(
        self,
        *,
        secret_type: builtins.str,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        sync_branch: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_rev: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_type: Type of secret configured for access to the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#secret_type GkeHubFeature#secret_type}
        :param gcp_service_account_email: The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#gcp_service_account_email GkeHubFeature#gcp_service_account_email}
        :param https_proxy: URL for the HTTPS Proxy to be used when communicating with the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#https_proxy GkeHubFeature#https_proxy}
        :param policy_dir: The path within the Git repository that represents the top level of the repo to sync. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policy_dir GkeHubFeature#policy_dir}
        :param sync_branch: The branch of the repository to sync from. Default: master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_branch GkeHubFeature#sync_branch}
        :param sync_repo: The URL of the Git repository to use as the source of truth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_repo GkeHubFeature#sync_repo}
        :param sync_rev: Git revision (tag or hash) to check out. Default HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_rev GkeHubFeature#sync_rev}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_wait_secs GkeHubFeature#sync_wait_secs}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit(
            secret_type=secret_type,
            gcp_service_account_email=gcp_service_account_email,
            https_proxy=https_proxy,
            policy_dir=policy_dir,
            sync_branch=sync_branch,
            sync_repo=sync_repo,
            sync_rev=sync_rev,
            sync_wait_secs=sync_wait_secs,
        )

        return typing.cast(None, jsii.invoke(self, "putGit", [value]))

    @jsii.member(jsii_name="putOci")
    def put_oci(
        self,
        *,
        secret_type: builtins.str,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_type: Type of secret configured for access to the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#secret_type GkeHubFeature#secret_type}
        :param gcp_service_account_email: The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#gcp_service_account_email GkeHubFeature#gcp_service_account_email}
        :param policy_dir: The absolute path of the directory that contains the local resources. Default: the root directory of the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policy_dir GkeHubFeature#policy_dir}
        :param sync_repo: The OCI image repository URL for the package to sync from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_repo GkeHubFeature#sync_repo}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#sync_wait_secs GkeHubFeature#sync_wait_secs}
        :param version: Version of Config Sync installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci(
            secret_type=secret_type,
            gcp_service_account_email=gcp_service_account_email,
            policy_dir=policy_dir,
            sync_repo=sync_repo,
            sync_wait_secs=sync_wait_secs,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putOci", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetGit")
    def reset_git(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGit", []))

    @jsii.member(jsii_name="resetMetricsGcpServiceAccountEmail")
    def reset_metrics_gcp_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsGcpServiceAccountEmail", []))

    @jsii.member(jsii_name="resetOci")
    def reset_oci(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOci", []))

    @jsii.member(jsii_name="resetPreventDrift")
    def reset_prevent_drift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreventDrift", []))

    @jsii.member(jsii_name="resetSourceFormat")
    def reset_source_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFormat", []))

    @builtins.property
    @jsii.member(jsii_name="git")
    def git(
        self,
    ) -> GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference, jsii.get(self, "git"))

    @builtins.property
    @jsii.member(jsii_name="oci")
    def oci(
        self,
    ) -> GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference, jsii.get(self, "oci"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="gitInput")
    def git_input(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit], jsii.get(self, "gitInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsGcpServiceAccountEmailInput")
    def metrics_gcp_service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricsGcpServiceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="ociInput")
    def oci_input(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci], jsii.get(self, "ociInput"))

    @builtins.property
    @jsii.member(jsii_name="preventDriftInput")
    def prevent_drift_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preventDriftInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFormatInput")
    def source_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFormatInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f520522133ad2dca70008175fb2d8d47f6e37686334f0b50030f84a8bdb7b177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsGcpServiceAccountEmail")
    def metrics_gcp_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricsGcpServiceAccountEmail"))

    @metrics_gcp_service_account_email.setter
    def metrics_gcp_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae7656f2fc5b93f36760e5aed15d71d7b01c89f99580160bb63bf572289582a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsGcpServiceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preventDrift")
    def prevent_drift(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preventDrift"))

    @prevent_drift.setter
    def prevent_drift(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9886a70546f10fe84a5fff483d135c11c66473ecbd0e20a0607aa7707ee55b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventDrift", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFormat")
    def source_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFormat"))

    @source_format.setter
    def source_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0005589a138e2476a6d151250eda755a236b9174826dce767021f5d8d1fd5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df7297b9140068ea436f0d9e8c411e74ff63b0ea1e3bac1b259544f76e75f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f5e528563f1854bc24f47208a109ce6d765fefe5b5b1d8c9d20b42d1a90d5a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfigSync")
    def put_config_sync(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        git: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit, typing.Dict[builtins.str, typing.Any]]] = None,
        metrics_gcp_service_account_email: typing.Optional[builtins.str] = None,
        oci: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci, typing.Dict[builtins.str, typing.Any]]] = None,
        prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enables the installation of ConfigSync. If set to true, ConfigSync resources will be created and the other ConfigSync fields will be applied if exist. If set to false, all other ConfigSync fields will be ignored, ConfigSync resources will be deleted. If omitted, ConfigSync resources will be managed depends on the presence of the git or oci field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#enabled GkeHubFeature#enabled}
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#git GkeHubFeature#git}
        :param metrics_gcp_service_account_email: The Email of the Google Cloud Service Account (GSA) used for exporting Config Sync metrics to Cloud Monitoring. The GSA should have the Monitoring Metric Writer(roles/monitoring.metricWriter) IAM role. The Kubernetes ServiceAccount 'default' in the namespace 'config-management-monitoring' should be bound to the GSA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#metrics_gcp_service_account_email GkeHubFeature#metrics_gcp_service_account_email}
        :param oci: oci block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#oci GkeHubFeature#oci}
        :param prevent_drift: Set to true to enable the Config Sync admission webhook to prevent drifts. If set to 'false', disables the Config Sync admission webhook and does not prevent drifts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#prevent_drift GkeHubFeature#prevent_drift}
        :param source_format: Specifies whether the Config Sync Repo is in hierarchical or unstructured mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#source_format GkeHubFeature#source_format}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync(
            enabled=enabled,
            git=git,
            metrics_gcp_service_account_email=metrics_gcp_service_account_email,
            oci=oci,
            prevent_drift=prevent_drift,
            source_format=source_format,
        )

        return typing.cast(None, jsii.invoke(self, "putConfigSync", [value]))

    @jsii.member(jsii_name="resetConfigSync")
    def reset_config_sync(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigSync", []))

    @jsii.member(jsii_name="resetManagement")
    def reset_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagement", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="configSync")
    def config_sync(
        self,
    ) -> GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference, jsii.get(self, "configSync"))

    @builtins.property
    @jsii.member(jsii_name="configSyncInput")
    def config_sync_input(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync], jsii.get(self, "configSyncInput"))

    @builtins.property
    @jsii.member(jsii_name="managementInput")
    def management_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managementInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "management"))

    @management.setter
    def management(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__111bc36f79a866a30a99e6fdf914ef74ffeb65988bd8da2fbe7ad38b77052c2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "management", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1075540d3b7fc3741f068a4a4f1022b9d495ceff54c9b9a6b91d72aa29f29a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15bcde01ed2bc266b78a27d6599b009218e3e8edaf01d1a37d49fab108ae1b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigMesh",
    jsii_struct_bases=[],
    name_mapping={"management": "management"},
)
class GkeHubFeatureFleetDefaultMemberConfigMesh:
    def __init__(self, *, management: builtins.str) -> None:
        '''
        :param management: Whether to automatically manage Service Mesh Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#management GkeHubFeature#management}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70aa677d42337c252333b2bb6e9e543e1628acdd851dcfa2b3198a55dcb8e09)
            check_type(argname="argument management", value=management, expected_type=type_hints["management"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "management": management,
        }

    @builtins.property
    def management(self) -> builtins.str:
        '''Whether to automatically manage Service Mesh Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#management GkeHubFeature#management}
        '''
        result = self._values.get("management")
        assert result is not None, "Required property 'management' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigMesh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureFleetDefaultMemberConfigMeshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigMeshOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eed1734dd7111c9c92f93bd59b8e880bc995fe09f06001bb6ce8b06158bc6d14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="managementInput")
    def management_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managementInput"))

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "management"))

    @management.setter
    def management(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb9e2e90cf66625ffb49d6e97ac3e92eba6b16fb920507b37e1c6f7d07cd59ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "management", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigMesh]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigMesh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigMesh],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f31e7c0a95ca8fd5449f298e72bbcc8be66ccc4710cedddf99847b219999a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureFleetDefaultMemberConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bee1feb5904aedc22f8e0941935b9df22576374ea2ba206d55bed9109d999bc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfigmanagement")
    def put_configmanagement(
        self,
        *,
        config_sync: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync, typing.Dict[builtins.str, typing.Any]]] = None,
        management: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config_sync: config_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#config_sync GkeHubFeature#config_sync}
        :param management: Set this field to MANAGEMENT_AUTOMATIC to enable Config Sync auto-upgrades, and set this field to MANAGEMENT_MANUAL or MANAGEMENT_UNSPECIFIED to disable Config Sync auto-upgrades. Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#management GkeHubFeature#management}
        :param version: Version of Config Sync installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigConfigmanagement(
            config_sync=config_sync, management=management, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putConfigmanagement", [value]))

    @jsii.member(jsii_name="putMesh")
    def put_mesh(self, *, management: builtins.str) -> None:
        '''
        :param management: Whether to automatically manage Service Mesh Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#management GkeHubFeature#management}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigMesh(management=management)

        return typing.cast(None, jsii.invoke(self, "putMesh", [value]))

    @jsii.member(jsii_name="putPolicycontroller")
    def put_policycontroller(
        self,
        *,
        policy_controller_hub_config: typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig", typing.Dict[builtins.str, typing.Any]],
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param policy_controller_hub_config: policy_controller_hub_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policy_controller_hub_config GkeHubFeature#policy_controller_hub_config}
        :param version: Configures the version of Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigPolicycontroller(
            policy_controller_hub_config=policy_controller_hub_config, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putPolicycontroller", [value]))

    @jsii.member(jsii_name="resetConfigmanagement")
    def reset_configmanagement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigmanagement", []))

    @jsii.member(jsii_name="resetMesh")
    def reset_mesh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMesh", []))

    @jsii.member(jsii_name="resetPolicycontroller")
    def reset_policycontroller(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicycontroller", []))

    @builtins.property
    @jsii.member(jsii_name="configmanagement")
    def configmanagement(
        self,
    ) -> GkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference, jsii.get(self, "configmanagement"))

    @builtins.property
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> GkeHubFeatureFleetDefaultMemberConfigMeshOutputReference:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigMeshOutputReference, jsii.get(self, "mesh"))

    @builtins.property
    @jsii.member(jsii_name="policycontroller")
    def policycontroller(
        self,
    ) -> "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerOutputReference":
        return typing.cast("GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerOutputReference", jsii.get(self, "policycontroller"))

    @builtins.property
    @jsii.member(jsii_name="configmanagementInput")
    def configmanagement_input(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement], jsii.get(self, "configmanagementInput"))

    @builtins.property
    @jsii.member(jsii_name="meshInput")
    def mesh_input(self) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigMesh]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigMesh], jsii.get(self, "meshInput"))

    @builtins.property
    @jsii.member(jsii_name="policycontrollerInput")
    def policycontroller_input(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontroller"]:
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontroller"], jsii.get(self, "policycontrollerInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cfcbef1a6482f9561f8124ac2c93a3bd22c7b53e212f7c4bf06552a7d9e8612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontroller",
    jsii_struct_bases=[],
    name_mapping={
        "policy_controller_hub_config": "policyControllerHubConfig",
        "version": "version",
    },
)
class GkeHubFeatureFleetDefaultMemberConfigPolicycontroller:
    def __init__(
        self,
        *,
        policy_controller_hub_config: typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig", typing.Dict[builtins.str, typing.Any]],
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param policy_controller_hub_config: policy_controller_hub_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policy_controller_hub_config GkeHubFeature#policy_controller_hub_config}
        :param version: Configures the version of Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        if isinstance(policy_controller_hub_config, dict):
            policy_controller_hub_config = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig(**policy_controller_hub_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9f161a2695f43e400b81e3a28c43ce3d956b7c70c6793391a2e84e9197e139)
            check_type(argname="argument policy_controller_hub_config", value=policy_controller_hub_config, expected_type=type_hints["policy_controller_hub_config"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_controller_hub_config": policy_controller_hub_config,
        }
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def policy_controller_hub_config(
        self,
    ) -> "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig":
        '''policy_controller_hub_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policy_controller_hub_config GkeHubFeature#policy_controller_hub_config}
        '''
        result = self._values.get("policy_controller_hub_config")
        assert result is not None, "Required property 'policy_controller_hub_config' is missing"
        return typing.cast("GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig", result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Configures the version of Policy Controller.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigPolicycontroller(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e66cc4cfe66b1018e24861ab4e00451da445fd484900e7c29883c71160935536)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPolicyControllerHubConfig")
    def put_policy_controller_hub_config(
        self,
        *,
        install_spec: builtins.str,
        audit_interval_seconds: typing.Optional[jsii.Number] = None,
        constraint_violation_limit: typing.Optional[jsii.Number] = None,
        deployment_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_content: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent", typing.Dict[builtins.str, typing.Any]]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param install_spec: Configures the mode of the Policy Controller installation Possible values: ["INSTALL_SPEC_UNSPECIFIED", "INSTALL_SPEC_NOT_INSTALLED", "INSTALL_SPEC_ENABLED", "INSTALL_SPEC_SUSPENDED", "INSTALL_SPEC_DETACHED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#install_spec GkeHubFeature#install_spec}
        :param audit_interval_seconds: Interval for Policy Controller Audit scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#audit_interval_seconds GkeHubFeature#audit_interval_seconds}
        :param constraint_violation_limit: The maximum number of audit violations to be stored in a constraint. If not set, the internal default of 20 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#constraint_violation_limit GkeHubFeature#constraint_violation_limit}
        :param deployment_configs: deployment_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#deployment_configs GkeHubFeature#deployment_configs}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#exemptable_namespaces GkeHubFeature#exemptable_namespaces}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#log_denies_enabled GkeHubFeature#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#monitoring GkeHubFeature#monitoring}
        :param mutation_enabled: Enables the ability to mutate resources using Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#mutation_enabled GkeHubFeature#mutation_enabled}
        :param policy_content: policy_content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policy_content GkeHubFeature#policy_content}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#referential_rules_enabled GkeHubFeature#referential_rules_enabled}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig(
            install_spec=install_spec,
            audit_interval_seconds=audit_interval_seconds,
            constraint_violation_limit=constraint_violation_limit,
            deployment_configs=deployment_configs,
            exemptable_namespaces=exemptable_namespaces,
            log_denies_enabled=log_denies_enabled,
            monitoring=monitoring,
            mutation_enabled=mutation_enabled,
            policy_content=policy_content,
            referential_rules_enabled=referential_rules_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putPolicyControllerHubConfig", [value]))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="policyControllerHubConfig")
    def policy_controller_hub_config(
        self,
    ) -> "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigOutputReference":
        return typing.cast("GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigOutputReference", jsii.get(self, "policyControllerHubConfig"))

    @builtins.property
    @jsii.member(jsii_name="policyControllerHubConfigInput")
    def policy_controller_hub_config_input(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig"]:
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig"], jsii.get(self, "policyControllerHubConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcbfbaa2f36d419131ec3e994856e923e557d6a1289a9b1e0262abc8a10c9bd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontroller]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontroller], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontroller],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49c8d47f340f96b635824cc28309d83eef0f9171bd35019e21b9ab4993c29565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig",
    jsii_struct_bases=[],
    name_mapping={
        "install_spec": "installSpec",
        "audit_interval_seconds": "auditIntervalSeconds",
        "constraint_violation_limit": "constraintViolationLimit",
        "deployment_configs": "deploymentConfigs",
        "exemptable_namespaces": "exemptableNamespaces",
        "log_denies_enabled": "logDeniesEnabled",
        "monitoring": "monitoring",
        "mutation_enabled": "mutationEnabled",
        "policy_content": "policyContent",
        "referential_rules_enabled": "referentialRulesEnabled",
    },
)
class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig:
    def __init__(
        self,
        *,
        install_spec: builtins.str,
        audit_interval_seconds: typing.Optional[jsii.Number] = None,
        constraint_violation_limit: typing.Optional[jsii.Number] = None,
        deployment_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_content: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent", typing.Dict[builtins.str, typing.Any]]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param install_spec: Configures the mode of the Policy Controller installation Possible values: ["INSTALL_SPEC_UNSPECIFIED", "INSTALL_SPEC_NOT_INSTALLED", "INSTALL_SPEC_ENABLED", "INSTALL_SPEC_SUSPENDED", "INSTALL_SPEC_DETACHED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#install_spec GkeHubFeature#install_spec}
        :param audit_interval_seconds: Interval for Policy Controller Audit scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#audit_interval_seconds GkeHubFeature#audit_interval_seconds}
        :param constraint_violation_limit: The maximum number of audit violations to be stored in a constraint. If not set, the internal default of 20 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#constraint_violation_limit GkeHubFeature#constraint_violation_limit}
        :param deployment_configs: deployment_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#deployment_configs GkeHubFeature#deployment_configs}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#exemptable_namespaces GkeHubFeature#exemptable_namespaces}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#log_denies_enabled GkeHubFeature#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#monitoring GkeHubFeature#monitoring}
        :param mutation_enabled: Enables the ability to mutate resources using Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#mutation_enabled GkeHubFeature#mutation_enabled}
        :param policy_content: policy_content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policy_content GkeHubFeature#policy_content}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#referential_rules_enabled GkeHubFeature#referential_rules_enabled}
        '''
        if isinstance(monitoring, dict):
            monitoring = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring(**monitoring)
        if isinstance(policy_content, dict):
            policy_content = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent(**policy_content)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447e41a47606b2d9b5fe8524d4cd9fb7a69d777411335bb221ff82ce9d2a6cc5)
            check_type(argname="argument install_spec", value=install_spec, expected_type=type_hints["install_spec"])
            check_type(argname="argument audit_interval_seconds", value=audit_interval_seconds, expected_type=type_hints["audit_interval_seconds"])
            check_type(argname="argument constraint_violation_limit", value=constraint_violation_limit, expected_type=type_hints["constraint_violation_limit"])
            check_type(argname="argument deployment_configs", value=deployment_configs, expected_type=type_hints["deployment_configs"])
            check_type(argname="argument exemptable_namespaces", value=exemptable_namespaces, expected_type=type_hints["exemptable_namespaces"])
            check_type(argname="argument log_denies_enabled", value=log_denies_enabled, expected_type=type_hints["log_denies_enabled"])
            check_type(argname="argument monitoring", value=monitoring, expected_type=type_hints["monitoring"])
            check_type(argname="argument mutation_enabled", value=mutation_enabled, expected_type=type_hints["mutation_enabled"])
            check_type(argname="argument policy_content", value=policy_content, expected_type=type_hints["policy_content"])
            check_type(argname="argument referential_rules_enabled", value=referential_rules_enabled, expected_type=type_hints["referential_rules_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "install_spec": install_spec,
        }
        if audit_interval_seconds is not None:
            self._values["audit_interval_seconds"] = audit_interval_seconds
        if constraint_violation_limit is not None:
            self._values["constraint_violation_limit"] = constraint_violation_limit
        if deployment_configs is not None:
            self._values["deployment_configs"] = deployment_configs
        if exemptable_namespaces is not None:
            self._values["exemptable_namespaces"] = exemptable_namespaces
        if log_denies_enabled is not None:
            self._values["log_denies_enabled"] = log_denies_enabled
        if monitoring is not None:
            self._values["monitoring"] = monitoring
        if mutation_enabled is not None:
            self._values["mutation_enabled"] = mutation_enabled
        if policy_content is not None:
            self._values["policy_content"] = policy_content
        if referential_rules_enabled is not None:
            self._values["referential_rules_enabled"] = referential_rules_enabled

    @builtins.property
    def install_spec(self) -> builtins.str:
        '''Configures the mode of the Policy Controller installation Possible values: ["INSTALL_SPEC_UNSPECIFIED", "INSTALL_SPEC_NOT_INSTALLED", "INSTALL_SPEC_ENABLED", "INSTALL_SPEC_SUSPENDED", "INSTALL_SPEC_DETACHED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#install_spec GkeHubFeature#install_spec}
        '''
        result = self._values.get("install_spec")
        assert result is not None, "Required property 'install_spec' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audit_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''Interval for Policy Controller Audit scans (in seconds). When set to 0, this disables audit functionality altogether.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#audit_interval_seconds GkeHubFeature#audit_interval_seconds}
        '''
        result = self._values.get("audit_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def constraint_violation_limit(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of audit violations to be stored in a constraint.

        If not set, the internal default of 20 will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#constraint_violation_limit GkeHubFeature#constraint_violation_limit}
        '''
        result = self._values.get("constraint_violation_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def deployment_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs"]]]:
        '''deployment_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#deployment_configs GkeHubFeature#deployment_configs}
        '''
        result = self._values.get("deployment_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs"]]], result)

    @builtins.property
    def exemptable_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of namespaces that are excluded from Policy Controller checks.

        Namespaces do not need to currently exist on the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#exemptable_namespaces GkeHubFeature#exemptable_namespaces}
        '''
        result = self._values.get("exemptable_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def log_denies_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Logs all denies and dry run failures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#log_denies_enabled GkeHubFeature#log_denies_enabled}
        '''
        result = self._values.get("log_denies_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monitoring(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring"]:
        '''monitoring block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#monitoring GkeHubFeature#monitoring}
        '''
        result = self._values.get("monitoring")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring"], result)

    @builtins.property
    def mutation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the ability to mutate resources using Policy Controller.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#mutation_enabled GkeHubFeature#mutation_enabled}
        '''
        result = self._values.get("mutation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def policy_content(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent"]:
        '''policy_content block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#policy_content GkeHubFeature#policy_content}
        '''
        result = self._values.get("policy_content")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent"], result)

    @builtins.property
    def referential_rules_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#referential_rules_enabled GkeHubFeature#referential_rules_enabled}
        '''
        result = self._values.get("referential_rules_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "component": "component",
        "container_resources": "containerResources",
        "pod_affinity": "podAffinity",
        "pod_toleration": "podToleration",
        "replica_count": "replicaCount",
    },
)
class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs:
    def __init__(
        self,
        *,
        component: builtins.str,
        container_resources: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources", typing.Dict[builtins.str, typing.Any]]] = None,
        pod_affinity: typing.Optional[builtins.str] = None,
        pod_toleration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param component: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#component GkeHubFeature#component}.
        :param container_resources: container_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#container_resources GkeHubFeature#container_resources}
        :param pod_affinity: Pod affinity configuration. Possible values: ["AFFINITY_UNSPECIFIED", "NO_AFFINITY", "ANTI_AFFINITY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#pod_affinity GkeHubFeature#pod_affinity}
        :param pod_toleration: pod_toleration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#pod_toleration GkeHubFeature#pod_toleration}
        :param replica_count: Pod replica count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#replica_count GkeHubFeature#replica_count}
        '''
        if isinstance(container_resources, dict):
            container_resources = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources(**container_resources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430ea392a5df56d4a0343a947ca4f046e6175acec57f22f236b55f7712fbfe2d)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
            check_type(argname="argument container_resources", value=container_resources, expected_type=type_hints["container_resources"])
            check_type(argname="argument pod_affinity", value=pod_affinity, expected_type=type_hints["pod_affinity"])
            check_type(argname="argument pod_toleration", value=pod_toleration, expected_type=type_hints["pod_toleration"])
            check_type(argname="argument replica_count", value=replica_count, expected_type=type_hints["replica_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "component": component,
        }
        if container_resources is not None:
            self._values["container_resources"] = container_resources
        if pod_affinity is not None:
            self._values["pod_affinity"] = pod_affinity
        if pod_toleration is not None:
            self._values["pod_toleration"] = pod_toleration
        if replica_count is not None:
            self._values["replica_count"] = replica_count

    @builtins.property
    def component(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#component GkeHubFeature#component}.'''
        result = self._values.get("component")
        assert result is not None, "Required property 'component' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_resources(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources"]:
        '''container_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#container_resources GkeHubFeature#container_resources}
        '''
        result = self._values.get("container_resources")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources"], result)

    @builtins.property
    def pod_affinity(self) -> typing.Optional[builtins.str]:
        '''Pod affinity configuration. Possible values: ["AFFINITY_UNSPECIFIED", "NO_AFFINITY", "ANTI_AFFINITY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#pod_affinity GkeHubFeature#pod_affinity}
        '''
        result = self._values.get("pod_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_toleration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration"]]]:
        '''pod_toleration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#pod_toleration GkeHubFeature#pod_toleration}
        '''
        result = self._values.get("pod_toleration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration"]]], result)

    @builtins.property
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''Pod replica count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#replica_count GkeHubFeature#replica_count}
        '''
        result = self._values.get("replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources",
    jsii_struct_bases=[],
    name_mapping={"limits": "limits", "requests": "requests"},
)
class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources:
    def __init__(
        self,
        *,
        limits: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        requests: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#limits GkeHubFeature#limits}
        :param requests: requests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#requests GkeHubFeature#requests}
        '''
        if isinstance(limits, dict):
            limits = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits(**limits)
        if isinstance(requests, dict):
            requests = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests(**requests)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0dafe1580a680953fd5b0e9a032d04cf98903d9944c71d391b9d9f37d61ab0)
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument requests", value=requests, expected_type=type_hints["requests"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if limits is not None:
            self._values["limits"] = limits
        if requests is not None:
            self._values["requests"] = requests

    @builtins.property
    def limits(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits"]:
        '''limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#limits GkeHubFeature#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits"], result)

    @builtins.property
    def requests(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"]:
        '''requests block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#requests GkeHubFeature#requests}
        '''
        result = self._values.get("requests")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory"},
)
class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#cpu GkeHubFeature#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#memory GkeHubFeature#memory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea24db54bd9f12c4481fa9360948b13e78f5799ce1cb26225a6021962d0c1e8)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory is not None:
            self._values["memory"] = memory

    @builtins.property
    def cpu(self) -> typing.Optional[builtins.str]:
        '''CPU requirement expressed in Kubernetes resource units.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#cpu GkeHubFeature#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Memory requirement expressed in Kubernetes resource units.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#memory GkeHubFeature#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5459cdd52863d93d971376103e2cef0f3694465da483187cb5099e92672487e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73603818615be005ca7e6b1b7c1b169220f2c2294b170542bdb30719f157edad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b639f109076f65ed2f9f0c10fedfe619eba6736b4b5707dcc08fbc83d4fff31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da822abfd060659b2ede0f6220491eab6c94b872ee8e5686f9950a441af66ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__785e0c816a5faf65106910f5c55b538c29bd7b5ef96a6db35f8a8e7ded009e82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLimits")
    def put_limits(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#cpu GkeHubFeature#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#memory GkeHubFeature#memory}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits(
            cpu=cpu, memory=memory
        )

        return typing.cast(None, jsii.invoke(self, "putLimits", [value]))

    @jsii.member(jsii_name="putRequests")
    def put_requests(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#cpu GkeHubFeature#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#memory GkeHubFeature#memory}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests(
            cpu=cpu, memory=memory
        )

        return typing.cast(None, jsii.invoke(self, "putRequests", [value]))

    @jsii.member(jsii_name="resetLimits")
    def reset_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimits", []))

    @jsii.member(jsii_name="resetRequests")
    def reset_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequests", []))

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(
        self,
    ) -> GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference, jsii.get(self, "limits"))

    @builtins.property
    @jsii.member(jsii_name="requests")
    def requests(
        self,
    ) -> "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference":
        return typing.cast("GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference", jsii.get(self, "requests"))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="requestsInput")
    def requests_input(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"]:
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"], jsii.get(self, "requestsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0470ca1b291c9c152f186b71ecd90f6bdb06de859743965424b1af72784860e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory"},
)
class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#cpu GkeHubFeature#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#memory GkeHubFeature#memory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23ff8f0d97dc9ab1f38e7a01eb92488e3e1eb1f58dded23192819c880b5a310)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory is not None:
            self._values["memory"] = memory

    @builtins.property
    def cpu(self) -> typing.Optional[builtins.str]:
        '''CPU requirement expressed in Kubernetes resource units.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#cpu GkeHubFeature#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Memory requirement expressed in Kubernetes resource units.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#memory GkeHubFeature#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fc2a40f229f855884a0244e612350b9db552abb6a0c408062fc8ae7876efc50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf95f5c396106923fe3a1ebbdb04a8c21151e1f426db058b1ea15dbfd964c46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c2530aa4c8c1f8c0d5b02dba3778f7e87ef8fa5f095bf71ca5bb9b8f826b73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__626b155db1e76429da17e8f180f16545c681dfdfa224d955679a6884ee64bc1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b07fa20cc776000ba8e8c4d79aad80350bf26248b11f44bb88824017839c1ccf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edea6db951330fe988334aa18105538c165abb8ab1cc867e83847a0579228f8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33fdef95f40fe5aab7189cbc2527e97e3814982fa0c4a0b10b68fb20c626d126)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3afb9cc8951ee966e0b2ef17240b0507b7972b866e0f1ed7ae4b268863fb45dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f38b724837cbe88d12be4c9a763dee4c3ad6bcbb7ba45a666b6ac4fdc9863df6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e83f671a363e06964de082cd3a7552fcdca0bf3b33908fe293160416ac31c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c1eb80ef609bd0eb39030367174306afac4dccc69432ce665e96fa5932438c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putContainerResources")
    def put_container_resources(
        self,
        *,
        limits: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits, typing.Dict[builtins.str, typing.Any]]] = None,
        requests: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#limits GkeHubFeature#limits}
        :param requests: requests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#requests GkeHubFeature#requests}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources(
            limits=limits, requests=requests
        )

        return typing.cast(None, jsii.invoke(self, "putContainerResources", [value]))

    @jsii.member(jsii_name="putPodToleration")
    def put_pod_toleration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ee2646de12ea5c363d4004dcf1f6a10647d5358aa68a8133f4653f2c739033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPodToleration", [value]))

    @jsii.member(jsii_name="resetContainerResources")
    def reset_container_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerResources", []))

    @jsii.member(jsii_name="resetPodAffinity")
    def reset_pod_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodAffinity", []))

    @jsii.member(jsii_name="resetPodToleration")
    def reset_pod_toleration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodToleration", []))

    @jsii.member(jsii_name="resetReplicaCount")
    def reset_replica_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaCount", []))

    @builtins.property
    @jsii.member(jsii_name="containerResources")
    def container_resources(
        self,
    ) -> GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference, jsii.get(self, "containerResources"))

    @builtins.property
    @jsii.member(jsii_name="podToleration")
    def pod_toleration(
        self,
    ) -> "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationList":
        return typing.cast("GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationList", jsii.get(self, "podToleration"))

    @builtins.property
    @jsii.member(jsii_name="componentInput")
    def component_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "componentInput"))

    @builtins.property
    @jsii.member(jsii_name="containerResourcesInput")
    def container_resources_input(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources], jsii.get(self, "containerResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="podAffinityInput")
    def pod_affinity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="podTolerationInput")
    def pod_toleration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration"]]], jsii.get(self, "podTolerationInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaCountInput")
    def replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="component")
    def component(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "component"))

    @component.setter
    def component(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df88e5556478023172b22f692d6cba415f077f2b6158eefed0bd09052d5d375f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "component", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podAffinity")
    def pod_affinity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podAffinity"))

    @pod_affinity.setter
    def pod_affinity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4423a319fee75e4107087dee281a3bed137af52a39f16fe33543dd13ed75a01d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaCount")
    def replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCount"))

    @replica_count.setter
    def replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e422368739aa3c597e199b480d6b588533b7f6794274acbd8df3e0c1460a859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126edde667752d2bd442ab6f17941be84e1d297c7908f63f9c349bb345edfa4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration",
    jsii_struct_bases=[],
    name_mapping={
        "effect": "effect",
        "key": "key",
        "operator": "operator",
        "value": "value",
    },
)
class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration:
    def __init__(
        self,
        *,
        effect: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Matches a taint effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#effect GkeHubFeature#effect}
        :param key: Matches a taint key (not necessarily unique). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#key GkeHubFeature#key}
        :param operator: Matches a taint operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#operator GkeHubFeature#operator}
        :param value: Matches a taint value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#value GkeHubFeature#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def2a21811bbb25d985c07e75f6db28bf42e8a0fe9b5762df25e663707ebdacc)
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if effect is not None:
            self._values["effect"] = effect
        if key is not None:
            self._values["key"] = key
        if operator is not None:
            self._values["operator"] = operator
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def effect(self) -> typing.Optional[builtins.str]:
        '''Matches a taint effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#effect GkeHubFeature#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Matches a taint key (not necessarily unique).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#key GkeHubFeature#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Matches a taint operator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#operator GkeHubFeature#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Matches a taint value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#value GkeHubFeature#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6f65ad0aea6cd8036f544e331017f9b526ea0bb505cdeed50ace9916230756c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a529b047867d8182333efb4b974dbbdce9d5807637a389cd2eb2fe8ad29262c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb95ad2bc253657cc7e034b2c0cf129f7fc8769b6a1fe72b345b80dd4ec568b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d12f49d2211a54de150ae7dc577fb09d7d6487e91bb75d5a6dbbcafc34a8df17)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49cf19ca6ac7f3e256347eef8c279adf0f796565eab13898dcc93a1c093a9486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__849b618d35995cc8a3d6b8cccfc60d49a87c975b77f4c709918b12f0902456d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__816c364f44c177ee7adf96373751e77a5af83bbe789944ae3891b185c531c791)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEffect")
    def reset_effect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffect", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="effectInput")
    def effect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__144759d622507850c27b092cf6622d82f0acad57ddbff334b58037c27aa92eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6708df6b55b3168b44738b6ad1298552bc3baadaa0f3c7748e1d9143e31408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79718ab84ad1c94d57b8c560a653cd67a445826b14297d5f1dd95304d169aae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6447a89df4de77daff49ac342beb2733af8587c83ec59b81f39a6378ec48501f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11bf7e52cb89d99554f0ff31fc332b0f950bc13a11a07146c84f922c24fb35c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring",
    jsii_struct_bases=[],
    name_mapping={"backends": "backends"},
)
class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring:
    def __init__(
        self,
        *,
        backends: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param backends: Specifies the list of backends Policy Controller will export to. An empty list would effectively disable metrics export. Possible values: ["MONITORING_BACKEND_UNSPECIFIED", "PROMETHEUS", "CLOUD_MONITORING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#backends GkeHubFeature#backends}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3c2678ae323eb6ccdc7bbab4a1b3515dd926e679313c04a59cdc7b6ef04140)
            check_type(argname="argument backends", value=backends, expected_type=type_hints["backends"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backends is not None:
            self._values["backends"] = backends

    @builtins.property
    def backends(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of backends Policy Controller will export to.

        An empty list would effectively disable metrics export. Possible values: ["MONITORING_BACKEND_UNSPECIFIED", "PROMETHEUS", "CLOUD_MONITORING"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#backends GkeHubFeature#backends}
        '''
        result = self._values.get("backends")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48a15e5984f64663f9c92e1ad48453cd3a9079c6310d2853047057af343230e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackends")
    def reset_backends(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackends", []))

    @builtins.property
    @jsii.member(jsii_name="backendsInput")
    def backends_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "backendsInput"))

    @builtins.property
    @jsii.member(jsii_name="backends")
    def backends(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "backends"))

    @backends.setter
    def backends(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a137d6bc58e665e937a165b4b322a78e9e8deb2322c9f105ea660dbbe03bd23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backends", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba8a9fb82da352b6c47812f1498c4fe3640b56a807edad59c3a748daaaf212b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5541d177a83cc9080bf1b2bb2296cb4abc623172fa9ab6b159a9c22db6862fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeploymentConfigs")
    def put_deployment_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1d1a954b26416a8de672ac374a40e73db8e7c91e42821061e6bcdec1268fdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeploymentConfigs", [value]))

    @jsii.member(jsii_name="putMonitoring")
    def put_monitoring(
        self,
        *,
        backends: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param backends: Specifies the list of backends Policy Controller will export to. An empty list would effectively disable metrics export. Possible values: ["MONITORING_BACKEND_UNSPECIFIED", "PROMETHEUS", "CLOUD_MONITORING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#backends GkeHubFeature#backends}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring(
            backends=backends
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoring", [value]))

    @jsii.member(jsii_name="putPolicyContent")
    def put_policy_content(
        self,
        *,
        bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        template_library: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bundles: bundles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#bundles GkeHubFeature#bundles}
        :param template_library: template_library block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#template_library GkeHubFeature#template_library}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent(
            bundles=bundles, template_library=template_library
        )

        return typing.cast(None, jsii.invoke(self, "putPolicyContent", [value]))

    @jsii.member(jsii_name="resetAuditIntervalSeconds")
    def reset_audit_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuditIntervalSeconds", []))

    @jsii.member(jsii_name="resetConstraintViolationLimit")
    def reset_constraint_violation_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConstraintViolationLimit", []))

    @jsii.member(jsii_name="resetDeploymentConfigs")
    def reset_deployment_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentConfigs", []))

    @jsii.member(jsii_name="resetExemptableNamespaces")
    def reset_exemptable_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExemptableNamespaces", []))

    @jsii.member(jsii_name="resetLogDeniesEnabled")
    def reset_log_denies_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogDeniesEnabled", []))

    @jsii.member(jsii_name="resetMonitoring")
    def reset_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoring", []))

    @jsii.member(jsii_name="resetMutationEnabled")
    def reset_mutation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMutationEnabled", []))

    @jsii.member(jsii_name="resetPolicyContent")
    def reset_policy_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyContent", []))

    @jsii.member(jsii_name="resetReferentialRulesEnabled")
    def reset_referential_rules_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferentialRulesEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigs")
    def deployment_configs(
        self,
    ) -> GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList, jsii.get(self, "deploymentConfigs"))

    @builtins.property
    @jsii.member(jsii_name="monitoring")
    def monitoring(
        self,
    ) -> GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference, jsii.get(self, "monitoring"))

    @builtins.property
    @jsii.member(jsii_name="policyContent")
    def policy_content(
        self,
    ) -> "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference":
        return typing.cast("GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference", jsii.get(self, "policyContent"))

    @builtins.property
    @jsii.member(jsii_name="auditIntervalSecondsInput")
    def audit_interval_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "auditIntervalSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="constraintViolationLimitInput")
    def constraint_violation_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "constraintViolationLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigsInput")
    def deployment_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]], jsii.get(self, "deploymentConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="exemptableNamespacesInput")
    def exemptable_namespaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exemptableNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="installSpecInput")
    def install_spec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "installSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="logDeniesEnabledInput")
    def log_denies_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logDeniesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringInput")
    def monitoring_input(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring], jsii.get(self, "monitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="mutationEnabledInput")
    def mutation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mutationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="policyContentInput")
    def policy_content_input(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent"]:
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent"], jsii.get(self, "policyContentInput"))

    @builtins.property
    @jsii.member(jsii_name="referentialRulesEnabledInput")
    def referential_rules_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "referentialRulesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="auditIntervalSeconds")
    def audit_interval_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "auditIntervalSeconds"))

    @audit_interval_seconds.setter
    def audit_interval_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7e977424951320a68434bf2cb63f823d33ea003ec54993dc3d0f27d774a0bee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auditIntervalSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="constraintViolationLimit")
    def constraint_violation_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "constraintViolationLimit"))

    @constraint_violation_limit.setter
    def constraint_violation_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab56625e57ba0467563ed23108e610043d67ffd048618ea26cc62fa303a9304d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constraintViolationLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exemptableNamespaces")
    def exemptable_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exemptableNamespaces"))

    @exemptable_namespaces.setter
    def exemptable_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af88697833a2623b6c3f99023e96e14b3dc1cb6c44b8be2bfee69e0c2293094d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exemptableNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="installSpec")
    def install_spec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "installSpec"))

    @install_spec.setter
    def install_spec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968e8e2b18e2cd9bbd4bfeaf83aa178ab5ece6ed8e9f631bccbfc3e90a880fb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "installSpec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logDeniesEnabled")
    def log_denies_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logDeniesEnabled"))

    @log_denies_enabled.setter
    def log_denies_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e3496f2a0162159bcda1e7c452cde766783f16715bb01d6b16ef931697c441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDeniesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mutationEnabled")
    def mutation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mutationEnabled"))

    @mutation_enabled.setter
    def mutation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1e42d1b0bf068ee836ee72a58fc9bf4e997686afc3efaaf726efdb70e9cbc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mutationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="referentialRulesEnabled")
    def referential_rules_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "referentialRulesEnabled"))

    @referential_rules_enabled.setter
    def referential_rules_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c992efc35dca1c451b609a3d5ff53dd4a202dd88df1116a6dd5d32bfa9ce1582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referentialRulesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffdf031201721ab07fd7cb070b34f3fe209cb40fbe185e6a72b9e476adf5a292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent",
    jsii_struct_bases=[],
    name_mapping={"bundles": "bundles", "template_library": "templateLibrary"},
)
class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent:
    def __init__(
        self,
        *,
        bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        template_library: typing.Optional[typing.Union["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bundles: bundles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#bundles GkeHubFeature#bundles}
        :param template_library: template_library block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#template_library GkeHubFeature#template_library}
        '''
        if isinstance(template_library, dict):
            template_library = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary(**template_library)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64b2a1b79347ed610e483ddb92256474268f284f08d39f279203118cb924e9c)
            check_type(argname="argument bundles", value=bundles, expected_type=type_hints["bundles"])
            check_type(argname="argument template_library", value=template_library, expected_type=type_hints["template_library"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bundles is not None:
            self._values["bundles"] = bundles
        if template_library is not None:
            self._values["template_library"] = template_library

    @builtins.property
    def bundles(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles"]]]:
        '''bundles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#bundles GkeHubFeature#bundles}
        '''
        result = self._values.get("bundles")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles"]]], result)

    @builtins.property
    def template_library(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"]:
        '''template_library block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#template_library GkeHubFeature#template_library}
        '''
        result = self._values.get("template_library")
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles",
    jsii_struct_bases=[],
    name_mapping={"bundle": "bundle", "exempted_namespaces": "exemptedNamespaces"},
)
class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles:
    def __init__(
        self,
        *,
        bundle: builtins.str,
        exempted_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bundle: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#bundle GkeHubFeature#bundle}.
        :param exempted_namespaces: The set of namespaces to be exempted from the bundle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#exempted_namespaces GkeHubFeature#exempted_namespaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8535feade9e0add025c3920d347bf701d6c7f8fd9cbd844f2f00d36c11c23e01)
            check_type(argname="argument bundle", value=bundle, expected_type=type_hints["bundle"])
            check_type(argname="argument exempted_namespaces", value=exempted_namespaces, expected_type=type_hints["exempted_namespaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bundle": bundle,
        }
        if exempted_namespaces is not None:
            self._values["exempted_namespaces"] = exempted_namespaces

    @builtins.property
    def bundle(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#bundle GkeHubFeature#bundle}.'''
        result = self._values.get("bundle")
        assert result is not None, "Required property 'bundle' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exempted_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of namespaces to be exempted from the bundle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#exempted_namespaces GkeHubFeature#exempted_namespaces}
        '''
        result = self._values.get("exempted_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bd4cefe9b03ba30e3e51da017e2df98cc55e395d131c663927eca8ac9f15e67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc3bdc2a556f95d0761d5e708e349f930404753a89c365e4fcd6faffbe704285)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3793b1c6e736b27f4e919aa3d79011cd761102acb7f656e34bb65a8291c1985)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dd0837593625d4d894281a6fb5ee4b1168ef38bf0194273d056d39049db634e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27e364a5ad00da88c58d514af650a4e106f0fc4aa4ab431cf3e5e27de78f82b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec33b015c8f652353e6bc87b4ddd58126bfbdb234b527e2bb1f98790ca356e43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__730c1d2a813f511a3c6accab394f0ea2ee25a261298cd386e7a267a466905f5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExemptedNamespaces")
    def reset_exempted_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExemptedNamespaces", []))

    @builtins.property
    @jsii.member(jsii_name="bundleInput")
    def bundle_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bundleInput"))

    @builtins.property
    @jsii.member(jsii_name="exemptedNamespacesInput")
    def exempted_namespaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exemptedNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="bundle")
    def bundle(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bundle"))

    @bundle.setter
    def bundle(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae87e2d96ba343a71ac6cb1a8aa31de76da0923dc3fc4acb376facae844e7d9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exemptedNamespaces")
    def exempted_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exemptedNamespaces"))

    @exempted_namespaces.setter
    def exempted_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dffc47a5d95312de89f1c2679e3e53dc70de089ac4a9d1d12ca4a7d962afe1e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exemptedNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc281dc670546574fa4b7296d55b779b5bab72215625100621ca243d13454fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7a0f6e077256a27c5aea28e8f77d275cedb7739b91c1425e7cb8bd8ed78d138)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBundles")
    def put_bundles(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0963eb95b502a692636dbd7200ce8d0e07b98bd4f93466104d6f709597ba5016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBundles", [value]))

    @jsii.member(jsii_name="putTemplateLibrary")
    def put_template_library(
        self,
        *,
        installation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param installation: Configures the manner in which the template library is installed on the cluster. Possible values: ["INSTALLATION_UNSPECIFIED", "NOT_INSTALLED", "ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#installation GkeHubFeature#installation}
        '''
        value = GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary(
            installation=installation
        )

        return typing.cast(None, jsii.invoke(self, "putTemplateLibrary", [value]))

    @jsii.member(jsii_name="resetBundles")
    def reset_bundles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBundles", []))

    @jsii.member(jsii_name="resetTemplateLibrary")
    def reset_template_library(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateLibrary", []))

    @builtins.property
    @jsii.member(jsii_name="bundles")
    def bundles(
        self,
    ) -> GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList:
        return typing.cast(GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList, jsii.get(self, "bundles"))

    @builtins.property
    @jsii.member(jsii_name="templateLibrary")
    def template_library(
        self,
    ) -> "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference":
        return typing.cast("GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference", jsii.get(self, "templateLibrary"))

    @builtins.property
    @jsii.member(jsii_name="bundlesInput")
    def bundles_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]], jsii.get(self, "bundlesInput"))

    @builtins.property
    @jsii.member(jsii_name="templateLibraryInput")
    def template_library_input(
        self,
    ) -> typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"]:
        return typing.cast(typing.Optional["GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"], jsii.get(self, "templateLibraryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32a3908ac408695f717040bfe288d49e60c34353b033d6fce0f653ad6b11ad9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary",
    jsii_struct_bases=[],
    name_mapping={"installation": "installation"},
)
class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary:
    def __init__(self, *, installation: typing.Optional[builtins.str] = None) -> None:
        '''
        :param installation: Configures the manner in which the template library is installed on the cluster. Possible values: ["INSTALLATION_UNSPECIFIED", "NOT_INSTALLED", "ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#installation GkeHubFeature#installation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91424fb6f79903b86a9c718fedc7b5a48ad4ac8619b16375574d0e36024eddf9)
            check_type(argname="argument installation", value=installation, expected_type=type_hints["installation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if installation is not None:
            self._values["installation"] = installation

    @builtins.property
    def installation(self) -> typing.Optional[builtins.str]:
        '''Configures the manner in which the template library is installed on the cluster. Possible values: ["INSTALLATION_UNSPECIFIED", "NOT_INSTALLED", "ALL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#installation GkeHubFeature#installation}
        '''
        result = self._values.get("installation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1723ddebdd3c15275b406c5280cbb4932f1be28e1a58d34dcb2c3aed91a4e590)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstallation")
    def reset_installation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstallation", []))

    @builtins.property
    @jsii.member(jsii_name="installationInput")
    def installation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "installationInput"))

    @builtins.property
    @jsii.member(jsii_name="installation")
    def installation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "installation"))

    @installation.setter
    def installation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbab8a094e2187bad12f39e498878612499d3dbe66fd74f9f4fa878020d35c5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "installation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary]:
        return typing.cast(typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a0ee3581da5d3aeaf54f1fc928e5e042b3d60d2ec2f0558903e7df7f21d143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureResourceState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeHubFeatureResourceState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureResourceState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureResourceStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureResourceStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51fa5def0c74b8743eb9dde5b12030b076d80f4991a1b7cb4ac34f6e941bb2f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GkeHubFeatureResourceStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__169e4dbd3e43a7981594669bdccb7718cef6c8c85402578e2ec5b7ece57b8af3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureResourceStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e90d2820e7dd4f098245f37a003b5de2956ec80f4c1248e1674d643af918857)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6376c67b67fb947da465a31a757336f1ffe10f32c58c4a2ac52ddf911da9cb1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffaef58b50a8ece292d1202c1fa9c1b4833922d8bc5445706a29e38808cec8bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureResourceStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureResourceStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d9b755f910d09e2cc696919bb5bf80e0cbea3b02a17dfa4b51c8ab6b7f57016)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hasResources")
    def has_resources(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "hasResources"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureResourceState]:
        return typing.cast(typing.Optional[GkeHubFeatureResourceState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureResourceState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0301590450c6283eebb008508d183857209ec55a5ae10acc873fc46846ae2e7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpec",
    jsii_struct_bases=[],
    name_mapping={
        "clusterupgrade": "clusterupgrade",
        "fleetobservability": "fleetobservability",
        "multiclusteringress": "multiclusteringress",
        "rbacrolebindingactuation": "rbacrolebindingactuation",
    },
)
class GkeHubFeatureSpec:
    def __init__(
        self,
        *,
        clusterupgrade: typing.Optional[typing.Union["GkeHubFeatureSpecClusterupgrade", typing.Dict[builtins.str, typing.Any]]] = None,
        fleetobservability: typing.Optional[typing.Union["GkeHubFeatureSpecFleetobservability", typing.Dict[builtins.str, typing.Any]]] = None,
        multiclusteringress: typing.Optional[typing.Union["GkeHubFeatureSpecMulticlusteringress", typing.Dict[builtins.str, typing.Any]]] = None,
        rbacrolebindingactuation: typing.Optional[typing.Union["GkeHubFeatureSpecRbacrolebindingactuation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param clusterupgrade: clusterupgrade block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#clusterupgrade GkeHubFeature#clusterupgrade}
        :param fleetobservability: fleetobservability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#fleetobservability GkeHubFeature#fleetobservability}
        :param multiclusteringress: multiclusteringress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#multiclusteringress GkeHubFeature#multiclusteringress}
        :param rbacrolebindingactuation: rbacrolebindingactuation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#rbacrolebindingactuation GkeHubFeature#rbacrolebindingactuation}
        '''
        if isinstance(clusterupgrade, dict):
            clusterupgrade = GkeHubFeatureSpecClusterupgrade(**clusterupgrade)
        if isinstance(fleetobservability, dict):
            fleetobservability = GkeHubFeatureSpecFleetobservability(**fleetobservability)
        if isinstance(multiclusteringress, dict):
            multiclusteringress = GkeHubFeatureSpecMulticlusteringress(**multiclusteringress)
        if isinstance(rbacrolebindingactuation, dict):
            rbacrolebindingactuation = GkeHubFeatureSpecRbacrolebindingactuation(**rbacrolebindingactuation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a716320b8f8b882d1cad6fcfc3c62e854fb6fab48035624c314bc71304c2453b)
            check_type(argname="argument clusterupgrade", value=clusterupgrade, expected_type=type_hints["clusterupgrade"])
            check_type(argname="argument fleetobservability", value=fleetobservability, expected_type=type_hints["fleetobservability"])
            check_type(argname="argument multiclusteringress", value=multiclusteringress, expected_type=type_hints["multiclusteringress"])
            check_type(argname="argument rbacrolebindingactuation", value=rbacrolebindingactuation, expected_type=type_hints["rbacrolebindingactuation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if clusterupgrade is not None:
            self._values["clusterupgrade"] = clusterupgrade
        if fleetobservability is not None:
            self._values["fleetobservability"] = fleetobservability
        if multiclusteringress is not None:
            self._values["multiclusteringress"] = multiclusteringress
        if rbacrolebindingactuation is not None:
            self._values["rbacrolebindingactuation"] = rbacrolebindingactuation

    @builtins.property
    def clusterupgrade(self) -> typing.Optional["GkeHubFeatureSpecClusterupgrade"]:
        '''clusterupgrade block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#clusterupgrade GkeHubFeature#clusterupgrade}
        '''
        result = self._values.get("clusterupgrade")
        return typing.cast(typing.Optional["GkeHubFeatureSpecClusterupgrade"], result)

    @builtins.property
    def fleetobservability(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecFleetobservability"]:
        '''fleetobservability block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#fleetobservability GkeHubFeature#fleetobservability}
        '''
        result = self._values.get("fleetobservability")
        return typing.cast(typing.Optional["GkeHubFeatureSpecFleetobservability"], result)

    @builtins.property
    def multiclusteringress(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecMulticlusteringress"]:
        '''multiclusteringress block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#multiclusteringress GkeHubFeature#multiclusteringress}
        '''
        result = self._values.get("multiclusteringress")
        return typing.cast(typing.Optional["GkeHubFeatureSpecMulticlusteringress"], result)

    @builtins.property
    def rbacrolebindingactuation(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecRbacrolebindingactuation"]:
        '''rbacrolebindingactuation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#rbacrolebindingactuation GkeHubFeature#rbacrolebindingactuation}
        '''
        result = self._values.get("rbacrolebindingactuation")
        return typing.cast(typing.Optional["GkeHubFeatureSpecRbacrolebindingactuation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecClusterupgrade",
    jsii_struct_bases=[],
    name_mapping={
        "upstream_fleets": "upstreamFleets",
        "gke_upgrade_overrides": "gkeUpgradeOverrides",
        "post_conditions": "postConditions",
    },
)
class GkeHubFeatureSpecClusterupgrade:
    def __init__(
        self,
        *,
        upstream_fleets: typing.Sequence[builtins.str],
        gke_upgrade_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_conditions: typing.Optional[typing.Union["GkeHubFeatureSpecClusterupgradePostConditions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param upstream_fleets: Specified if other fleet should be considered as a source of upgrades. Currently, at most one upstream fleet is allowed. The fleet name should be either fleet project number or id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#upstream_fleets GkeHubFeature#upstream_fleets}
        :param gke_upgrade_overrides: gke_upgrade_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#gke_upgrade_overrides GkeHubFeature#gke_upgrade_overrides}
        :param post_conditions: post_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#post_conditions GkeHubFeature#post_conditions}
        '''
        if isinstance(post_conditions, dict):
            post_conditions = GkeHubFeatureSpecClusterupgradePostConditions(**post_conditions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422aad5b19e4356dc05157719e07d849c96c978e43ceb475c33b8afe28d0008e)
            check_type(argname="argument upstream_fleets", value=upstream_fleets, expected_type=type_hints["upstream_fleets"])
            check_type(argname="argument gke_upgrade_overrides", value=gke_upgrade_overrides, expected_type=type_hints["gke_upgrade_overrides"])
            check_type(argname="argument post_conditions", value=post_conditions, expected_type=type_hints["post_conditions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "upstream_fleets": upstream_fleets,
        }
        if gke_upgrade_overrides is not None:
            self._values["gke_upgrade_overrides"] = gke_upgrade_overrides
        if post_conditions is not None:
            self._values["post_conditions"] = post_conditions

    @builtins.property
    def upstream_fleets(self) -> typing.List[builtins.str]:
        '''Specified if other fleet should be considered as a source of upgrades.

        Currently, at most one upstream fleet is allowed. The fleet name should be either fleet project number or id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#upstream_fleets GkeHubFeature#upstream_fleets}
        '''
        result = self._values.get("upstream_fleets")
        assert result is not None, "Required property 'upstream_fleets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def gke_upgrade_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides"]]]:
        '''gke_upgrade_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#gke_upgrade_overrides GkeHubFeature#gke_upgrade_overrides}
        '''
        result = self._values.get("gke_upgrade_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides"]]], result)

    @builtins.property
    def post_conditions(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecClusterupgradePostConditions"]:
        '''post_conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#post_conditions GkeHubFeature#post_conditions}
        '''
        result = self._values.get("post_conditions")
        return typing.cast(typing.Optional["GkeHubFeatureSpecClusterupgradePostConditions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecClusterupgrade(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides",
    jsii_struct_bases=[],
    name_mapping={"post_conditions": "postConditions", "upgrade": "upgrade"},
)
class GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides:
    def __init__(
        self,
        *,
        post_conditions: typing.Union["GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions", typing.Dict[builtins.str, typing.Any]],
        upgrade: typing.Union["GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param post_conditions: post_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#post_conditions GkeHubFeature#post_conditions}
        :param upgrade: upgrade block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#upgrade GkeHubFeature#upgrade}
        '''
        if isinstance(post_conditions, dict):
            post_conditions = GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions(**post_conditions)
        if isinstance(upgrade, dict):
            upgrade = GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade(**upgrade)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__295b00727e5a5b2f2dbc90125f6c1c32e599be9d7dd214a8f01628270a1a1765)
            check_type(argname="argument post_conditions", value=post_conditions, expected_type=type_hints["post_conditions"])
            check_type(argname="argument upgrade", value=upgrade, expected_type=type_hints["upgrade"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "post_conditions": post_conditions,
            "upgrade": upgrade,
        }

    @builtins.property
    def post_conditions(
        self,
    ) -> "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions":
        '''post_conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#post_conditions GkeHubFeature#post_conditions}
        '''
        result = self._values.get("post_conditions")
        assert result is not None, "Required property 'post_conditions' is missing"
        return typing.cast("GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions", result)

    @builtins.property
    def upgrade(self) -> "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade":
        '''upgrade block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#upgrade GkeHubFeature#upgrade}
        '''
        result = self._values.get("upgrade")
        assert result is not None, "Required property 'upgrade' is missing"
        return typing.cast("GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c63ca39571dc5cd55e9bcab6ab564e06cb063c4b54785c1d94d435182785ac84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e847c8d5e15d79a848734b0ce91e312688eeae7eb80a7326e486fbaede807c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63780bd7156ddb4cd657130ce02a27ecc9474a64c25761dd0dbd1901d71ac85e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b630118727b1103be516f28efa34ffe595fb5ea27bf14d3644e55d0fcfbfa345)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14d74705166d212b36a770726590f6193cfe369e0bd977f3633a51be19f9a495)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7387fc9172a105c3de14215daf78e584c19537252f34d1922f769afb442b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5018478af9ac11c4d14bc312edbdf0527b6e7a63ff5d5f929d2ecca5348f3086)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPostConditions")
    def put_post_conditions(self, *, soaking: builtins.str) -> None:
        '''
        :param soaking: Amount of time to "soak" after a rollout has been finished before marking it COMPLETE. Cannot exceed 30 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#soaking GkeHubFeature#soaking}
        '''
        value = GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions(
            soaking=soaking
        )

        return typing.cast(None, jsii.invoke(self, "putPostConditions", [value]))

    @jsii.member(jsii_name="putUpgrade")
    def put_upgrade(self, *, name: builtins.str, version: builtins.str) -> None:
        '''
        :param name: Name of the upgrade, e.g., "k8s_control_plane". It should be a valid upgrade name. It must not exceet 99 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#name GkeHubFeature#name}
        :param version: Version of the upgrade, e.g., "1.22.1-gke.100". It should be a valid version. It must not exceet 99 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        value = GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade(
            name=name, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putUpgrade", [value]))

    @builtins.property
    @jsii.member(jsii_name="postConditions")
    def post_conditions(
        self,
    ) -> "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditionsOutputReference":
        return typing.cast("GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditionsOutputReference", jsii.get(self, "postConditions"))

    @builtins.property
    @jsii.member(jsii_name="upgrade")
    def upgrade(
        self,
    ) -> "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgradeOutputReference":
        return typing.cast("GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgradeOutputReference", jsii.get(self, "upgrade"))

    @builtins.property
    @jsii.member(jsii_name="postConditionsInput")
    def post_conditions_input(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions"]:
        return typing.cast(typing.Optional["GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions"], jsii.get(self, "postConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeInput")
    def upgrade_input(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade"]:
        return typing.cast(typing.Optional["GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade"], jsii.get(self, "upgradeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444f092d6adf02a66163230875e966e45b76d9cc5c9104caa47f0049dd1efc1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions",
    jsii_struct_bases=[],
    name_mapping={"soaking": "soaking"},
)
class GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions:
    def __init__(self, *, soaking: builtins.str) -> None:
        '''
        :param soaking: Amount of time to "soak" after a rollout has been finished before marking it COMPLETE. Cannot exceed 30 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#soaking GkeHubFeature#soaking}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97fc8b63a540e6d759de031766a79559f50aa5a509c1253678c5dea18b3fd699)
            check_type(argname="argument soaking", value=soaking, expected_type=type_hints["soaking"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "soaking": soaking,
        }

    @builtins.property
    def soaking(self) -> builtins.str:
        '''Amount of time to "soak" after a rollout has been finished before marking it COMPLETE. Cannot exceed 30 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#soaking GkeHubFeature#soaking}
        '''
        result = self._values.get("soaking")
        assert result is not None, "Required property 'soaking' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__641c27807576fcf7cd56e15d08d1f4b39d68bc07529b82eb78df27b6ec3f98aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="soakingInput")
    def soaking_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "soakingInput"))

    @builtins.property
    @jsii.member(jsii_name="soaking")
    def soaking(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "soaking"))

    @soaking.setter
    def soaking(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1ffe6ab47a06aaf147685bb53c96cb6eaa196f9c23bbd60deeaa4135aa2031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "soaking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dae6bc8429d2fbd0121875adb734926f208731a737d34da4dd8873ebb3c6bac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "version": "version"},
)
class GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade:
    def __init__(self, *, name: builtins.str, version: builtins.str) -> None:
        '''
        :param name: Name of the upgrade, e.g., "k8s_control_plane". It should be a valid upgrade name. It must not exceet 99 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#name GkeHubFeature#name}
        :param version: Version of the upgrade, e.g., "1.22.1-gke.100". It should be a valid version. It must not exceet 99 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a482714d0334cfe20337b73af514474962652adf0debfe14f1903a720556a3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "version": version,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the upgrade, e.g., "k8s_control_plane". It should be a valid upgrade name. It must not exceet 99 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#name GkeHubFeature#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Version of the upgrade, e.g., "1.22.1-gke.100". It should be a valid version. It must not exceet 99 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#version GkeHubFeature#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgradeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgradeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89af15afb78fdc835e5a1a44c3b2efec697de36a7aba124bbe1979430fb7c554)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7f8ac91749ffb513331400a8faf9d2171dfb0a489a21b9e3a410eeb3f8f5de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22491371982f99c04cf2f030a7abc3b3001ce68e183810c9b1a6169352207ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ba1351bfe71d80e7a808eeef62d841cf0200259d8eb03f58b708059d0a6694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureSpecClusterupgradeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecClusterupgradeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f56ca5f7ff1c19850775d36296c14ae679fa49423940f8440eda9415085001e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGkeUpgradeOverrides")
    def put_gke_upgrade_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac4ffb472fd20cb48b15d1fbdf2088c1204f7c5711b690ae8604532ed4cb9fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGkeUpgradeOverrides", [value]))

    @jsii.member(jsii_name="putPostConditions")
    def put_post_conditions(self, *, soaking: builtins.str) -> None:
        '''
        :param soaking: Amount of time to "soak" after a rollout has been finished before marking it COMPLETE. Cannot exceed 30 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#soaking GkeHubFeature#soaking}
        '''
        value = GkeHubFeatureSpecClusterupgradePostConditions(soaking=soaking)

        return typing.cast(None, jsii.invoke(self, "putPostConditions", [value]))

    @jsii.member(jsii_name="resetGkeUpgradeOverrides")
    def reset_gke_upgrade_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGkeUpgradeOverrides", []))

    @jsii.member(jsii_name="resetPostConditions")
    def reset_post_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostConditions", []))

    @builtins.property
    @jsii.member(jsii_name="gkeUpgradeOverrides")
    def gke_upgrade_overrides(
        self,
    ) -> GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesList:
        return typing.cast(GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesList, jsii.get(self, "gkeUpgradeOverrides"))

    @builtins.property
    @jsii.member(jsii_name="postConditions")
    def post_conditions(
        self,
    ) -> "GkeHubFeatureSpecClusterupgradePostConditionsOutputReference":
        return typing.cast("GkeHubFeatureSpecClusterupgradePostConditionsOutputReference", jsii.get(self, "postConditions"))

    @builtins.property
    @jsii.member(jsii_name="gkeUpgradeOverridesInput")
    def gke_upgrade_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]], jsii.get(self, "gkeUpgradeOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="postConditionsInput")
    def post_conditions_input(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecClusterupgradePostConditions"]:
        return typing.cast(typing.Optional["GkeHubFeatureSpecClusterupgradePostConditions"], jsii.get(self, "postConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="upstreamFleetsInput")
    def upstream_fleets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "upstreamFleetsInput"))

    @builtins.property
    @jsii.member(jsii_name="upstreamFleets")
    def upstream_fleets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "upstreamFleets"))

    @upstream_fleets.setter
    def upstream_fleets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c857b73e84a92c855aefa49a18508ec313f6e0ba9e8e072a0e6b91b957a77fec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upstreamFleets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureSpecClusterupgrade]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecClusterupgrade], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecClusterupgrade],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48b2ceb32f289efcf9d126a577c1429c99a67dfca2765c92903e9004cfff034c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecClusterupgradePostConditions",
    jsii_struct_bases=[],
    name_mapping={"soaking": "soaking"},
)
class GkeHubFeatureSpecClusterupgradePostConditions:
    def __init__(self, *, soaking: builtins.str) -> None:
        '''
        :param soaking: Amount of time to "soak" after a rollout has been finished before marking it COMPLETE. Cannot exceed 30 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#soaking GkeHubFeature#soaking}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ddb0b8cf65ba648cd588f7045003778bb81c6ceabd69aa4983915590eeab864)
            check_type(argname="argument soaking", value=soaking, expected_type=type_hints["soaking"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "soaking": soaking,
        }

    @builtins.property
    def soaking(self) -> builtins.str:
        '''Amount of time to "soak" after a rollout has been finished before marking it COMPLETE. Cannot exceed 30 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#soaking GkeHubFeature#soaking}
        '''
        result = self._values.get("soaking")
        assert result is not None, "Required property 'soaking' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecClusterupgradePostConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureSpecClusterupgradePostConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecClusterupgradePostConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__522c16537c2030f35c821a82ffe81c9a8380b946bdfea4c974a600b3aa3f7e36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="soakingInput")
    def soaking_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "soakingInput"))

    @builtins.property
    @jsii.member(jsii_name="soaking")
    def soaking(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "soaking"))

    @soaking.setter
    def soaking(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c547bc8da54b9d9eba7deca3a74970066f8b3448b21a517ae611a0cafc5835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "soaking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecClusterupgradePostConditions]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecClusterupgradePostConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecClusterupgradePostConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa016000beba25e15d657b6a5311f4635e443edc360aa2c53c7e6dc750ff131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservability",
    jsii_struct_bases=[],
    name_mapping={"logging_config": "loggingConfig"},
)
class GkeHubFeatureSpecFleetobservability:
    def __init__(
        self,
        *,
        logging_config: typing.Optional[typing.Union["GkeHubFeatureSpecFleetobservabilityLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#logging_config GkeHubFeature#logging_config}
        '''
        if isinstance(logging_config, dict):
            logging_config = GkeHubFeatureSpecFleetobservabilityLoggingConfig(**logging_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030a905466c4f9658d40701158addfebf98ef14c6c84a43cdd13d5ba7a55670b)
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if logging_config is not None:
            self._values["logging_config"] = logging_config

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecFleetobservabilityLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#logging_config GkeHubFeature#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["GkeHubFeatureSpecFleetobservabilityLoggingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecFleetobservability(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "default_config": "defaultConfig",
        "fleet_scope_logs_config": "fleetScopeLogsConfig",
    },
)
class GkeHubFeatureSpecFleetobservabilityLoggingConfig:
    def __init__(
        self,
        *,
        default_config: typing.Optional[typing.Union["GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        fleet_scope_logs_config: typing.Optional[typing.Union["GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_config: default_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#default_config GkeHubFeature#default_config}
        :param fleet_scope_logs_config: fleet_scope_logs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#fleet_scope_logs_config GkeHubFeature#fleet_scope_logs_config}
        '''
        if isinstance(default_config, dict):
            default_config = GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig(**default_config)
        if isinstance(fleet_scope_logs_config, dict):
            fleet_scope_logs_config = GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig(**fleet_scope_logs_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052b23094a3454b7a310041016ec2a7c7ba987f03eacf5ac5a28c8328074811e)
            check_type(argname="argument default_config", value=default_config, expected_type=type_hints["default_config"])
            check_type(argname="argument fleet_scope_logs_config", value=fleet_scope_logs_config, expected_type=type_hints["fleet_scope_logs_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_config is not None:
            self._values["default_config"] = default_config
        if fleet_scope_logs_config is not None:
            self._values["fleet_scope_logs_config"] = fleet_scope_logs_config

    @builtins.property
    def default_config(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig"]:
        '''default_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#default_config GkeHubFeature#default_config}
        '''
        result = self._values.get("default_config")
        return typing.cast(typing.Optional["GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig"], result)

    @builtins.property
    def fleet_scope_logs_config(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig"]:
        '''fleet_scope_logs_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#fleet_scope_logs_config GkeHubFeature#fleet_scope_logs_config}
        '''
        result = self._values.get("fleet_scope_logs_config")
        return typing.cast(typing.Optional["GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecFleetobservabilityLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig:
    def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mode: Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#mode GkeHubFeature#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684f07004b1ba6f1f8d8210a6d8f55a5b9e71793ea2dd271410e09057bf670ce)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#mode GkeHubFeature#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2eefa415f8be9ad5f0084e817c76a09dfcd7f3d4ebc38d5c8d8005bf3ca26347)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b36e41c88ff90e7c3ac695aaa0d8a66814ac975ea59594c975ce23ec284dde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5abb6ffe810d324d665591d0e1dc7deeb2de562a5571ecfafa46e3ed8801e8e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig:
    def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mode: Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#mode GkeHubFeature#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59cdac985bb9fb598a09f83796f0d95e39afb6c9258d8a3f9b900ff953ba91a5)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#mode GkeHubFeature#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75d8228dc60e23fa3ca020047c75c220dbb36cdcf72e723161170edb0817fd0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d5864bccefcbd7788e4cf6385173e4cafc7cde89842f64b6035871d08d2dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19855e3fa053dde6fb0ff5978dc5bdc59eff9aa0a1c445915bbb3dc3bdba55a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d845075062d30d7e7f9f6a20d4a519ea3dd3c5b2bd23e55ac16814d01a83f188)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDefaultConfig")
    def put_default_config(self, *, mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mode: Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#mode GkeHubFeature#mode}
        '''
        value = GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig(
            mode=mode
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultConfig", [value]))

    @jsii.member(jsii_name="putFleetScopeLogsConfig")
    def put_fleet_scope_logs_config(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#mode GkeHubFeature#mode}
        '''
        value = GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig(
            mode=mode
        )

        return typing.cast(None, jsii.invoke(self, "putFleetScopeLogsConfig", [value]))

    @jsii.member(jsii_name="resetDefaultConfig")
    def reset_default_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultConfig", []))

    @jsii.member(jsii_name="resetFleetScopeLogsConfig")
    def reset_fleet_scope_logs_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFleetScopeLogsConfig", []))

    @builtins.property
    @jsii.member(jsii_name="defaultConfig")
    def default_config(
        self,
    ) -> GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference:
        return typing.cast(GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference, jsii.get(self, "defaultConfig"))

    @builtins.property
    @jsii.member(jsii_name="fleetScopeLogsConfig")
    def fleet_scope_logs_config(
        self,
    ) -> GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference:
        return typing.cast(GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference, jsii.get(self, "fleetScopeLogsConfig"))

    @builtins.property
    @jsii.member(jsii_name="defaultConfigInput")
    def default_config_input(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig], jsii.get(self, "defaultConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetScopeLogsConfigInput")
    def fleet_scope_logs_config_input(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig], jsii.get(self, "fleetScopeLogsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2eefb77c01d055b0e63a5526402c6a1a51e3434075a2c39d13f641b987098b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureSpecFleetobservabilityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecFleetobservabilityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfb4c97d07dd08c1bd71296d80b57fadaffa68ec990d5d377d04725e7b97412c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        default_config: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        fleet_scope_logs_config: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_config: default_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#default_config GkeHubFeature#default_config}
        :param fleet_scope_logs_config: fleet_scope_logs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#fleet_scope_logs_config GkeHubFeature#fleet_scope_logs_config}
        '''
        value = GkeHubFeatureSpecFleetobservabilityLoggingConfig(
            default_config=default_config,
            fleet_scope_logs_config=fleet_scope_logs_config,
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> GkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference:
        return typing.cast(GkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureSpecFleetobservability]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservability], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecFleetobservability],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b27a2569d413f9d62089e0030491958ab16fcc8141fbae5bec1cdd5f53342a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecMulticlusteringress",
    jsii_struct_bases=[],
    name_mapping={"config_membership": "configMembership"},
)
class GkeHubFeatureSpecMulticlusteringress:
    def __init__(self, *, config_membership: builtins.str) -> None:
        '''
        :param config_membership: Fully-qualified Membership name which hosts the MultiClusterIngress CRD. Example: 'projects/foo-proj/locations/global/memberships/bar'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#config_membership GkeHubFeature#config_membership}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42001b933a09bfedcafd2135e2449a44c8b807f8de748095bcca334fd6e37a1)
            check_type(argname="argument config_membership", value=config_membership, expected_type=type_hints["config_membership"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_membership": config_membership,
        }

    @builtins.property
    def config_membership(self) -> builtins.str:
        '''Fully-qualified Membership name which hosts the MultiClusterIngress CRD. Example: 'projects/foo-proj/locations/global/memberships/bar'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#config_membership GkeHubFeature#config_membership}
        '''
        result = self._values.get("config_membership")
        assert result is not None, "Required property 'config_membership' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecMulticlusteringress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureSpecMulticlusteringressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecMulticlusteringressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e787769b7a1016f6952abb8601447de6098f294856b79bae4749ab46b10b75d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="configMembershipInput")
    def config_membership_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configMembershipInput"))

    @builtins.property
    @jsii.member(jsii_name="configMembership")
    def config_membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configMembership"))

    @config_membership.setter
    def config_membership(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3bd2b56883c6f3693de74d0998420c8e5f70cec3de660eeb795d5876487e66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configMembership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureSpecMulticlusteringress]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecMulticlusteringress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecMulticlusteringress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a5845702568e545287521eb4cd522f450b7df32043774f3410e63faf03a0eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39987c2a69b04624c5f234f3f934c5a5ab7e6ef463c757767db320c09d73bdba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClusterupgrade")
    def put_clusterupgrade(
        self,
        *,
        upstream_fleets: typing.Sequence[builtins.str],
        gke_upgrade_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_conditions: typing.Optional[typing.Union[GkeHubFeatureSpecClusterupgradePostConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param upstream_fleets: Specified if other fleet should be considered as a source of upgrades. Currently, at most one upstream fleet is allowed. The fleet name should be either fleet project number or id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#upstream_fleets GkeHubFeature#upstream_fleets}
        :param gke_upgrade_overrides: gke_upgrade_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#gke_upgrade_overrides GkeHubFeature#gke_upgrade_overrides}
        :param post_conditions: post_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#post_conditions GkeHubFeature#post_conditions}
        '''
        value = GkeHubFeatureSpecClusterupgrade(
            upstream_fleets=upstream_fleets,
            gke_upgrade_overrides=gke_upgrade_overrides,
            post_conditions=post_conditions,
        )

        return typing.cast(None, jsii.invoke(self, "putClusterupgrade", [value]))

    @jsii.member(jsii_name="putFleetobservability")
    def put_fleetobservability(
        self,
        *,
        logging_config: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservabilityLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#logging_config GkeHubFeature#logging_config}
        '''
        value = GkeHubFeatureSpecFleetobservability(logging_config=logging_config)

        return typing.cast(None, jsii.invoke(self, "putFleetobservability", [value]))

    @jsii.member(jsii_name="putMulticlusteringress")
    def put_multiclusteringress(self, *, config_membership: builtins.str) -> None:
        '''
        :param config_membership: Fully-qualified Membership name which hosts the MultiClusterIngress CRD. Example: 'projects/foo-proj/locations/global/memberships/bar'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#config_membership GkeHubFeature#config_membership}
        '''
        value = GkeHubFeatureSpecMulticlusteringress(
            config_membership=config_membership
        )

        return typing.cast(None, jsii.invoke(self, "putMulticlusteringress", [value]))

    @jsii.member(jsii_name="putRbacrolebindingactuation")
    def put_rbacrolebindingactuation(
        self,
        *,
        allowed_custom_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_custom_roles: The list of allowed custom roles (ClusterRoles). If a custom role is not part of this list, it cannot be used in a fleet scope RBACRoleBinding. If a custom role in this list is in use, it cannot be removed from the list until the scope RBACRolebindings using it are deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#allowed_custom_roles GkeHubFeature#allowed_custom_roles}
        '''
        value = GkeHubFeatureSpecRbacrolebindingactuation(
            allowed_custom_roles=allowed_custom_roles
        )

        return typing.cast(None, jsii.invoke(self, "putRbacrolebindingactuation", [value]))

    @jsii.member(jsii_name="resetClusterupgrade")
    def reset_clusterupgrade(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterupgrade", []))

    @jsii.member(jsii_name="resetFleetobservability")
    def reset_fleetobservability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFleetobservability", []))

    @jsii.member(jsii_name="resetMulticlusteringress")
    def reset_multiclusteringress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMulticlusteringress", []))

    @jsii.member(jsii_name="resetRbacrolebindingactuation")
    def reset_rbacrolebindingactuation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRbacrolebindingactuation", []))

    @builtins.property
    @jsii.member(jsii_name="clusterupgrade")
    def clusterupgrade(self) -> GkeHubFeatureSpecClusterupgradeOutputReference:
        return typing.cast(GkeHubFeatureSpecClusterupgradeOutputReference, jsii.get(self, "clusterupgrade"))

    @builtins.property
    @jsii.member(jsii_name="fleetobservability")
    def fleetobservability(self) -> GkeHubFeatureSpecFleetobservabilityOutputReference:
        return typing.cast(GkeHubFeatureSpecFleetobservabilityOutputReference, jsii.get(self, "fleetobservability"))

    @builtins.property
    @jsii.member(jsii_name="multiclusteringress")
    def multiclusteringress(
        self,
    ) -> GkeHubFeatureSpecMulticlusteringressOutputReference:
        return typing.cast(GkeHubFeatureSpecMulticlusteringressOutputReference, jsii.get(self, "multiclusteringress"))

    @builtins.property
    @jsii.member(jsii_name="rbacrolebindingactuation")
    def rbacrolebindingactuation(
        self,
    ) -> "GkeHubFeatureSpecRbacrolebindingactuationOutputReference":
        return typing.cast("GkeHubFeatureSpecRbacrolebindingactuationOutputReference", jsii.get(self, "rbacrolebindingactuation"))

    @builtins.property
    @jsii.member(jsii_name="clusterupgradeInput")
    def clusterupgrade_input(self) -> typing.Optional[GkeHubFeatureSpecClusterupgrade]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecClusterupgrade], jsii.get(self, "clusterupgradeInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetobservabilityInput")
    def fleetobservability_input(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecFleetobservability]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecFleetobservability], jsii.get(self, "fleetobservabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="multiclusteringressInput")
    def multiclusteringress_input(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecMulticlusteringress]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecMulticlusteringress], jsii.get(self, "multiclusteringressInput"))

    @builtins.property
    @jsii.member(jsii_name="rbacrolebindingactuationInput")
    def rbacrolebindingactuation_input(
        self,
    ) -> typing.Optional["GkeHubFeatureSpecRbacrolebindingactuation"]:
        return typing.cast(typing.Optional["GkeHubFeatureSpecRbacrolebindingactuation"], jsii.get(self, "rbacrolebindingactuationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureSpec]:
        return typing.cast(typing.Optional[GkeHubFeatureSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GkeHubFeatureSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8d8fa0eab991fd969df830414c08fea85d71a97075b940824875cddddda560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecRbacrolebindingactuation",
    jsii_struct_bases=[],
    name_mapping={"allowed_custom_roles": "allowedCustomRoles"},
)
class GkeHubFeatureSpecRbacrolebindingactuation:
    def __init__(
        self,
        *,
        allowed_custom_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_custom_roles: The list of allowed custom roles (ClusterRoles). If a custom role is not part of this list, it cannot be used in a fleet scope RBACRoleBinding. If a custom role in this list is in use, it cannot be removed from the list until the scope RBACRolebindings using it are deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#allowed_custom_roles GkeHubFeature#allowed_custom_roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53bcdfdc23bc46487b74447b98fc61ced1efcb733c8fdd16ed3077a9f6022b34)
            check_type(argname="argument allowed_custom_roles", value=allowed_custom_roles, expected_type=type_hints["allowed_custom_roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_custom_roles is not None:
            self._values["allowed_custom_roles"] = allowed_custom_roles

    @builtins.property
    def allowed_custom_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of allowed custom roles (ClusterRoles).

        If a custom role is not part of this list, it cannot be used in a fleet scope RBACRoleBinding. If a custom role in this list is in use, it cannot be removed from the list until the scope RBACRolebindings using it are deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#allowed_custom_roles GkeHubFeature#allowed_custom_roles}
        '''
        result = self._values.get("allowed_custom_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureSpecRbacrolebindingactuation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureSpecRbacrolebindingactuationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureSpecRbacrolebindingactuationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae3b1a756ec34d4da38fc2584326575cf7d26df8cad59214d8091f9620125c80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedCustomRoles")
    def reset_allowed_custom_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedCustomRoles", []))

    @builtins.property
    @jsii.member(jsii_name="allowedCustomRolesInput")
    def allowed_custom_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedCustomRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedCustomRoles")
    def allowed_custom_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedCustomRoles"))

    @allowed_custom_roles.setter
    def allowed_custom_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db544d4fe19e08f2f08a4204dec8e1cbb96029c0d4ba040e7c7bb19c0502acf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedCustomRoles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureSpecRbacrolebindingactuation]:
        return typing.cast(typing.Optional[GkeHubFeatureSpecRbacrolebindingactuation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureSpecRbacrolebindingactuation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf5791485202b41107cbe72cf89f6585ef8d8d4088dee87697a1193914c2295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeHubFeatureState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18a24cda2552f89ea775c9ffc65f2c0d0c35caf4e7c7a7ffad8f87fa96ea2159)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GkeHubFeatureStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45448dda26a2061969daf29a989b088aa27d4bf4407c6ce7e21b3030355fe26c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3737c59ce12a8e1bc5d7484507e1729fef47944a49ed18a599192efa9df091f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a547b379a8e7b218b291197b37e794805cf23ead34d227e6a90cb734c565ba00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17300cad930d1605c5bf21980a0e6522a4d4a3c29b79ec3f2857c4dd82c16e78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__209a2a3497d66f97f3799730c0741e9854a7cb044c80973f3010e807ec8dc864)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> "GkeHubFeatureStateStateList":
        return typing.cast("GkeHubFeatureStateStateList", jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureState]:
        return typing.cast(typing.Optional[GkeHubFeatureState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GkeHubFeatureState]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a4b5463573e3596c2418486fd0c5d64039cd4e23fa475eaf7880dc3f10535f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureStateState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeHubFeatureStateState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureStateState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureStateStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureStateStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc070dd9ef24311bd600f204701b63923e80dc51075755a10d27ee2056271a6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GkeHubFeatureStateStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a60b7232d286898e96c0f89aaf766b7f2604e7fa451ebcf5bc428fef6b6ce7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureStateStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c72eeb9c5c491886ee3a0f76920b2be92b6db291d80b5a491fa3a1fd69f8fe30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f67886f891b39422f70a8882e4d651e4189e55183855dec13a7d40d7b193777)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c470d04d92bb6a6388776232ed7338fcec64c389b99929eb48f85f84333fb6a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureStateStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureStateStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e1d91a8d54c84d61f80ea6cd8788ef3871449fa15aeddada9e9b50f822c5d71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureStateState]:
        return typing.cast(typing.Optional[GkeHubFeatureStateState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GkeHubFeatureStateState]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1213261b9efa354ff823baa647b452b75f2a2f72c74e30297547cbaf888e92c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeHubFeatureTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#create GkeHubFeature#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#delete GkeHubFeature#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#update GkeHubFeature#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf89b32285c28e02e496862b4900cced96d984060b303179a8af09c5f45a8e83)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#create GkeHubFeature#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#delete GkeHubFeature#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature#update GkeHubFeature#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeature.GkeHubFeatureTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa96931188e82b4d32061d7d49abb25b81d966a4a43568d69480a7f41ef3a828)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a99e9f6faca5ec732456bf1268e1bbb8c1dcce0b7b5abb6d2af0d7eb313a0b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__695232b98c003b755334fd66d011ec42779f5b5bb17b050396ab97640305e7ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2012273f21a1b1460fbd0a640e059067a6e84a431e11df4a639de8a74a3883e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a999d1e826cd91ca7848d0f14250a8b6cce08065cb7ab3bf7b3779673777876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GkeHubFeature",
    "GkeHubFeatureConfig",
    "GkeHubFeatureFleetDefaultMemberConfig",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagement",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigMesh",
    "GkeHubFeatureFleetDefaultMemberConfigMeshOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontroller",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationList",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary",
    "GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference",
    "GkeHubFeatureResourceState",
    "GkeHubFeatureResourceStateList",
    "GkeHubFeatureResourceStateOutputReference",
    "GkeHubFeatureSpec",
    "GkeHubFeatureSpecClusterupgrade",
    "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides",
    "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesList",
    "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesOutputReference",
    "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions",
    "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditionsOutputReference",
    "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade",
    "GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgradeOutputReference",
    "GkeHubFeatureSpecClusterupgradeOutputReference",
    "GkeHubFeatureSpecClusterupgradePostConditions",
    "GkeHubFeatureSpecClusterupgradePostConditionsOutputReference",
    "GkeHubFeatureSpecFleetobservability",
    "GkeHubFeatureSpecFleetobservabilityLoggingConfig",
    "GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig",
    "GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference",
    "GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig",
    "GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference",
    "GkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference",
    "GkeHubFeatureSpecFleetobservabilityOutputReference",
    "GkeHubFeatureSpecMulticlusteringress",
    "GkeHubFeatureSpecMulticlusteringressOutputReference",
    "GkeHubFeatureSpecOutputReference",
    "GkeHubFeatureSpecRbacrolebindingactuation",
    "GkeHubFeatureSpecRbacrolebindingactuationOutputReference",
    "GkeHubFeatureState",
    "GkeHubFeatureStateList",
    "GkeHubFeatureStateOutputReference",
    "GkeHubFeatureStateState",
    "GkeHubFeatureStateStateList",
    "GkeHubFeatureStateStateOutputReference",
    "GkeHubFeatureTimeouts",
    "GkeHubFeatureTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__15da6eaa3ff0c55b3dff385d70176ea2bd8835bf45ef327deb74c261fd6ac44a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    fleet_default_member_config: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[GkeHubFeatureSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GkeHubFeatureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4aaea1ebfac8ca28455fa4c0f1b0f746f0c3797b35647135f50498c8df8812c0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae9a2ce391dcaa8ee000a5107c326540f8b9c30bea48ffb61b5cfdf21e4bda2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1c4356cc9f935ee9239eef88ebf69a26f09857659e653ec9afc97c6f1a3084(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87906e5e9de78c2b73f818d12a9adc4ece5fdcb25a576b7c847697b305fdfbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86172f659954d4ad2a80245204f7c53fc1b655e13d03eba59c7731da1117141(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922739c77119c248f5d1192543d5aff17fef63c95a65453f19cd71901acbfc37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a972c15bd6c1e15f9e9f64da9624d0c473d944f00af1591b7529f310c108616(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    fleet_default_member_config: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[GkeHubFeatureSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GkeHubFeatureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c6c3cb298d5d3abbba7b33fc9cea3023e11cac6602ef4726ff31d133391199(
    *,
    configmanagement: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement, typing.Dict[builtins.str, typing.Any]]] = None,
    mesh: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigMesh, typing.Dict[builtins.str, typing.Any]]] = None,
    policycontroller: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontroller, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b2618b3fdf90fc25064fbb89ebddfdaa38c42afff93f3abdc040773f5ee8ea(
    *,
    config_sync: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync, typing.Dict[builtins.str, typing.Any]]] = None,
    management: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c0aea23d86f0a5e0b6e17a11161be2637487e29297ebb1b70f545ad223a337(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    git: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit, typing.Dict[builtins.str, typing.Any]]] = None,
    metrics_gcp_service_account_email: typing.Optional[builtins.str] = None,
    oci: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci, typing.Dict[builtins.str, typing.Any]]] = None,
    prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c84c552a77e21b661dc33c9bf0f36cf74727c9adf91b4d2601ab26a2c27556(
    *,
    secret_type: builtins.str,
    gcp_service_account_email: typing.Optional[builtins.str] = None,
    https_proxy: typing.Optional[builtins.str] = None,
    policy_dir: typing.Optional[builtins.str] = None,
    sync_branch: typing.Optional[builtins.str] = None,
    sync_repo: typing.Optional[builtins.str] = None,
    sync_rev: typing.Optional[builtins.str] = None,
    sync_wait_secs: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff91e5395c7d8494383f90cd73c09d2dd8b49f8b0408245612c2b52b9815babc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196b0d51f9f540fe5bc003f1a4a3f5f830a78f245d58b6df67a8291babedd3c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b40806f21bec7a33a3d0a05adc0db6118625cea44a8ed6e7f93c17938cacbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787a7c1a4723d01285e104ffc9a78e7c0fc4878f37dfa1b7c033a4647f59d339(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55d2b640c416d2540e2b93c5d6420d7642ec244062ce1819f1962ddb0a343d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb5515e78bff91ea3fb4fe1bcb228d6579445fb10a28bdd077e74e40b2f0b81e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41515055982a396422d049350ebb71da25079c1e73696caa73461890b0467bad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8216d27dda54e295217b0a394961ae66152058b7f93adc6c4a18471bed346862(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c2a3cc7605b23f3132ed161966b87a9c1677f4fc79584b44168df3e8c646e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdd6231f4960552f423fbff7d1fc3c8ebc66edccb859514c866c5876b6c0dac(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce9168f80bcbf2ed6498d161e113a23c96a174d7f2ebd50d3fd19c0bc5180d0(
    *,
    secret_type: builtins.str,
    gcp_service_account_email: typing.Optional[builtins.str] = None,
    policy_dir: typing.Optional[builtins.str] = None,
    sync_repo: typing.Optional[builtins.str] = None,
    sync_wait_secs: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c15e3ca25981c7f03e2408f1ac7a88101b6a3cebd01fb356eea913dd96892b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21ec10a1a4ba51ef2af5fec57de8407c6721ed69dd52aa9e03a4b07fbc762b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d5997a29f7a9eed5397903e2a0630110e9d3a9ef9503bd2a4fe6a166593de3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2308501d92e0f66a791e4d27daddfd971712e3a1034dd35a5e98810a5eea6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0925139c6ba0bd061b4ae3c8e19e7eea4c89fd800a55b8d8e638e59bef70ff6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c1d3c4621f9d7c9f1a2aca9621a651d5f5027c7e314896431269896fdfedd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c2299add112fd41088c3fb23b0e5d70ab93879bdb52c2e1ec3665e6a259868(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323b074cd209eb6944e126eb1514a94dac1f8ce03c40a2bab080388f6be6bc4d(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10866afd9d433a8facfa7d40612b05ad041b1bc7563026466a83f65fa3e15b38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f520522133ad2dca70008175fb2d8d47f6e37686334f0b50030f84a8bdb7b177(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7656f2fc5b93f36760e5aed15d71d7b01c89f99580160bb63bf572289582a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9886a70546f10fe84a5fff483d135c11c66473ecbd0e20a0607aa7707ee55b5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0005589a138e2476a6d151250eda755a236b9174826dce767021f5d8d1fd5ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df7297b9140068ea436f0d9e8c411e74ff63b0ea1e3bac1b259544f76e75f20(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5e528563f1854bc24f47208a109ce6d765fefe5b5b1d8c9d20b42d1a90d5a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111bc36f79a866a30a99e6fdf914ef74ffeb65988bd8da2fbe7ad38b77052c2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1075540d3b7fc3741f068a4a4f1022b9d495ceff54c9b9a6b91d72aa29f29a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15bcde01ed2bc266b78a27d6599b009218e3e8edaf01d1a37d49fab108ae1b4e(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigConfigmanagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70aa677d42337c252333b2bb6e9e543e1628acdd851dcfa2b3198a55dcb8e09(
    *,
    management: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed1734dd7111c9c92f93bd59b8e880bc995fe09f06001bb6ce8b06158bc6d14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9e2e90cf66625ffb49d6e97ac3e92eba6b16fb920507b37e1c6f7d07cd59ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f31e7c0a95ca8fd5449f298e72bbcc8be66ccc4710cedddf99847b219999a2(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigMesh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee1feb5904aedc22f8e0941935b9df22576374ea2ba206d55bed9109d999bc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cfcbef1a6482f9561f8124ac2c93a3bd22c7b53e212f7c4bf06552a7d9e8612(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9f161a2695f43e400b81e3a28c43ce3d956b7c70c6793391a2e84e9197e139(
    *,
    policy_controller_hub_config: typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig, typing.Dict[builtins.str, typing.Any]],
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66cc4cfe66b1018e24861ab4e00451da445fd484900e7c29883c71160935536(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbfbaa2f36d419131ec3e994856e923e557d6a1289a9b1e0262abc8a10c9bd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c8d47f340f96b635824cc28309d83eef0f9171bd35019e21b9ab4993c29565(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontroller],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447e41a47606b2d9b5fe8524d4cd9fb7a69d777411335bb221ff82ce9d2a6cc5(
    *,
    install_spec: builtins.str,
    audit_interval_seconds: typing.Optional[jsii.Number] = None,
    constraint_violation_limit: typing.Optional[jsii.Number] = None,
    deployment_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitoring: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring, typing.Dict[builtins.str, typing.Any]]] = None,
    mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policy_content: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent, typing.Dict[builtins.str, typing.Any]]] = None,
    referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430ea392a5df56d4a0343a947ca4f046e6175acec57f22f236b55f7712fbfe2d(
    *,
    component: builtins.str,
    container_resources: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources, typing.Dict[builtins.str, typing.Any]]] = None,
    pod_affinity: typing.Optional[builtins.str] = None,
    pod_toleration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    replica_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0dafe1580a680953fd5b0e9a032d04cf98903d9944c71d391b9d9f37d61ab0(
    *,
    limits: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    requests: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea24db54bd9f12c4481fa9360948b13e78f5799ce1cb26225a6021962d0c1e8(
    *,
    cpu: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5459cdd52863d93d971376103e2cef0f3694465da483187cb5099e92672487e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73603818615be005ca7e6b1b7c1b169220f2c2294b170542bdb30719f157edad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b639f109076f65ed2f9f0c10fedfe619eba6736b4b5707dcc08fbc83d4fff31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da822abfd060659b2ede0f6220491eab6c94b872ee8e5686f9950a441af66ac(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785e0c816a5faf65106910f5c55b538c29bd7b5ef96a6db35f8a8e7ded009e82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0470ca1b291c9c152f186b71ecd90f6bdb06de859743965424b1af72784860e6(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23ff8f0d97dc9ab1f38e7a01eb92488e3e1eb1f58dded23192819c880b5a310(
    *,
    cpu: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc2a40f229f855884a0244e612350b9db552abb6a0c408062fc8ae7876efc50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf95f5c396106923fe3a1ebbdb04a8c21151e1f426db058b1ea15dbfd964c46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c2530aa4c8c1f8c0d5b02dba3778f7e87ef8fa5f095bf71ca5bb9b8f826b73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626b155db1e76429da17e8f180f16545c681dfdfa224d955679a6884ee64bc1d(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07fa20cc776000ba8e8c4d79aad80350bf26248b11f44bb88824017839c1ccf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edea6db951330fe988334aa18105538c165abb8ab1cc867e83847a0579228f8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33fdef95f40fe5aab7189cbc2527e97e3814982fa0c4a0b10b68fb20c626d126(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3afb9cc8951ee966e0b2ef17240b0507b7972b866e0f1ed7ae4b268863fb45dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38b724837cbe88d12be4c9a763dee4c3ad6bcbb7ba45a666b6ac4fdc9863df6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e83f671a363e06964de082cd3a7552fcdca0bf3b33908fe293160416ac31c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1eb80ef609bd0eb39030367174306afac4dccc69432ce665e96fa5932438c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ee2646de12ea5c363d4004dcf1f6a10647d5358aa68a8133f4653f2c739033(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df88e5556478023172b22f692d6cba415f077f2b6158eefed0bd09052d5d375f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4423a319fee75e4107087dee281a3bed137af52a39f16fe33543dd13ed75a01d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e422368739aa3c597e199b480d6b588533b7f6794274acbd8df3e0c1460a859(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126edde667752d2bd442ab6f17941be84e1d297c7908f63f9c349bb345edfa4e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def2a21811bbb25d985c07e75f6db28bf42e8a0fe9b5762df25e663707ebdacc(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f65ad0aea6cd8036f544e331017f9b526ea0bb505cdeed50ace9916230756c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a529b047867d8182333efb4b974dbbdce9d5807637a389cd2eb2fe8ad29262c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb95ad2bc253657cc7e034b2c0cf129f7fc8769b6a1fe72b345b80dd4ec568b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12f49d2211a54de150ae7dc577fb09d7d6487e91bb75d5a6dbbcafc34a8df17(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49cf19ca6ac7f3e256347eef8c279adf0f796565eab13898dcc93a1c093a9486(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849b618d35995cc8a3d6b8cccfc60d49a87c975b77f4c709918b12f0902456d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816c364f44c177ee7adf96373751e77a5af83bbe789944ae3891b185c531c791(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144759d622507850c27b092cf6622d82f0acad57ddbff334b58037c27aa92eea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6708df6b55b3168b44738b6ad1298552bc3baadaa0f3c7748e1d9143e31408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79718ab84ad1c94d57b8c560a653cd67a445826b14297d5f1dd95304d169aae8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6447a89df4de77daff49ac342beb2733af8587c83ec59b81f39a6378ec48501f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11bf7e52cb89d99554f0ff31fc332b0f950bc13a11a07146c84f922c24fb35c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3c2678ae323eb6ccdc7bbab4a1b3515dd926e679313c04a59cdc7b6ef04140(
    *,
    backends: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a15e5984f64663f9c92e1ad48453cd3a9079c6310d2853047057af343230e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a137d6bc58e665e937a165b4b322a78e9e8deb2322c9f105ea660dbbe03bd23(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba8a9fb82da352b6c47812f1498c4fe3640b56a807edad59c3a748daaaf212b(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5541d177a83cc9080bf1b2bb2296cb4abc623172fa9ab6b159a9c22db6862fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1d1a954b26416a8de672ac374a40e73db8e7c91e42821061e6bcdec1268fdc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7e977424951320a68434bf2cb63f823d33ea003ec54993dc3d0f27d774a0bee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab56625e57ba0467563ed23108e610043d67ffd048618ea26cc62fa303a9304d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af88697833a2623b6c3f99023e96e14b3dc1cb6c44b8be2bfee69e0c2293094d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968e8e2b18e2cd9bbd4bfeaf83aa178ab5ece6ed8e9f631bccbfc3e90a880fb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e3496f2a0162159bcda1e7c452cde766783f16715bb01d6b16ef931697c441(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1e42d1b0bf068ee836ee72a58fc9bf4e997686afc3efaaf726efdb70e9cbc6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c992efc35dca1c451b609a3d5ff53dd4a202dd88df1116a6dd5d32bfa9ce1582(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffdf031201721ab07fd7cb070b34f3fe209cb40fbe185e6a72b9e476adf5a292(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64b2a1b79347ed610e483ddb92256474268f284f08d39f279203118cb924e9c(
    *,
    bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles, typing.Dict[builtins.str, typing.Any]]]]] = None,
    template_library: typing.Optional[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8535feade9e0add025c3920d347bf701d6c7f8fd9cbd844f2f00d36c11c23e01(
    *,
    bundle: builtins.str,
    exempted_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd4cefe9b03ba30e3e51da017e2df98cc55e395d131c663927eca8ac9f15e67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3bdc2a556f95d0761d5e708e349f930404753a89c365e4fcd6faffbe704285(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3793b1c6e736b27f4e919aa3d79011cd761102acb7f656e34bb65a8291c1985(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd0837593625d4d894281a6fb5ee4b1168ef38bf0194273d056d39049db634e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e364a5ad00da88c58d514af650a4e106f0fc4aa4ab431cf3e5e27de78f82b1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec33b015c8f652353e6bc87b4ddd58126bfbdb234b527e2bb1f98790ca356e43(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730c1d2a813f511a3c6accab394f0ea2ee25a261298cd386e7a267a466905f5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae87e2d96ba343a71ac6cb1a8aa31de76da0923dc3fc4acb376facae844e7d9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dffc47a5d95312de89f1c2679e3e53dc70de089ac4a9d1d12ca4a7d962afe1e2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc281dc670546574fa4b7296d55b779b5bab72215625100621ca243d13454fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a0f6e077256a27c5aea28e8f77d275cedb7739b91c1425e7cb8bd8ed78d138(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0963eb95b502a692636dbd7200ce8d0e07b98bd4f93466104d6f709597ba5016(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a3908ac408695f717040bfe288d49e60c34353b033d6fce0f653ad6b11ad9a(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91424fb6f79903b86a9c718fedc7b5a48ad4ac8619b16375574d0e36024eddf9(
    *,
    installation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1723ddebdd3c15275b406c5280cbb4932f1be28e1a58d34dcb2c3aed91a4e590(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbab8a094e2187bad12f39e498878612499d3dbe66fd74f9f4fa878020d35c5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a0ee3581da5d3aeaf54f1fc928e5e042b3d60d2ec2f0558903e7df7f21d143(
    value: typing.Optional[GkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51fa5def0c74b8743eb9dde5b12030b076d80f4991a1b7cb4ac34f6e941bb2f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169e4dbd3e43a7981594669bdccb7718cef6c8c85402578e2ec5b7ece57b8af3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e90d2820e7dd4f098245f37a003b5de2956ec80f4c1248e1674d643af918857(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6376c67b67fb947da465a31a757336f1ffe10f32c58c4a2ac52ddf911da9cb1b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffaef58b50a8ece292d1202c1fa9c1b4833922d8bc5445706a29e38808cec8bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9b755f910d09e2cc696919bb5bf80e0cbea3b02a17dfa4b51c8ab6b7f57016(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0301590450c6283eebb008508d183857209ec55a5ae10acc873fc46846ae2e7d(
    value: typing.Optional[GkeHubFeatureResourceState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a716320b8f8b882d1cad6fcfc3c62e854fb6fab48035624c314bc71304c2453b(
    *,
    clusterupgrade: typing.Optional[typing.Union[GkeHubFeatureSpecClusterupgrade, typing.Dict[builtins.str, typing.Any]]] = None,
    fleetobservability: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservability, typing.Dict[builtins.str, typing.Any]]] = None,
    multiclusteringress: typing.Optional[typing.Union[GkeHubFeatureSpecMulticlusteringress, typing.Dict[builtins.str, typing.Any]]] = None,
    rbacrolebindingactuation: typing.Optional[typing.Union[GkeHubFeatureSpecRbacrolebindingactuation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422aad5b19e4356dc05157719e07d849c96c978e43ceb475c33b8afe28d0008e(
    *,
    upstream_fleets: typing.Sequence[builtins.str],
    gke_upgrade_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    post_conditions: typing.Optional[typing.Union[GkeHubFeatureSpecClusterupgradePostConditions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295b00727e5a5b2f2dbc90125f6c1c32e599be9d7dd214a8f01628270a1a1765(
    *,
    post_conditions: typing.Union[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions, typing.Dict[builtins.str, typing.Any]],
    upgrade: typing.Union[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63ca39571dc5cd55e9bcab6ab564e06cb063c4b54785c1d94d435182785ac84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e847c8d5e15d79a848734b0ce91e312688eeae7eb80a7326e486fbaede807c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63780bd7156ddb4cd657130ce02a27ecc9474a64c25761dd0dbd1901d71ac85e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b630118727b1103be516f28efa34ffe595fb5ea27bf14d3644e55d0fcfbfa345(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d74705166d212b36a770726590f6193cfe369e0bd977f3633a51be19f9a495(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7387fc9172a105c3de14215daf78e584c19537252f34d1922f769afb442b6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5018478af9ac11c4d14bc312edbdf0527b6e7a63ff5d5f929d2ecca5348f3086(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444f092d6adf02a66163230875e966e45b76d9cc5c9104caa47f0049dd1efc1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97fc8b63a540e6d759de031766a79559f50aa5a509c1253678c5dea18b3fd699(
    *,
    soaking: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641c27807576fcf7cd56e15d08d1f4b39d68bc07529b82eb78df27b6ec3f98aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1ffe6ab47a06aaf147685bb53c96cb6eaa196f9c23bbd60deeaa4135aa2031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae6bc8429d2fbd0121875adb734926f208731a737d34da4dd8873ebb3c6bac6(
    value: typing.Optional[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a482714d0334cfe20337b73af514474962652adf0debfe14f1903a720556a3(
    *,
    name: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89af15afb78fdc835e5a1a44c3b2efec697de36a7aba124bbe1979430fb7c554(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f8ac91749ffb513331400a8faf9d2171dfb0a489a21b9e3a410eeb3f8f5de9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22491371982f99c04cf2f030a7abc3b3001ce68e183810c9b1a6169352207ef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ba1351bfe71d80e7a808eeef62d841cf0200259d8eb03f58b708059d0a6694(
    value: typing.Optional[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f56ca5f7ff1c19850775d36296c14ae679fa49423940f8440eda9415085001e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac4ffb472fd20cb48b15d1fbdf2088c1204f7c5711b690ae8604532ed4cb9fd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c857b73e84a92c855aefa49a18508ec313f6e0ba9e8e072a0e6b91b957a77fec(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b2ceb32f289efcf9d126a577c1429c99a67dfca2765c92903e9004cfff034c(
    value: typing.Optional[GkeHubFeatureSpecClusterupgrade],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ddb0b8cf65ba648cd588f7045003778bb81c6ceabd69aa4983915590eeab864(
    *,
    soaking: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522c16537c2030f35c821a82ffe81c9a8380b946bdfea4c974a600b3aa3f7e36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c547bc8da54b9d9eba7deca3a74970066f8b3448b21a517ae611a0cafc5835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa016000beba25e15d657b6a5311f4635e443edc360aa2c53c7e6dc750ff131(
    value: typing.Optional[GkeHubFeatureSpecClusterupgradePostConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030a905466c4f9658d40701158addfebf98ef14c6c84a43cdd13d5ba7a55670b(
    *,
    logging_config: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservabilityLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052b23094a3454b7a310041016ec2a7c7ba987f03eacf5ac5a28c8328074811e(
    *,
    default_config: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    fleet_scope_logs_config: typing.Optional[typing.Union[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684f07004b1ba6f1f8d8210a6d8f55a5b9e71793ea2dd271410e09057bf670ce(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eefa415f8be9ad5f0084e817c76a09dfcd7f3d4ebc38d5c8d8005bf3ca26347(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b36e41c88ff90e7c3ac695aaa0d8a66814ac975ea59594c975ce23ec284dde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abb6ffe810d324d665591d0e1dc7deeb2de562a5571ecfafa46e3ed8801e8e3(
    value: typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59cdac985bb9fb598a09f83796f0d95e39afb6c9258d8a3f9b900ff953ba91a5(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d8228dc60e23fa3ca020047c75c220dbb36cdcf72e723161170edb0817fd0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d5864bccefcbd7788e4cf6385173e4cafc7cde89842f64b6035871d08d2dc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19855e3fa053dde6fb0ff5978dc5bdc59eff9aa0a1c445915bbb3dc3bdba55a3(
    value: typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d845075062d30d7e7f9f6a20d4a519ea3dd3c5b2bd23e55ac16814d01a83f188(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2eefb77c01d055b0e63a5526402c6a1a51e3434075a2c39d13f641b987098b2(
    value: typing.Optional[GkeHubFeatureSpecFleetobservabilityLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb4c97d07dd08c1bd71296d80b57fadaffa68ec990d5d377d04725e7b97412c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27a2569d413f9d62089e0030491958ab16fcc8141fbae5bec1cdd5f53342a74(
    value: typing.Optional[GkeHubFeatureSpecFleetobservability],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42001b933a09bfedcafd2135e2449a44c8b807f8de748095bcca334fd6e37a1(
    *,
    config_membership: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e787769b7a1016f6952abb8601447de6098f294856b79bae4749ab46b10b75d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3bd2b56883c6f3693de74d0998420c8e5f70cec3de660eeb795d5876487e66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a5845702568e545287521eb4cd522f450b7df32043774f3410e63faf03a0eb(
    value: typing.Optional[GkeHubFeatureSpecMulticlusteringress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39987c2a69b04624c5f234f3f934c5a5ab7e6ef463c757767db320c09d73bdba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8d8fa0eab991fd969df830414c08fea85d71a97075b940824875cddddda560(
    value: typing.Optional[GkeHubFeatureSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bcdfdc23bc46487b74447b98fc61ced1efcb733c8fdd16ed3077a9f6022b34(
    *,
    allowed_custom_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3b1a756ec34d4da38fc2584326575cf7d26df8cad59214d8091f9620125c80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db544d4fe19e08f2f08a4204dec8e1cbb96029c0d4ba040e7c7bb19c0502acf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf5791485202b41107cbe72cf89f6585ef8d8d4088dee87697a1193914c2295(
    value: typing.Optional[GkeHubFeatureSpecRbacrolebindingactuation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a24cda2552f89ea775c9ffc65f2c0d0c35caf4e7c7a7ffad8f87fa96ea2159(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45448dda26a2061969daf29a989b088aa27d4bf4407c6ce7e21b3030355fe26c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3737c59ce12a8e1bc5d7484507e1729fef47944a49ed18a599192efa9df091f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a547b379a8e7b218b291197b37e794805cf23ead34d227e6a90cb734c565ba00(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17300cad930d1605c5bf21980a0e6522a4d4a3c29b79ec3f2857c4dd82c16e78(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209a2a3497d66f97f3799730c0741e9854a7cb044c80973f3010e807ec8dc864(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a4b5463573e3596c2418486fd0c5d64039cd4e23fa475eaf7880dc3f10535f(
    value: typing.Optional[GkeHubFeatureState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc070dd9ef24311bd600f204701b63923e80dc51075755a10d27ee2056271a6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a60b7232d286898e96c0f89aaf766b7f2604e7fa451ebcf5bc428fef6b6ce7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72eeb9c5c491886ee3a0f76920b2be92b6db291d80b5a491fa3a1fd69f8fe30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f67886f891b39422f70a8882e4d651e4189e55183855dec13a7d40d7b193777(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c470d04d92bb6a6388776232ed7338fcec64c389b99929eb48f85f84333fb6a7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1d91a8d54c84d61f80ea6cd8788ef3871449fa15aeddada9e9b50f822c5d71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1213261b9efa354ff823baa647b452b75f2a2f72c74e30297547cbaf888e92c0(
    value: typing.Optional[GkeHubFeatureStateState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf89b32285c28e02e496862b4900cced96d984060b303179a8af09c5f45a8e83(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa96931188e82b4d32061d7d49abb25b81d966a4a43568d69480a7f41ef3a828(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a99e9f6faca5ec732456bf1268e1bbb8c1dcce0b7b5abb6d2af0d7eb313a0b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__695232b98c003b755334fd66d011ec42779f5b5bb17b050396ab97640305e7ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2012273f21a1b1460fbd0a640e059067a6e84a431e11df4a639de8a74a3883e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a999d1e826cd91ca7848d0f14250a8b6cce08065cb7ab3bf7b3779673777876(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
