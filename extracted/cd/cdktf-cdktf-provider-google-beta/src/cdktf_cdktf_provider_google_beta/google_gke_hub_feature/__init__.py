r'''
# `google_gke_hub_feature`

Refer to the Terraform Registry for docs: [`google_gke_hub_feature`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature).
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


class GoogleGkeHubFeature(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeature",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature google_gke_hub_feature}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        fleet_default_member_config: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["GoogleGkeHubFeatureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeHubFeatureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature google_gke_hub_feature} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#location GoogleGkeHubFeature#location}
        :param fleet_default_member_config: fleet_default_member_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#fleet_default_member_config GoogleGkeHubFeature#fleet_default_member_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#id GoogleGkeHubFeature#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: GCP labels for this Feature. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#labels GoogleGkeHubFeature#labels}
        :param name: The full, unique name of this Feature resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#name GoogleGkeHubFeature#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#project GoogleGkeHubFeature#project}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#spec GoogleGkeHubFeature#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#timeouts GoogleGkeHubFeature#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb0a3fd65f9fa47bafa789113e2cc02ccb5128458d34d152ae7bd13698b9aa7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleGkeHubFeatureConfig(
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
        '''Generates CDKTF code for importing a GoogleGkeHubFeature resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleGkeHubFeature to import.
        :param import_from_id: The id of the existing GoogleGkeHubFeature that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleGkeHubFeature to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58f967f1975fad4e1ba0d785a20e7605bac04ac05977e754d73c4f641f0a2538)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFleetDefaultMemberConfig")
    def put_fleet_default_member_config(
        self,
        *,
        configmanagement: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement", typing.Dict[builtins.str, typing.Any]]] = None,
        mesh: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        policycontroller: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configmanagement: configmanagement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#configmanagement GoogleGkeHubFeature#configmanagement}
        :param mesh: mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#mesh GoogleGkeHubFeature#mesh}
        :param policycontroller: policycontroller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policycontroller GoogleGkeHubFeature#policycontroller}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfig(
            configmanagement=configmanagement,
            mesh=mesh,
            policycontroller=policycontroller,
        )

        return typing.cast(None, jsii.invoke(self, "putFleetDefaultMemberConfig", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        clusterupgrade: typing.Optional[typing.Union["GoogleGkeHubFeatureSpecClusterupgrade", typing.Dict[builtins.str, typing.Any]]] = None,
        fleetobservability: typing.Optional[typing.Union["GoogleGkeHubFeatureSpecFleetobservability", typing.Dict[builtins.str, typing.Any]]] = None,
        multiclusteringress: typing.Optional[typing.Union["GoogleGkeHubFeatureSpecMulticlusteringress", typing.Dict[builtins.str, typing.Any]]] = None,
        rbacrolebindingactuation: typing.Optional[typing.Union["GoogleGkeHubFeatureSpecRbacrolebindingactuation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param clusterupgrade: clusterupgrade block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#clusterupgrade GoogleGkeHubFeature#clusterupgrade}
        :param fleetobservability: fleetobservability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#fleetobservability GoogleGkeHubFeature#fleetobservability}
        :param multiclusteringress: multiclusteringress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#multiclusteringress GoogleGkeHubFeature#multiclusteringress}
        :param rbacrolebindingactuation: rbacrolebindingactuation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#rbacrolebindingactuation GoogleGkeHubFeature#rbacrolebindingactuation}
        '''
        value = GoogleGkeHubFeatureSpec(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#create GoogleGkeHubFeature#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#delete GoogleGkeHubFeature#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#update GoogleGkeHubFeature#update}.
        '''
        value = GoogleGkeHubFeatureTimeouts(
            create=create, delete=delete, update=update
        )

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
    ) -> "GoogleGkeHubFeatureFleetDefaultMemberConfigOutputReference":
        return typing.cast("GoogleGkeHubFeatureFleetDefaultMemberConfigOutputReference", jsii.get(self, "fleetDefaultMemberConfig"))

    @builtins.property
    @jsii.member(jsii_name="resourceState")
    def resource_state(self) -> "GoogleGkeHubFeatureResourceStateList":
        return typing.cast("GoogleGkeHubFeatureResourceStateList", jsii.get(self, "resourceState"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "GoogleGkeHubFeatureSpecOutputReference":
        return typing.cast("GoogleGkeHubFeatureSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> "GoogleGkeHubFeatureStateList":
        return typing.cast("GoogleGkeHubFeatureStateList", jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleGkeHubFeatureTimeoutsOutputReference":
        return typing.cast("GoogleGkeHubFeatureTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="fleetDefaultMemberConfigInput")
    def fleet_default_member_config_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfig"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfig"], jsii.get(self, "fleetDefaultMemberConfigInput"))

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
    def spec_input(self) -> typing.Optional["GoogleGkeHubFeatureSpec"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeHubFeatureTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeHubFeatureTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f7ee43ae258d522c9ddea24987abb84477958d09875e186a32b9d2d330abbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5541c7fa13f702682f24628bd612b50eb847693374d09fba356f4cf8ec6487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f22c23edb7c67172605b89e0ec8b04b99e5fa900792a2b5fa0f0e5081dffa64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3db494c632e775b125d48a446928f7094203f9499b2591a62874290572a9201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8650d74f696329dae2a01fd36941dc53c4a32755ffe0ed2df00e995d086e9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureConfig",
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
class GoogleGkeHubFeatureConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        fleet_default_member_config: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["GoogleGkeHubFeatureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeHubFeatureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#location GoogleGkeHubFeature#location}
        :param fleet_default_member_config: fleet_default_member_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#fleet_default_member_config GoogleGkeHubFeature#fleet_default_member_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#id GoogleGkeHubFeature#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: GCP labels for this Feature. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#labels GoogleGkeHubFeature#labels}
        :param name: The full, unique name of this Feature resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#name GoogleGkeHubFeature#name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#project GoogleGkeHubFeature#project}.
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#spec GoogleGkeHubFeature#spec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#timeouts GoogleGkeHubFeature#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(fleet_default_member_config, dict):
            fleet_default_member_config = GoogleGkeHubFeatureFleetDefaultMemberConfig(**fleet_default_member_config)
        if isinstance(spec, dict):
            spec = GoogleGkeHubFeatureSpec(**spec)
        if isinstance(timeouts, dict):
            timeouts = GoogleGkeHubFeatureTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf1728319ee978297c79124f6478064ea7f9cd7b09411f94fa2528c1cded37b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#location GoogleGkeHubFeature#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fleet_default_member_config(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfig"]:
        '''fleet_default_member_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#fleet_default_member_config GoogleGkeHubFeature#fleet_default_member_config}
        '''
        result = self._values.get("fleet_default_member_config")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#id GoogleGkeHubFeature#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#labels GoogleGkeHubFeature#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The full, unique name of this Feature resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#name GoogleGkeHubFeature#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#project GoogleGkeHubFeature#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(self) -> typing.Optional["GoogleGkeHubFeatureSpec"]:
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#spec GoogleGkeHubFeature#spec}
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpec"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleGkeHubFeatureTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#timeouts GoogleGkeHubFeature#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfig",
    jsii_struct_bases=[],
    name_mapping={
        "configmanagement": "configmanagement",
        "mesh": "mesh",
        "policycontroller": "policycontroller",
    },
)
class GoogleGkeHubFeatureFleetDefaultMemberConfig:
    def __init__(
        self,
        *,
        configmanagement: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement", typing.Dict[builtins.str, typing.Any]]] = None,
        mesh: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        policycontroller: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configmanagement: configmanagement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#configmanagement GoogleGkeHubFeature#configmanagement}
        :param mesh: mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#mesh GoogleGkeHubFeature#mesh}
        :param policycontroller: policycontroller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policycontroller GoogleGkeHubFeature#policycontroller}
        '''
        if isinstance(configmanagement, dict):
            configmanagement = GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement(**configmanagement)
        if isinstance(mesh, dict):
            mesh = GoogleGkeHubFeatureFleetDefaultMemberConfigMesh(**mesh)
        if isinstance(policycontroller, dict):
            policycontroller = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller(**policycontroller)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e543bd9e370f2eb2897a9d7d6e37a41cd7e903f77ff903e44457606ed1422178)
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
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement"]:
        '''configmanagement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#configmanagement GoogleGkeHubFeature#configmanagement}
        '''
        result = self._values.get("configmanagement")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement"], result)

    @builtins.property
    def mesh(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigMesh"]:
        '''mesh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#mesh GoogleGkeHubFeature#mesh}
        '''
        result = self._values.get("mesh")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigMesh"], result)

    @builtins.property
    def policycontroller(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller"]:
        '''policycontroller block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policycontroller GoogleGkeHubFeature#policycontroller}
        '''
        result = self._values.get("policycontroller")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement",
    jsii_struct_bases=[],
    name_mapping={
        "config_sync": "configSync",
        "management": "management",
        "version": "version",
    },
)
class GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement:
    def __init__(
        self,
        *,
        config_sync: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync", typing.Dict[builtins.str, typing.Any]]] = None,
        management: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config_sync: config_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#config_sync GoogleGkeHubFeature#config_sync}
        :param management: Set this field to MANAGEMENT_AUTOMATIC to enable Config Sync auto-upgrades, and set this field to MANAGEMENT_MANUAL or MANAGEMENT_UNSPECIFIED to disable Config Sync auto-upgrades. Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#management GoogleGkeHubFeature#management}
        :param version: Version of Config Sync installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#version GoogleGkeHubFeature#version}
        '''
        if isinstance(config_sync, dict):
            config_sync = GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync(**config_sync)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea580e2e37453bbfd577e8716127d6f1472dc9e2232bc1bac4999e071e69f93)
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
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync"]:
        '''config_sync block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#config_sync GoogleGkeHubFeature#config_sync}
        '''
        result = self._values.get("config_sync")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync"], result)

    @builtins.property
    def management(self) -> typing.Optional[builtins.str]:
        '''Set this field to MANAGEMENT_AUTOMATIC to enable Config Sync auto-upgrades, and set this field to MANAGEMENT_MANUAL or MANAGEMENT_UNSPECIFIED to disable Config Sync auto-upgrades.

        Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#management GoogleGkeHubFeature#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of Config Sync installed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#version GoogleGkeHubFeature#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync",
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
class GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        git: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit", typing.Dict[builtins.str, typing.Any]]] = None,
        metrics_gcp_service_account_email: typing.Optional[builtins.str] = None,
        oci: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci", typing.Dict[builtins.str, typing.Any]]] = None,
        prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enables the installation of ConfigSync. If set to true, ConfigSync resources will be created and the other ConfigSync fields will be applied if exist. If set to false, all other ConfigSync fields will be ignored, ConfigSync resources will be deleted. If omitted, ConfigSync resources will be managed depends on the presence of the git or oci field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#enabled GoogleGkeHubFeature#enabled}
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#git GoogleGkeHubFeature#git}
        :param metrics_gcp_service_account_email: The Email of the Google Cloud Service Account (GSA) used for exporting Config Sync metrics to Cloud Monitoring. The GSA should have the Monitoring Metric Writer(roles/monitoring.metricWriter) IAM role. The Kubernetes ServiceAccount 'default' in the namespace 'config-management-monitoring' should be bound to the GSA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#metrics_gcp_service_account_email GoogleGkeHubFeature#metrics_gcp_service_account_email}
        :param oci: oci block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#oci GoogleGkeHubFeature#oci}
        :param prevent_drift: Set to true to enable the Config Sync admission webhook to prevent drifts. If set to 'false', disables the Config Sync admission webhook and does not prevent drifts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#prevent_drift GoogleGkeHubFeature#prevent_drift}
        :param source_format: Specifies whether the Config Sync Repo is in hierarchical or unstructured mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#source_format GoogleGkeHubFeature#source_format}
        '''
        if isinstance(git, dict):
            git = GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit(**git)
        if isinstance(oci, dict):
            oci = GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci(**oci)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d13afff405078acd1b3aa212c6e765bbf5e457ce90a0bfd17c9820016f9758cd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#enabled GoogleGkeHubFeature#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def git(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit"]:
        '''git block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#git GoogleGkeHubFeature#git}
        '''
        result = self._values.get("git")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit"], result)

    @builtins.property
    def metrics_gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''The Email of the Google Cloud Service Account (GSA) used for exporting Config Sync metrics to Cloud Monitoring.

        The GSA should have the Monitoring Metric Writer(roles/monitoring.metricWriter) IAM role. The Kubernetes ServiceAccount 'default' in the namespace 'config-management-monitoring' should be bound to the GSA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#metrics_gcp_service_account_email GoogleGkeHubFeature#metrics_gcp_service_account_email}
        '''
        result = self._values.get("metrics_gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oci(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci"]:
        '''oci block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#oci GoogleGkeHubFeature#oci}
        '''
        result = self._values.get("oci")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci"], result)

    @builtins.property
    def prevent_drift(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to enable the Config Sync admission webhook to prevent drifts.

        If set to 'false', disables the Config Sync admission webhook and does not prevent drifts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#prevent_drift GoogleGkeHubFeature#prevent_drift}
        '''
        result = self._values.get("prevent_drift")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_format(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the Config Sync Repo is in hierarchical or unstructured mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#source_format GoogleGkeHubFeature#source_format}
        '''
        result = self._values.get("source_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit",
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
class GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit:
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
        :param secret_type: Type of secret configured for access to the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#secret_type GoogleGkeHubFeature#secret_type}
        :param gcp_service_account_email: The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#gcp_service_account_email GoogleGkeHubFeature#gcp_service_account_email}
        :param https_proxy: URL for the HTTPS Proxy to be used when communicating with the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#https_proxy GoogleGkeHubFeature#https_proxy}
        :param policy_dir: The path within the Git repository that represents the top level of the repo to sync. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policy_dir GoogleGkeHubFeature#policy_dir}
        :param sync_branch: The branch of the repository to sync from. Default: master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_branch GoogleGkeHubFeature#sync_branch}
        :param sync_repo: The URL of the Git repository to use as the source of truth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_repo GoogleGkeHubFeature#sync_repo}
        :param sync_rev: Git revision (tag or hash) to check out. Default HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_rev GoogleGkeHubFeature#sync_rev}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_wait_secs GoogleGkeHubFeature#sync_wait_secs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0721edb45f7f37b510e07059bf09b7cb4d9fbbf5f84bc9612638b01910e585d8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#secret_type GoogleGkeHubFeature#secret_type}
        '''
        result = self._values.get("secret_type")
        assert result is not None, "Required property 'secret_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#gcp_service_account_email GoogleGkeHubFeature#gcp_service_account_email}
        '''
        result = self._values.get("gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_proxy(self) -> typing.Optional[builtins.str]:
        '''URL for the HTTPS Proxy to be used when communicating with the Git repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#https_proxy GoogleGkeHubFeature#https_proxy}
        '''
        result = self._values.get("https_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_dir(self) -> typing.Optional[builtins.str]:
        '''The path within the Git repository that represents the top level of the repo to sync.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policy_dir GoogleGkeHubFeature#policy_dir}
        '''
        result = self._values.get("policy_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_branch(self) -> typing.Optional[builtins.str]:
        '''The branch of the repository to sync from. Default: master.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_branch GoogleGkeHubFeature#sync_branch}
        '''
        result = self._values.get("sync_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_repo(self) -> typing.Optional[builtins.str]:
        '''The URL of the Git repository to use as the source of truth.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_repo GoogleGkeHubFeature#sync_repo}
        '''
        result = self._values.get("sync_repo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_rev(self) -> typing.Optional[builtins.str]:
        '''Git revision (tag or hash) to check out. Default HEAD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_rev GoogleGkeHubFeature#sync_rev}
        '''
        result = self._values.get("sync_rev")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_wait_secs(self) -> typing.Optional[builtins.str]:
        '''Period in seconds between consecutive syncs. Default: 15.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_wait_secs GoogleGkeHubFeature#sync_wait_secs}
        '''
        result = self._values.get("sync_wait_secs")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69ca12cea6baf74a45cc215787ab5e5571e4b15e9adfe0b122254ce5081c86a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d674e1977682fb7e8baada27b075e67e513b3e7fa6194a1fbdd88b48794948e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsProxy")
    def https_proxy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsProxy"))

    @https_proxy.setter
    def https_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd16413611ea85897778be596aa32ac5ade6dd783deb546ee66760cc33d929ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyDir")
    def policy_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDir"))

    @policy_dir.setter
    def policy_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d84128a1235b54c8268f0a1b34c28ed3b4e646ef3c350bbef8f313996b8e5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretType")
    def secret_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretType"))

    @secret_type.setter
    def secret_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a3326516501d9838b678e2db364776f5613f3dc5847ccfb70501abee4074e5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncBranch")
    def sync_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncBranch"))

    @sync_branch.setter
    def sync_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa4bb78b655c841da6d328600412cc59fe133ff1a40748ec28e141b5eb298260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncRepo")
    def sync_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRepo"))

    @sync_repo.setter
    def sync_repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57cc8603bd2fe5d12b054ec8d3f3fbebb57bd4fee5cae57f5507d8f0dc03fd71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRepo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncRev")
    def sync_rev(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRev"))

    @sync_rev.setter
    def sync_rev(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016563e035e5612dbd6ede75a1e8ed695381d29358cd07e0579e8ca241065069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRev", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecs")
    def sync_wait_secs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncWaitSecs"))

    @sync_wait_secs.setter
    def sync_wait_secs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22c6b1303616fe1dfe4298b8cb64d0c1b50b6ed93344f38843b19858852b755c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncWaitSecs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c50993643f6f2eea684201c856ace207ea8116e90d4b1b907a0db7bac98f3532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci",
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
class GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci:
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
        :param secret_type: Type of secret configured for access to the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#secret_type GoogleGkeHubFeature#secret_type}
        :param gcp_service_account_email: The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#gcp_service_account_email GoogleGkeHubFeature#gcp_service_account_email}
        :param policy_dir: The absolute path of the directory that contains the local resources. Default: the root directory of the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policy_dir GoogleGkeHubFeature#policy_dir}
        :param sync_repo: The OCI image repository URL for the package to sync from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_repo GoogleGkeHubFeature#sync_repo}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_wait_secs GoogleGkeHubFeature#sync_wait_secs}
        :param version: Version of Config Sync installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#version GoogleGkeHubFeature#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9cfab22367d7ddc9eb4e8e2e6942e5abfbe420dc1930f40c85ad4a9fc7b90b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#secret_type GoogleGkeHubFeature#secret_type}
        '''
        result = self._values.get("secret_type")
        assert result is not None, "Required property 'secret_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#gcp_service_account_email GoogleGkeHubFeature#gcp_service_account_email}
        '''
        result = self._values.get("gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_dir(self) -> typing.Optional[builtins.str]:
        '''The absolute path of the directory that contains the local resources. Default: the root directory of the image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policy_dir GoogleGkeHubFeature#policy_dir}
        '''
        result = self._values.get("policy_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_repo(self) -> typing.Optional[builtins.str]:
        '''The OCI image repository URL for the package to sync from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_repo GoogleGkeHubFeature#sync_repo}
        '''
        result = self._values.get("sync_repo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_wait_secs(self) -> typing.Optional[builtins.str]:
        '''Period in seconds between consecutive syncs. Default: 15.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_wait_secs GoogleGkeHubFeature#sync_wait_secs}
        '''
        result = self._values.get("sync_wait_secs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of Config Sync installed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#version GoogleGkeHubFeature#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3261b51ddaf26d37116b7adf6f35a96b7119887ef164d6f188ec938f88d9d72d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__480bc25330085595d5edc13198ae9e268d279fb588e2ec03d1fd49513b7f330b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyDir")
    def policy_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDir"))

    @policy_dir.setter
    def policy_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__371eb2a29f8d48c5c678be6235cc737eeef673c2643aee25dea33aba06063aa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretType")
    def secret_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretType"))

    @secret_type.setter
    def secret_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15847209393b1a73e01ca1931e8de4512710496174df853a7b0d7b128573b9d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncRepo")
    def sync_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRepo"))

    @sync_repo.setter
    def sync_repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c063d112c5623252658ba71497e4704f935b4b63ef07d0becbd6221bd2cbe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRepo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecs")
    def sync_wait_secs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncWaitSecs"))

    @sync_wait_secs.setter
    def sync_wait_secs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3bb645f7e8efe18ed9008b95a1916fb4bb0fb05450c4055edd6f00763eb4d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncWaitSecs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a2c942042dd09684426ea69b99bd0a543c896a3ec00321d51f390842ba24b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e109f493d653966a6ef4872199622a6de2fb577dc1a605f5fff7fabb137cf07d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f12093991d4573e8b272cd913c816cad93fda263f5781e6fb4710802d39ae02b)
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
        :param secret_type: Type of secret configured for access to the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#secret_type GoogleGkeHubFeature#secret_type}
        :param gcp_service_account_email: The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#gcp_service_account_email GoogleGkeHubFeature#gcp_service_account_email}
        :param https_proxy: URL for the HTTPS Proxy to be used when communicating with the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#https_proxy GoogleGkeHubFeature#https_proxy}
        :param policy_dir: The path within the Git repository that represents the top level of the repo to sync. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policy_dir GoogleGkeHubFeature#policy_dir}
        :param sync_branch: The branch of the repository to sync from. Default: master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_branch GoogleGkeHubFeature#sync_branch}
        :param sync_repo: The URL of the Git repository to use as the source of truth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_repo GoogleGkeHubFeature#sync_repo}
        :param sync_rev: Git revision (tag or hash) to check out. Default HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_rev GoogleGkeHubFeature#sync_rev}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_wait_secs GoogleGkeHubFeature#sync_wait_secs}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit(
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
        :param secret_type: Type of secret configured for access to the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#secret_type GoogleGkeHubFeature#secret_type}
        :param gcp_service_account_email: The Google Cloud Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#gcp_service_account_email GoogleGkeHubFeature#gcp_service_account_email}
        :param policy_dir: The absolute path of the directory that contains the local resources. Default: the root directory of the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policy_dir GoogleGkeHubFeature#policy_dir}
        :param sync_repo: The OCI image repository URL for the package to sync from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_repo GoogleGkeHubFeature#sync_repo}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#sync_wait_secs GoogleGkeHubFeature#sync_wait_secs}
        :param version: Version of Config Sync installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#version GoogleGkeHubFeature#version}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci(
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
    ) -> GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference:
        return typing.cast(GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference, jsii.get(self, "git"))

    @builtins.property
    @jsii.member(jsii_name="oci")
    def oci(
        self,
    ) -> GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference:
        return typing.cast(GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference, jsii.get(self, "oci"))

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
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit], jsii.get(self, "gitInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsGcpServiceAccountEmailInput")
    def metrics_gcp_service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricsGcpServiceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="ociInput")
    def oci_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci], jsii.get(self, "ociInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3f2d1c21ff56fa649539990efe326b75ebcd9bbc2763922ceaad2f2b4e15a3bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsGcpServiceAccountEmail")
    def metrics_gcp_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricsGcpServiceAccountEmail"))

    @metrics_gcp_service_account_email.setter
    def metrics_gcp_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113b3db8bdaa71efaf995ca7cc6e91451975808c458412795fdb96ba86980e1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f1074eb8bed469b6dfa70674e7508fc68b727f3a73d4819a9906c98b7ffa390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventDrift", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFormat")
    def source_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFormat"))

    @source_format.setter
    def source_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__364e696aa1b39d01aab3aa039de19e783bd8e9c1adb0344bd80756071e8650fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cedf565b3d840e25876cece03876ddec659bde75fc4f9864ac3cf7a0342adc7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca17c0a7173decdf3f45ab38a6988afd1e868369f53464576542506bd1089fc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfigSync")
    def put_config_sync(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        git: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit, typing.Dict[builtins.str, typing.Any]]] = None,
        metrics_gcp_service_account_email: typing.Optional[builtins.str] = None,
        oci: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci, typing.Dict[builtins.str, typing.Any]]] = None,
        prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enables the installation of ConfigSync. If set to true, ConfigSync resources will be created and the other ConfigSync fields will be applied if exist. If set to false, all other ConfigSync fields will be ignored, ConfigSync resources will be deleted. If omitted, ConfigSync resources will be managed depends on the presence of the git or oci field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#enabled GoogleGkeHubFeature#enabled}
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#git GoogleGkeHubFeature#git}
        :param metrics_gcp_service_account_email: The Email of the Google Cloud Service Account (GSA) used for exporting Config Sync metrics to Cloud Monitoring. The GSA should have the Monitoring Metric Writer(roles/monitoring.metricWriter) IAM role. The Kubernetes ServiceAccount 'default' in the namespace 'config-management-monitoring' should be bound to the GSA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#metrics_gcp_service_account_email GoogleGkeHubFeature#metrics_gcp_service_account_email}
        :param oci: oci block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#oci GoogleGkeHubFeature#oci}
        :param prevent_drift: Set to true to enable the Config Sync admission webhook to prevent drifts. If set to 'false', disables the Config Sync admission webhook and does not prevent drifts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#prevent_drift GoogleGkeHubFeature#prevent_drift}
        :param source_format: Specifies whether the Config Sync Repo is in hierarchical or unstructured mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#source_format GoogleGkeHubFeature#source_format}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync(
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
    ) -> GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference:
        return typing.cast(GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference, jsii.get(self, "configSync"))

    @builtins.property
    @jsii.member(jsii_name="configSyncInput")
    def config_sync_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync], jsii.get(self, "configSyncInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d083b135e516c050de2d42e4a4e16bf35e4cefe56e72248ab9c1d54fec45364d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "management", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e5b22a28d29cf3c54e126039d5a0ec911cf227e55d7f09cbffb7b4be05105d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc7698b4f15f358e332419974552d05760e0994029d3e92c5ce5ba706243b328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigMesh",
    jsii_struct_bases=[],
    name_mapping={"management": "management"},
)
class GoogleGkeHubFeatureFleetDefaultMemberConfigMesh:
    def __init__(self, *, management: builtins.str) -> None:
        '''
        :param management: Whether to automatically manage Service Mesh Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#management GoogleGkeHubFeature#management}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c42dcc8e4ea75751510b2c933502f459fd5dc4af69ee20ef8368a7c140cffd)
            check_type(argname="argument management", value=management, expected_type=type_hints["management"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "management": management,
        }

    @builtins.property
    def management(self) -> builtins.str:
        '''Whether to automatically manage Service Mesh Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#management GoogleGkeHubFeature#management}
        '''
        result = self._values.get("management")
        assert result is not None, "Required property 'management' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigMesh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureFleetDefaultMemberConfigMeshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigMeshOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__185134601c70944bb1f7d9bb65b4842ffebb02d54c6802dfd6c9df1c577a363c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9025fbf0d7ee34f3042701e38957e07b761f66810597a18527524680f9b06449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "management", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigMesh]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigMesh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigMesh],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__807901be3db45f3acb440b1fcafd32969740d2201a044e6b1e11bc41299173ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureFleetDefaultMemberConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6710aeb75b71c25ae6d0a4242dfd6b677af815b37af0ccf89decae0228af157c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfigmanagement")
    def put_configmanagement(
        self,
        *,
        config_sync: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync, typing.Dict[builtins.str, typing.Any]]] = None,
        management: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config_sync: config_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#config_sync GoogleGkeHubFeature#config_sync}
        :param management: Set this field to MANAGEMENT_AUTOMATIC to enable Config Sync auto-upgrades, and set this field to MANAGEMENT_MANUAL or MANAGEMENT_UNSPECIFIED to disable Config Sync auto-upgrades. Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#management GoogleGkeHubFeature#management}
        :param version: Version of Config Sync installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#version GoogleGkeHubFeature#version}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement(
            config_sync=config_sync, management=management, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putConfigmanagement", [value]))

    @jsii.member(jsii_name="putMesh")
    def put_mesh(self, *, management: builtins.str) -> None:
        '''
        :param management: Whether to automatically manage Service Mesh Possible values: ["MANAGEMENT_UNSPECIFIED", "MANAGEMENT_AUTOMATIC", "MANAGEMENT_MANUAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#management GoogleGkeHubFeature#management}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfigMesh(management=management)

        return typing.cast(None, jsii.invoke(self, "putMesh", [value]))

    @jsii.member(jsii_name="putPolicycontroller")
    def put_policycontroller(
        self,
        *,
        policy_controller_hub_config: typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig", typing.Dict[builtins.str, typing.Any]],
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param policy_controller_hub_config: policy_controller_hub_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policy_controller_hub_config GoogleGkeHubFeature#policy_controller_hub_config}
        :param version: Configures the version of Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#version GoogleGkeHubFeature#version}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller(
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
    ) -> GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference:
        return typing.cast(GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference, jsii.get(self, "configmanagement"))

    @builtins.property
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> GoogleGkeHubFeatureFleetDefaultMemberConfigMeshOutputReference:
        return typing.cast(GoogleGkeHubFeatureFleetDefaultMemberConfigMeshOutputReference, jsii.get(self, "mesh"))

    @builtins.property
    @jsii.member(jsii_name="policycontroller")
    def policycontroller(
        self,
    ) -> "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerOutputReference":
        return typing.cast("GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerOutputReference", jsii.get(self, "policycontroller"))

    @builtins.property
    @jsii.member(jsii_name="configmanagementInput")
    def configmanagement_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement], jsii.get(self, "configmanagementInput"))

    @builtins.property
    @jsii.member(jsii_name="meshInput")
    def mesh_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigMesh]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigMesh], jsii.get(self, "meshInput"))

    @builtins.property
    @jsii.member(jsii_name="policycontrollerInput")
    def policycontroller_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller"], jsii.get(self, "policycontrollerInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfig]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__998fb7c8ba6729775381015285e37dd962563f46b4bcaa298b549479f942bdeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller",
    jsii_struct_bases=[],
    name_mapping={
        "policy_controller_hub_config": "policyControllerHubConfig",
        "version": "version",
    },
)
class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller:
    def __init__(
        self,
        *,
        policy_controller_hub_config: typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig", typing.Dict[builtins.str, typing.Any]],
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param policy_controller_hub_config: policy_controller_hub_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policy_controller_hub_config GoogleGkeHubFeature#policy_controller_hub_config}
        :param version: Configures the version of Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#version GoogleGkeHubFeature#version}
        '''
        if isinstance(policy_controller_hub_config, dict):
            policy_controller_hub_config = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig(**policy_controller_hub_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45e77637cadef0bcfb4b448daeb4a001144abf9c61c0d01fba368560910aa5ec)
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
    ) -> "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig":
        '''policy_controller_hub_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policy_controller_hub_config GoogleGkeHubFeature#policy_controller_hub_config}
        '''
        result = self._values.get("policy_controller_hub_config")
        assert result is not None, "Required property 'policy_controller_hub_config' is missing"
        return typing.cast("GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig", result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Configures the version of Policy Controller.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#version GoogleGkeHubFeature#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19b2c5334530be3aa815d63d06209f259fb25df2fb44f19504a733d9c0e7f294)
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
        deployment_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_content: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent", typing.Dict[builtins.str, typing.Any]]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param install_spec: Configures the mode of the Policy Controller installation Possible values: ["INSTALL_SPEC_UNSPECIFIED", "INSTALL_SPEC_NOT_INSTALLED", "INSTALL_SPEC_ENABLED", "INSTALL_SPEC_SUSPENDED", "INSTALL_SPEC_DETACHED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#install_spec GoogleGkeHubFeature#install_spec}
        :param audit_interval_seconds: Interval for Policy Controller Audit scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#audit_interval_seconds GoogleGkeHubFeature#audit_interval_seconds}
        :param constraint_violation_limit: The maximum number of audit violations to be stored in a constraint. If not set, the internal default of 20 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#constraint_violation_limit GoogleGkeHubFeature#constraint_violation_limit}
        :param deployment_configs: deployment_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#deployment_configs GoogleGkeHubFeature#deployment_configs}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#exemptable_namespaces GoogleGkeHubFeature#exemptable_namespaces}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#log_denies_enabled GoogleGkeHubFeature#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#monitoring GoogleGkeHubFeature#monitoring}
        :param mutation_enabled: Enables the ability to mutate resources using Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#mutation_enabled GoogleGkeHubFeature#mutation_enabled}
        :param policy_content: policy_content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policy_content GoogleGkeHubFeature#policy_content}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#referential_rules_enabled GoogleGkeHubFeature#referential_rules_enabled}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig(
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
    ) -> "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigOutputReference":
        return typing.cast("GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigOutputReference", jsii.get(self, "policyControllerHubConfig"))

    @builtins.property
    @jsii.member(jsii_name="policyControllerHubConfigInput")
    def policy_controller_hub_config_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig"], jsii.get(self, "policyControllerHubConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__47b6c718c032d3129d23257cb64e35692e2493552c17033f17854ebb61a4f1cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e595bdaece62a778a5bbe002f57843748ee471243fb73a14a3f5f7a4e4bcc88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig",
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
class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig:
    def __init__(
        self,
        *,
        install_spec: builtins.str,
        audit_interval_seconds: typing.Optional[jsii.Number] = None,
        constraint_violation_limit: typing.Optional[jsii.Number] = None,
        deployment_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_content: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent", typing.Dict[builtins.str, typing.Any]]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param install_spec: Configures the mode of the Policy Controller installation Possible values: ["INSTALL_SPEC_UNSPECIFIED", "INSTALL_SPEC_NOT_INSTALLED", "INSTALL_SPEC_ENABLED", "INSTALL_SPEC_SUSPENDED", "INSTALL_SPEC_DETACHED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#install_spec GoogleGkeHubFeature#install_spec}
        :param audit_interval_seconds: Interval for Policy Controller Audit scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#audit_interval_seconds GoogleGkeHubFeature#audit_interval_seconds}
        :param constraint_violation_limit: The maximum number of audit violations to be stored in a constraint. If not set, the internal default of 20 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#constraint_violation_limit GoogleGkeHubFeature#constraint_violation_limit}
        :param deployment_configs: deployment_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#deployment_configs GoogleGkeHubFeature#deployment_configs}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#exemptable_namespaces GoogleGkeHubFeature#exemptable_namespaces}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#log_denies_enabled GoogleGkeHubFeature#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#monitoring GoogleGkeHubFeature#monitoring}
        :param mutation_enabled: Enables the ability to mutate resources using Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#mutation_enabled GoogleGkeHubFeature#mutation_enabled}
        :param policy_content: policy_content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policy_content GoogleGkeHubFeature#policy_content}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#referential_rules_enabled GoogleGkeHubFeature#referential_rules_enabled}
        '''
        if isinstance(monitoring, dict):
            monitoring = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring(**monitoring)
        if isinstance(policy_content, dict):
            policy_content = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent(**policy_content)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c70079cb7cc23fac347a547aac0fcc158bb7155787f4e19e8eee2ab80fe252)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#install_spec GoogleGkeHubFeature#install_spec}
        '''
        result = self._values.get("install_spec")
        assert result is not None, "Required property 'install_spec' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audit_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''Interval for Policy Controller Audit scans (in seconds). When set to 0, this disables audit functionality altogether.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#audit_interval_seconds GoogleGkeHubFeature#audit_interval_seconds}
        '''
        result = self._values.get("audit_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def constraint_violation_limit(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of audit violations to be stored in a constraint.

        If not set, the internal default of 20 will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#constraint_violation_limit GoogleGkeHubFeature#constraint_violation_limit}
        '''
        result = self._values.get("constraint_violation_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def deployment_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs"]]]:
        '''deployment_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#deployment_configs GoogleGkeHubFeature#deployment_configs}
        '''
        result = self._values.get("deployment_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs"]]], result)

    @builtins.property
    def exemptable_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of namespaces that are excluded from Policy Controller checks.

        Namespaces do not need to currently exist on the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#exemptable_namespaces GoogleGkeHubFeature#exemptable_namespaces}
        '''
        result = self._values.get("exemptable_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def log_denies_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Logs all denies and dry run failures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#log_denies_enabled GoogleGkeHubFeature#log_denies_enabled}
        '''
        result = self._values.get("log_denies_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monitoring(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring"]:
        '''monitoring block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#monitoring GoogleGkeHubFeature#monitoring}
        '''
        result = self._values.get("monitoring")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring"], result)

    @builtins.property
    def mutation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the ability to mutate resources using Policy Controller.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#mutation_enabled GoogleGkeHubFeature#mutation_enabled}
        '''
        result = self._values.get("mutation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def policy_content(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent"]:
        '''policy_content block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#policy_content GoogleGkeHubFeature#policy_content}
        '''
        result = self._values.get("policy_content")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent"], result)

    @builtins.property
    def referential_rules_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#referential_rules_enabled GoogleGkeHubFeature#referential_rules_enabled}
        '''
        result = self._values.get("referential_rules_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "component": "component",
        "container_resources": "containerResources",
        "pod_affinity": "podAffinity",
        "pod_toleration": "podToleration",
        "replica_count": "replicaCount",
    },
)
class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs:
    def __init__(
        self,
        *,
        component: builtins.str,
        container_resources: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources", typing.Dict[builtins.str, typing.Any]]] = None,
        pod_affinity: typing.Optional[builtins.str] = None,
        pod_toleration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param component: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#component GoogleGkeHubFeature#component}.
        :param container_resources: container_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#container_resources GoogleGkeHubFeature#container_resources}
        :param pod_affinity: Pod affinity configuration. Possible values: ["AFFINITY_UNSPECIFIED", "NO_AFFINITY", "ANTI_AFFINITY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#pod_affinity GoogleGkeHubFeature#pod_affinity}
        :param pod_toleration: pod_toleration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#pod_toleration GoogleGkeHubFeature#pod_toleration}
        :param replica_count: Pod replica count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#replica_count GoogleGkeHubFeature#replica_count}
        '''
        if isinstance(container_resources, dict):
            container_resources = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources(**container_resources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3308441b7ae9f33d05065ee589a0779ff2a267a32511c584f7e023683ad70a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#component GoogleGkeHubFeature#component}.'''
        result = self._values.get("component")
        assert result is not None, "Required property 'component' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_resources(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources"]:
        '''container_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#container_resources GoogleGkeHubFeature#container_resources}
        '''
        result = self._values.get("container_resources")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources"], result)

    @builtins.property
    def pod_affinity(self) -> typing.Optional[builtins.str]:
        '''Pod affinity configuration. Possible values: ["AFFINITY_UNSPECIFIED", "NO_AFFINITY", "ANTI_AFFINITY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#pod_affinity GoogleGkeHubFeature#pod_affinity}
        '''
        result = self._values.get("pod_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_toleration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration"]]]:
        '''pod_toleration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#pod_toleration GoogleGkeHubFeature#pod_toleration}
        '''
        result = self._values.get("pod_toleration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration"]]], result)

    @builtins.property
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''Pod replica count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#replica_count GoogleGkeHubFeature#replica_count}
        '''
        result = self._values.get("replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources",
    jsii_struct_bases=[],
    name_mapping={"limits": "limits", "requests": "requests"},
)
class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources:
    def __init__(
        self,
        *,
        limits: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        requests: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#limits GoogleGkeHubFeature#limits}
        :param requests: requests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#requests GoogleGkeHubFeature#requests}
        '''
        if isinstance(limits, dict):
            limits = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits(**limits)
        if isinstance(requests, dict):
            requests = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests(**requests)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7113a8fb31aa110b2e71d6f7dc9620d99465a71fee0746a7c924e72ac0dcb555)
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
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits"]:
        '''limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#limits GoogleGkeHubFeature#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits"], result)

    @builtins.property
    def requests(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"]:
        '''requests block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#requests GoogleGkeHubFeature#requests}
        '''
        result = self._values.get("requests")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory"},
)
class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#cpu GoogleGkeHubFeature#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#memory GoogleGkeHubFeature#memory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b32a2a1ece23dc0bb4330b29a00d47f5d6a59f8888472fe8638ddf66adadd9b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#cpu GoogleGkeHubFeature#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Memory requirement expressed in Kubernetes resource units.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#memory GoogleGkeHubFeature#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dee99b498071208d822e8e8e9459b8b38329a953f338b54e8ada6c6edd1285d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e37db0a0680e8898e6c1bb71c893bab82b155f337e363d534a307c95bfedbaf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a69751878a72cf61595a5c99bad3fd3a5031a1c083697affc0a97f942e89b393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a06870231fa0296828dafb8314662bfb61f0bbdcf13a9692aa4c2233bbabcdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57313e86a346efbc2429ea2d4d83cfd8fb74ee9b16dc8733ee7d05e112c1ee80)
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
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#cpu GoogleGkeHubFeature#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#memory GoogleGkeHubFeature#memory}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits(
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
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#cpu GoogleGkeHubFeature#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#memory GoogleGkeHubFeature#memory}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests(
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
    ) -> GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference:
        return typing.cast(GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference, jsii.get(self, "limits"))

    @builtins.property
    @jsii.member(jsii_name="requests")
    def requests(
        self,
    ) -> "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference":
        return typing.cast("GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference", jsii.get(self, "requests"))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="requestsInput")
    def requests_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"], jsii.get(self, "requestsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef027deb50b1bf00eda8e23f899ed7056a741154be66e9a37bad28cb4694a33f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory"},
)
class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#cpu GoogleGkeHubFeature#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#memory GoogleGkeHubFeature#memory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__250e6b65f03205e0275244783889a71170da85ce23f180b0455577eda55a0052)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#cpu GoogleGkeHubFeature#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Memory requirement expressed in Kubernetes resource units.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#memory GoogleGkeHubFeature#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__825151c0de4e61c8a501e9fdc85ba8de4721ec413e9c2e0c0520ef47c0cb08d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db5adc92004c65fb553a89173b76c1eb9cc93860057098b73b8fdf64a05a099a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281059f67f6f47ce11e072b7c373418427051620692d2ceebaaff8040bc65c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93169b7b782e724083661c774bb7a650f813e359ce45e9d94e35cc49b48f29cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4fd6cfdc0c4a95d4213a5a53db890ed0af0eb41d878d1bd385c90144752ae70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24b3bfba2612b2cdce8a83169fe44e2331ca145e224d7c3cd718da649a1913a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b668a5d8e5e63458ec8ff62c85950312fa13b60fe78bf0a03aa4b03acb43c3bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dd871d736fc0cb512cbc5ef2ddc338aabf871431afc8a2451f425d9d5a107db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47281aa661e2ab89f93d70b67b6fda12789b97d9ed4639b8b6fad10a4cca6d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c23ac9fe172081e158f6808b89867a22f1a845ef16d7181154fccfa2250546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa56914804517cbf648ab41b4b520801bffcd99ca197fffa40041a0085fff435)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putContainerResources")
    def put_container_resources(
        self,
        *,
        limits: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits, typing.Dict[builtins.str, typing.Any]]] = None,
        requests: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#limits GoogleGkeHubFeature#limits}
        :param requests: requests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#requests GoogleGkeHubFeature#requests}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources(
            limits=limits, requests=requests
        )

        return typing.cast(None, jsii.invoke(self, "putContainerResources", [value]))

    @jsii.member(jsii_name="putPodToleration")
    def put_pod_toleration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__166f2233f7c33885268b5fd2b4244ef7aa2f57883420675b0039b7b3543336d0)
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
    ) -> GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference:
        return typing.cast(GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference, jsii.get(self, "containerResources"))

    @builtins.property
    @jsii.member(jsii_name="podToleration")
    def pod_toleration(
        self,
    ) -> "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationList":
        return typing.cast("GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationList", jsii.get(self, "podToleration"))

    @builtins.property
    @jsii.member(jsii_name="componentInput")
    def component_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "componentInput"))

    @builtins.property
    @jsii.member(jsii_name="containerResourcesInput")
    def container_resources_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources], jsii.get(self, "containerResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="podAffinityInput")
    def pod_affinity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="podTolerationInput")
    def pod_toleration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration"]]], jsii.get(self, "podTolerationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c8f82a6fc04c0ebc0d203c283ac7bb070877f7082f857a020c28e3ab13a031ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "component", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podAffinity")
    def pod_affinity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podAffinity"))

    @pod_affinity.setter
    def pod_affinity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0eccf1bb2a2d44c39959b51522425aef9f8ff41f1436b1c89d8f24978a2c241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaCount")
    def replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCount"))

    @replica_count.setter
    def replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d29ef850a3b555ebb0c2b73ce89509ea8f34e14ec66a439ae32c3b25e96c31f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff10dadf25a0fafb360626a6ab15aa32e7766d9beadee48edad11c043a94b4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration",
    jsii_struct_bases=[],
    name_mapping={
        "effect": "effect",
        "key": "key",
        "operator": "operator",
        "value": "value",
    },
)
class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration:
    def __init__(
        self,
        *,
        effect: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Matches a taint effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#effect GoogleGkeHubFeature#effect}
        :param key: Matches a taint key (not necessarily unique). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#key GoogleGkeHubFeature#key}
        :param operator: Matches a taint operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#operator GoogleGkeHubFeature#operator}
        :param value: Matches a taint value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#value GoogleGkeHubFeature#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d41872650ca72d8278cedf55c31f75057db42a95a85095c69ced1c1040908e4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#effect GoogleGkeHubFeature#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Matches a taint key (not necessarily unique).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#key GoogleGkeHubFeature#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Matches a taint operator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#operator GoogleGkeHubFeature#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Matches a taint value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#value GoogleGkeHubFeature#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e8bd04083fe3a6a9ba22573a6fb78243df3c31739631e006d94e5cbcdcb0fd7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2e887afce1759186b20c80e09c97691687a42d19159789177c40d0b6027e03)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9c3b814f4301d256267ed62351724e042002276f435c4c4cb4aee718580137)
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
            type_hints = typing.get_type_hints(_typecheckingstub__908915d086b5cf6f37116e2f6ab9e300c8a62a9876710a085eca280b50bd2afa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d78d5fbea907cca0861a77141cc6e9ac631f37507ffdbc2d7580111c95f3ca24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016ae138256acc1940d2b711ea9e12bdba0a79ab705881b46e2b5df898e10655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06280b962343fba1f33b1522b84389eeca7bd9acad5493897e810dcc11712ed3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c833a02899992413b46e1b5ad2655667299bb9a515487f906158c77962c4090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eed52423f07b56fcfed853657f9936c5e7125e096b68c3c8f39b2acd9fa5e502)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ccb72a987a81676b9b6be49ab0d63c35c303215d864901fec6118185f3e37fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e593c6ac5ca9bb575d0779461df3b7eb8a6ac57e99b2110561275bc58ac589b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22c6b0b4e2b13d16bb1eaa049c5fff44dce41830022fcd11e3b8020996e486d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring",
    jsii_struct_bases=[],
    name_mapping={"backends": "backends"},
)
class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring:
    def __init__(
        self,
        *,
        backends: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param backends: Specifies the list of backends Policy Controller will export to. An empty list would effectively disable metrics export. Possible values: ["MONITORING_BACKEND_UNSPECIFIED", "PROMETHEUS", "CLOUD_MONITORING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#backends GoogleGkeHubFeature#backends}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca84ef0c3b4cc3d9460d1c5502b3deb118eff6cea840ead9c5405cf9a903acf7)
            check_type(argname="argument backends", value=backends, expected_type=type_hints["backends"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backends is not None:
            self._values["backends"] = backends

    @builtins.property
    def backends(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of backends Policy Controller will export to.

        An empty list would effectively disable metrics export. Possible values: ["MONITORING_BACKEND_UNSPECIFIED", "PROMETHEUS", "CLOUD_MONITORING"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#backends GoogleGkeHubFeature#backends}
        '''
        result = self._values.get("backends")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5ad8871c722837f4eb13a23dfbf3b1c4cdbc08944c44f3010d06d15a3258dcf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f4053c542f2c4e1f3be55be53e49ff556da86d321fe5864517684e76b4420a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backends", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e0b86e2353c73c6e04b55287176bca17c9d398978ad44630a770d094d44f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__805354dc24c7f02a08debb8e58ec6577760fdb4419189045c99eae98ce067aad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeploymentConfigs")
    def put_deployment_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7735f483462dff19d477ca15a2386189da6a2fd94a9c3c9f3391fd523563b6c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeploymentConfigs", [value]))

    @jsii.member(jsii_name="putMonitoring")
    def put_monitoring(
        self,
        *,
        backends: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param backends: Specifies the list of backends Policy Controller will export to. An empty list would effectively disable metrics export. Possible values: ["MONITORING_BACKEND_UNSPECIFIED", "PROMETHEUS", "CLOUD_MONITORING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#backends GoogleGkeHubFeature#backends}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring(
            backends=backends
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoring", [value]))

    @jsii.member(jsii_name="putPolicyContent")
    def put_policy_content(
        self,
        *,
        bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        template_library: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bundles: bundles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#bundles GoogleGkeHubFeature#bundles}
        :param template_library: template_library block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#template_library GoogleGkeHubFeature#template_library}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent(
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
    ) -> GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList:
        return typing.cast(GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList, jsii.get(self, "deploymentConfigs"))

    @builtins.property
    @jsii.member(jsii_name="monitoring")
    def monitoring(
        self,
    ) -> GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference:
        return typing.cast(GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference, jsii.get(self, "monitoring"))

    @builtins.property
    @jsii.member(jsii_name="policyContent")
    def policy_content(
        self,
    ) -> "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference":
        return typing.cast("GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference", jsii.get(self, "policyContent"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]], jsii.get(self, "deploymentConfigsInput"))

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
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring], jsii.get(self, "monitoringInput"))

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
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent"], jsii.get(self, "policyContentInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__33ddced2711338d8353fed2163410156380a696c1d2e135dc9c5c164ae32dc2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auditIntervalSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="constraintViolationLimit")
    def constraint_violation_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "constraintViolationLimit"))

    @constraint_violation_limit.setter
    def constraint_violation_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d629c890ce240fb77df97fa30b62708bc324951f16aef49631e6d6ad33a2f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constraintViolationLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exemptableNamespaces")
    def exemptable_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exemptableNamespaces"))

    @exemptable_namespaces.setter
    def exemptable_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6487028e8cdf21c229f371bc19d3afd87d4a2d3978f228a7b5c786779d2e664a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exemptableNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="installSpec")
    def install_spec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "installSpec"))

    @install_spec.setter
    def install_spec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d203f944f7c25b322fbea400eb151afaa9da47ca66c35ed53eece492ad23d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__959f4a1f06ef8cd9532778684f0dbf187c92d4a728ec314d777d13a948588a69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__758bafa3cee9b182a8bdbb3554bedb7aa7eff5960ec1124d2a895232f59aed88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9585a2a5df940b6718424eac10eb266da730139d0d0c852f9110f1c821305bfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referentialRulesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b38faff90502dce2ac53da1913e54e465904991fe5075ca41dc2c74e6318d21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent",
    jsii_struct_bases=[],
    name_mapping={"bundles": "bundles", "template_library": "templateLibrary"},
)
class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent:
    def __init__(
        self,
        *,
        bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        template_library: typing.Optional[typing.Union["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bundles: bundles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#bundles GoogleGkeHubFeature#bundles}
        :param template_library: template_library block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#template_library GoogleGkeHubFeature#template_library}
        '''
        if isinstance(template_library, dict):
            template_library = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary(**template_library)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2eda8144401dd8dad9090206d3e3e71142fab1386e43a934be0374021e6458b)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles"]]]:
        '''bundles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#bundles GoogleGkeHubFeature#bundles}
        '''
        result = self._values.get("bundles")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles"]]], result)

    @builtins.property
    def template_library(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"]:
        '''template_library block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#template_library GoogleGkeHubFeature#template_library}
        '''
        result = self._values.get("template_library")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles",
    jsii_struct_bases=[],
    name_mapping={"bundle": "bundle", "exempted_namespaces": "exemptedNamespaces"},
)
class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles:
    def __init__(
        self,
        *,
        bundle: builtins.str,
        exempted_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bundle: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#bundle GoogleGkeHubFeature#bundle}.
        :param exempted_namespaces: The set of namespaces to be exempted from the bundle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#exempted_namespaces GoogleGkeHubFeature#exempted_namespaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e846ad5f5cd6613912f8839885784518d783f710dcca2bd33819a2b6b5b904b)
            check_type(argname="argument bundle", value=bundle, expected_type=type_hints["bundle"])
            check_type(argname="argument exempted_namespaces", value=exempted_namespaces, expected_type=type_hints["exempted_namespaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bundle": bundle,
        }
        if exempted_namespaces is not None:
            self._values["exempted_namespaces"] = exempted_namespaces

    @builtins.property
    def bundle(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#bundle GoogleGkeHubFeature#bundle}.'''
        result = self._values.get("bundle")
        assert result is not None, "Required property 'bundle' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exempted_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of namespaces to be exempted from the bundle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#exempted_namespaces GoogleGkeHubFeature#exempted_namespaces}
        '''
        result = self._values.get("exempted_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5d53cdee1c35b711a2107b7c9c4d94943a69763cfe9e2fa32c01ca697ad30a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa70578683c046154c04f729097a7488b6e0a1757ef3079f337c57babcb559c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee05e8d7fba69a833bf10e08e60cde8f9f84e5d78727eaf08008b72ccfc3197)
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
            type_hints = typing.get_type_hints(_typecheckingstub__029fe1da5e8036e64095c7b56a3a7e3ad84ad5b62116869d186002dcae9c39d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__724b3986972f1f81b4e8a54e550ecc8974cd40042e66016161e1ac193f122d71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9b2b2e1eb0ccaf7dcbb6da583af7a7f015ae2d4181875d2869c4cd63bf51c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__171e1c93b1cfaa1064bae24fbbd3a1e05bd5902d44f3d07089d9bb86a121aac4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71099e7bbd8c4dd9568e36d8fbd0108c9365aee5e9c5d05599108078da8d637c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exemptedNamespaces")
    def exempted_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exemptedNamespaces"))

    @exempted_namespaces.setter
    def exempted_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4712cc00d8ef1bf34e7810cff3361bd145379d9d359b7fdbec47dde7f46a21c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exemptedNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a92dff9bfb1f4efc0f258b1a9313f32936b937a905c9b149be01efacba6372b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26e07aadd97d580a8bc6c5c9b3db01d7dee4b0bf6f10d8178513722f2c505737)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBundles")
    def put_bundles(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a03f752a6d2291fdc6949c016c1a21bf292a59837dadb9273ff00d9ff65b06c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBundles", [value]))

    @jsii.member(jsii_name="putTemplateLibrary")
    def put_template_library(
        self,
        *,
        installation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param installation: Configures the manner in which the template library is installed on the cluster. Possible values: ["INSTALLATION_UNSPECIFIED", "NOT_INSTALLED", "ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#installation GoogleGkeHubFeature#installation}
        '''
        value = GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary(
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
    ) -> GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList:
        return typing.cast(GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList, jsii.get(self, "bundles"))

    @builtins.property
    @jsii.member(jsii_name="templateLibrary")
    def template_library(
        self,
    ) -> "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference":
        return typing.cast("GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference", jsii.get(self, "templateLibrary"))

    @builtins.property
    @jsii.member(jsii_name="bundlesInput")
    def bundles_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]], jsii.get(self, "bundlesInput"))

    @builtins.property
    @jsii.member(jsii_name="templateLibraryInput")
    def template_library_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"], jsii.get(self, "templateLibraryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa288494e9d223539a89846ecbcac08f7316837a76a8280e2e3204ec21f8a4e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary",
    jsii_struct_bases=[],
    name_mapping={"installation": "installation"},
)
class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary:
    def __init__(self, *, installation: typing.Optional[builtins.str] = None) -> None:
        '''
        :param installation: Configures the manner in which the template library is installed on the cluster. Possible values: ["INSTALLATION_UNSPECIFIED", "NOT_INSTALLED", "ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#installation GoogleGkeHubFeature#installation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d16fb271116835a3c7e4bb9c18be3fb9883eb970279a7585d985501b263863)
            check_type(argname="argument installation", value=installation, expected_type=type_hints["installation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if installation is not None:
            self._values["installation"] = installation

    @builtins.property
    def installation(self) -> typing.Optional[builtins.str]:
        '''Configures the manner in which the template library is installed on the cluster. Possible values: ["INSTALLATION_UNSPECIFIED", "NOT_INSTALLED", "ALL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#installation GoogleGkeHubFeature#installation}
        '''
        result = self._values.get("installation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__645343a72262466d7c0299065e8ba7aeff688ffbbce07799df05ede276809ac8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__134bb3cda57603737edf80ed4739a8e495605afcbd753f61724b1ffce2ac562c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "installation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c324bd63a87f66a0e3b6db4777b5333cb5e0fb8c95833195b59351e37370190e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureResourceState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeHubFeatureResourceState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureResourceState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureResourceStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureResourceStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df1d2d88370d1223823343c2c031752606e794b9abd460e2f3c9a2851ac5125b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeHubFeatureResourceStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d904627009a4f880b9dd170f1b3844d0598e8bf87dbbf9d2c0e7514ae1c5595b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFeatureResourceStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18c3d40393e00090df5a89c64b245879019da5457e7b69a6194aac4b2d16d44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3214317708b2332e2ef93286e0c78e75a8dbeacb70736549fc7c1feeac317d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52a8e710f324d5cc19d9f303b395542f662973af9542a31e607166a6345e8a1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureResourceStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureResourceStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9823f175e6d5a0c6a5029e73c67c721b74f8809454b294a9fb700e1fd82fe39)
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
    def internal_value(self) -> typing.Optional[GoogleGkeHubFeatureResourceState]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureResourceState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureResourceState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8bcaae70ece5f4f953795bd10825e17f0f0f406312be4d914e8be9148f6aa9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpec",
    jsii_struct_bases=[],
    name_mapping={
        "clusterupgrade": "clusterupgrade",
        "fleetobservability": "fleetobservability",
        "multiclusteringress": "multiclusteringress",
        "rbacrolebindingactuation": "rbacrolebindingactuation",
    },
)
class GoogleGkeHubFeatureSpec:
    def __init__(
        self,
        *,
        clusterupgrade: typing.Optional[typing.Union["GoogleGkeHubFeatureSpecClusterupgrade", typing.Dict[builtins.str, typing.Any]]] = None,
        fleetobservability: typing.Optional[typing.Union["GoogleGkeHubFeatureSpecFleetobservability", typing.Dict[builtins.str, typing.Any]]] = None,
        multiclusteringress: typing.Optional[typing.Union["GoogleGkeHubFeatureSpecMulticlusteringress", typing.Dict[builtins.str, typing.Any]]] = None,
        rbacrolebindingactuation: typing.Optional[typing.Union["GoogleGkeHubFeatureSpecRbacrolebindingactuation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param clusterupgrade: clusterupgrade block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#clusterupgrade GoogleGkeHubFeature#clusterupgrade}
        :param fleetobservability: fleetobservability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#fleetobservability GoogleGkeHubFeature#fleetobservability}
        :param multiclusteringress: multiclusteringress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#multiclusteringress GoogleGkeHubFeature#multiclusteringress}
        :param rbacrolebindingactuation: rbacrolebindingactuation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#rbacrolebindingactuation GoogleGkeHubFeature#rbacrolebindingactuation}
        '''
        if isinstance(clusterupgrade, dict):
            clusterupgrade = GoogleGkeHubFeatureSpecClusterupgrade(**clusterupgrade)
        if isinstance(fleetobservability, dict):
            fleetobservability = GoogleGkeHubFeatureSpecFleetobservability(**fleetobservability)
        if isinstance(multiclusteringress, dict):
            multiclusteringress = GoogleGkeHubFeatureSpecMulticlusteringress(**multiclusteringress)
        if isinstance(rbacrolebindingactuation, dict):
            rbacrolebindingactuation = GoogleGkeHubFeatureSpecRbacrolebindingactuation(**rbacrolebindingactuation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d061d7c79bb94b3cd8b8e284adcf8b1dc6311abcb09f92c38bfaad2f62cd10)
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
    def clusterupgrade(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureSpecClusterupgrade"]:
        '''clusterupgrade block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#clusterupgrade GoogleGkeHubFeature#clusterupgrade}
        '''
        result = self._values.get("clusterupgrade")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpecClusterupgrade"], result)

    @builtins.property
    def fleetobservability(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureSpecFleetobservability"]:
        '''fleetobservability block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#fleetobservability GoogleGkeHubFeature#fleetobservability}
        '''
        result = self._values.get("fleetobservability")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpecFleetobservability"], result)

    @builtins.property
    def multiclusteringress(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureSpecMulticlusteringress"]:
        '''multiclusteringress block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#multiclusteringress GoogleGkeHubFeature#multiclusteringress}
        '''
        result = self._values.get("multiclusteringress")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpecMulticlusteringress"], result)

    @builtins.property
    def rbacrolebindingactuation(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureSpecRbacrolebindingactuation"]:
        '''rbacrolebindingactuation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#rbacrolebindingactuation GoogleGkeHubFeature#rbacrolebindingactuation}
        '''
        result = self._values.get("rbacrolebindingactuation")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpecRbacrolebindingactuation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecClusterupgrade",
    jsii_struct_bases=[],
    name_mapping={
        "upstream_fleets": "upstreamFleets",
        "gke_upgrade_overrides": "gkeUpgradeOverrides",
        "post_conditions": "postConditions",
    },
)
class GoogleGkeHubFeatureSpecClusterupgrade:
    def __init__(
        self,
        *,
        upstream_fleets: typing.Sequence[builtins.str],
        gke_upgrade_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_conditions: typing.Optional[typing.Union["GoogleGkeHubFeatureSpecClusterupgradePostConditions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param upstream_fleets: Specified if other fleet should be considered as a source of upgrades. Currently, at most one upstream fleet is allowed. The fleet name should be either fleet project number or id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#upstream_fleets GoogleGkeHubFeature#upstream_fleets}
        :param gke_upgrade_overrides: gke_upgrade_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#gke_upgrade_overrides GoogleGkeHubFeature#gke_upgrade_overrides}
        :param post_conditions: post_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#post_conditions GoogleGkeHubFeature#post_conditions}
        '''
        if isinstance(post_conditions, dict):
            post_conditions = GoogleGkeHubFeatureSpecClusterupgradePostConditions(**post_conditions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38a5823aec2c7ceb7031d11377e5527c67296f4d851450bf1328a1153345db3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#upstream_fleets GoogleGkeHubFeature#upstream_fleets}
        '''
        result = self._values.get("upstream_fleets")
        assert result is not None, "Required property 'upstream_fleets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def gke_upgrade_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides"]]]:
        '''gke_upgrade_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#gke_upgrade_overrides GoogleGkeHubFeature#gke_upgrade_overrides}
        '''
        result = self._values.get("gke_upgrade_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides"]]], result)

    @builtins.property
    def post_conditions(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureSpecClusterupgradePostConditions"]:
        '''post_conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#post_conditions GoogleGkeHubFeature#post_conditions}
        '''
        result = self._values.get("post_conditions")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpecClusterupgradePostConditions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureSpecClusterupgrade(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides",
    jsii_struct_bases=[],
    name_mapping={"post_conditions": "postConditions", "upgrade": "upgrade"},
)
class GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides:
    def __init__(
        self,
        *,
        post_conditions: typing.Union["GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions", typing.Dict[builtins.str, typing.Any]],
        upgrade: typing.Union["GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param post_conditions: post_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#post_conditions GoogleGkeHubFeature#post_conditions}
        :param upgrade: upgrade block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#upgrade GoogleGkeHubFeature#upgrade}
        '''
        if isinstance(post_conditions, dict):
            post_conditions = GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions(**post_conditions)
        if isinstance(upgrade, dict):
            upgrade = GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade(**upgrade)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b3f77e45b75d3faa47d92594ff21027dc30467c61d636329896dc2922da2f3)
            check_type(argname="argument post_conditions", value=post_conditions, expected_type=type_hints["post_conditions"])
            check_type(argname="argument upgrade", value=upgrade, expected_type=type_hints["upgrade"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "post_conditions": post_conditions,
            "upgrade": upgrade,
        }

    @builtins.property
    def post_conditions(
        self,
    ) -> "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions":
        '''post_conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#post_conditions GoogleGkeHubFeature#post_conditions}
        '''
        result = self._values.get("post_conditions")
        assert result is not None, "Required property 'post_conditions' is missing"
        return typing.cast("GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions", result)

    @builtins.property
    def upgrade(
        self,
    ) -> "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade":
        '''upgrade block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#upgrade GoogleGkeHubFeature#upgrade}
        '''
        result = self._values.get("upgrade")
        assert result is not None, "Required property 'upgrade' is missing"
        return typing.cast("GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af7bf03287de35ab1046413cd74dbd1871cc53d711c35e98a4f42de31c56b4ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__533bd44b881a087b4567f64728bff421431ff47959f1ac956661a41e36f1c235)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b6822a846dd4303944127c6aa02527640dcf62d33fc0f3c7774484eb3c2074)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f62fcc4f7080f047891885b5670a964a53913cb48194692ee3275cb9769774aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a19cce341136dd46dc5a1a93f53fa1ede0e40301dc12439f1069a65a9941a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f086720447c5ab16bb9dc8e497fcaf8f6e7d30a5b693a2a527f8f3000e621a9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0458b19508303303020514288304054e2e40b89378d07fd80ae52b830fde8f16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPostConditions")
    def put_post_conditions(self, *, soaking: builtins.str) -> None:
        '''
        :param soaking: Amount of time to "soak" after a rollout has been finished before marking it COMPLETE. Cannot exceed 30 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#soaking GoogleGkeHubFeature#soaking}
        '''
        value = GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions(
            soaking=soaking
        )

        return typing.cast(None, jsii.invoke(self, "putPostConditions", [value]))

    @jsii.member(jsii_name="putUpgrade")
    def put_upgrade(self, *, name: builtins.str, version: builtins.str) -> None:
        '''
        :param name: Name of the upgrade, e.g., "k8s_control_plane". It should be a valid upgrade name. It must not exceet 99 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#name GoogleGkeHubFeature#name}
        :param version: Version of the upgrade, e.g., "1.22.1-gke.100". It should be a valid version. It must not exceet 99 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#version GoogleGkeHubFeature#version}
        '''
        value = GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade(
            name=name, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putUpgrade", [value]))

    @builtins.property
    @jsii.member(jsii_name="postConditions")
    def post_conditions(
        self,
    ) -> "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditionsOutputReference":
        return typing.cast("GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditionsOutputReference", jsii.get(self, "postConditions"))

    @builtins.property
    @jsii.member(jsii_name="upgrade")
    def upgrade(
        self,
    ) -> "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgradeOutputReference":
        return typing.cast("GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgradeOutputReference", jsii.get(self, "upgrade"))

    @builtins.property
    @jsii.member(jsii_name="postConditionsInput")
    def post_conditions_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions"], jsii.get(self, "postConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeInput")
    def upgrade_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade"], jsii.get(self, "upgradeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd165f23c755660ba0a797be995bfcc7155451c7c0c3b3e2565a3591208bd2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions",
    jsii_struct_bases=[],
    name_mapping={"soaking": "soaking"},
)
class GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions:
    def __init__(self, *, soaking: builtins.str) -> None:
        '''
        :param soaking: Amount of time to "soak" after a rollout has been finished before marking it COMPLETE. Cannot exceed 30 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#soaking GoogleGkeHubFeature#soaking}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d9127c751687f67ed8cc633366440ee724b7da83876fd6135cf309d9923cbc)
            check_type(argname="argument soaking", value=soaking, expected_type=type_hints["soaking"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "soaking": soaking,
        }

    @builtins.property
    def soaking(self) -> builtins.str:
        '''Amount of time to "soak" after a rollout has been finished before marking it COMPLETE. Cannot exceed 30 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#soaking GoogleGkeHubFeature#soaking}
        '''
        result = self._values.get("soaking")
        assert result is not None, "Required property 'soaking' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46389715736951be3b80b6f68de765f6eb89777ea8a08c0d4d0ae922d5c64bfb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__380f515575148f98a5927553f68d800bb62cfb7c105310e4c347283ba4921933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "soaking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f109d4de656564984dfcba05220051815d248feb1297c16eb506c3ba71086a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "version": "version"},
)
class GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade:
    def __init__(self, *, name: builtins.str, version: builtins.str) -> None:
        '''
        :param name: Name of the upgrade, e.g., "k8s_control_plane". It should be a valid upgrade name. It must not exceet 99 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#name GoogleGkeHubFeature#name}
        :param version: Version of the upgrade, e.g., "1.22.1-gke.100". It should be a valid version. It must not exceet 99 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#version GoogleGkeHubFeature#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22c2cc45d44393705ef271d2bd2540ff977bb63251bcdecc5dff84d31a6284a8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "version": version,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the upgrade, e.g., "k8s_control_plane". It should be a valid upgrade name. It must not exceet 99 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#name GoogleGkeHubFeature#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Version of the upgrade, e.g., "1.22.1-gke.100". It should be a valid version. It must not exceet 99 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#version GoogleGkeHubFeature#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgradeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgradeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab93205b017f0140600d625ca3b87fb9226c5073b43eddc70a301123d240d5ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d273ecf8e55039e9f61edb0bca5d4b005c9ef39c8586d86dfd4dc28f0d294032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c385e70de7d0eee48d3a395302c03790bb4d6cd438ff520671b665097687b99d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c29b74a02791faab0044d58461babe9fa6ab336c2bb50b571c02f3d6cc7eb85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureSpecClusterupgradeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecClusterupgradeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01eaebcd1d22d9f66ff9e742b829ff1c49aad63219e88205db077c0290c1ccbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGkeUpgradeOverrides")
    def put_gke_upgrade_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b875caba6c5bc6e68a7473dd25b4cf9d51dfa8fb81f7dd2b9e3c1e8c809b7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGkeUpgradeOverrides", [value]))

    @jsii.member(jsii_name="putPostConditions")
    def put_post_conditions(self, *, soaking: builtins.str) -> None:
        '''
        :param soaking: Amount of time to "soak" after a rollout has been finished before marking it COMPLETE. Cannot exceed 30 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#soaking GoogleGkeHubFeature#soaking}
        '''
        value = GoogleGkeHubFeatureSpecClusterupgradePostConditions(soaking=soaking)

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
    ) -> GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesList:
        return typing.cast(GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesList, jsii.get(self, "gkeUpgradeOverrides"))

    @builtins.property
    @jsii.member(jsii_name="postConditions")
    def post_conditions(
        self,
    ) -> "GoogleGkeHubFeatureSpecClusterupgradePostConditionsOutputReference":
        return typing.cast("GoogleGkeHubFeatureSpecClusterupgradePostConditionsOutputReference", jsii.get(self, "postConditions"))

    @builtins.property
    @jsii.member(jsii_name="gkeUpgradeOverridesInput")
    def gke_upgrade_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]], jsii.get(self, "gkeUpgradeOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="postConditionsInput")
    def post_conditions_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureSpecClusterupgradePostConditions"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpecClusterupgradePostConditions"], jsii.get(self, "postConditionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6445d9edcaf8429642eb4a4ce9ee167dad08a374a2177e5ce8fedb4879038619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upstreamFleets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeHubFeatureSpecClusterupgrade]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecClusterupgrade], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureSpecClusterupgrade],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b697b1d3e7db5f6d93ad0fcff166309003a2b2ad025aaddf195698e4342934d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecClusterupgradePostConditions",
    jsii_struct_bases=[],
    name_mapping={"soaking": "soaking"},
)
class GoogleGkeHubFeatureSpecClusterupgradePostConditions:
    def __init__(self, *, soaking: builtins.str) -> None:
        '''
        :param soaking: Amount of time to "soak" after a rollout has been finished before marking it COMPLETE. Cannot exceed 30 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#soaking GoogleGkeHubFeature#soaking}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507ea075dd732441f2baf98e609ff2e3ba8be484a70aa9027764f951a280a5af)
            check_type(argname="argument soaking", value=soaking, expected_type=type_hints["soaking"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "soaking": soaking,
        }

    @builtins.property
    def soaking(self) -> builtins.str:
        '''Amount of time to "soak" after a rollout has been finished before marking it COMPLETE. Cannot exceed 30 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#soaking GoogleGkeHubFeature#soaking}
        '''
        result = self._values.get("soaking")
        assert result is not None, "Required property 'soaking' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureSpecClusterupgradePostConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureSpecClusterupgradePostConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecClusterupgradePostConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b38474516932ddb9d3036e299baf46eae85e6dd3d445b9c48911d389e56f0624)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4f3fe9e3c3a8b5b788ee1c87e7e2ee47691335ca4ded14d711cc3628e6cc8fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "soaking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecClusterupgradePostConditions]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecClusterupgradePostConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureSpecClusterupgradePostConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df0bb4a9840dae1902b5b6de51fe57c436813184d367d742b50b9a257eac046f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecFleetobservability",
    jsii_struct_bases=[],
    name_mapping={"logging_config": "loggingConfig"},
)
class GoogleGkeHubFeatureSpecFleetobservability:
    def __init__(
        self,
        *,
        logging_config: typing.Optional[typing.Union["GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#logging_config GoogleGkeHubFeature#logging_config}
        '''
        if isinstance(logging_config, dict):
            logging_config = GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig(**logging_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90cc420bb6c8200aca13bc9b30339e23450c89bc33b34c6826aca627336e1a64)
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if logging_config is not None:
            self._values["logging_config"] = logging_config

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#logging_config GoogleGkeHubFeature#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureSpecFleetobservability(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "default_config": "defaultConfig",
        "fleet_scope_logs_config": "fleetScopeLogsConfig",
    },
)
class GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig:
    def __init__(
        self,
        *,
        default_config: typing.Optional[typing.Union["GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        fleet_scope_logs_config: typing.Optional[typing.Union["GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_config: default_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#default_config GoogleGkeHubFeature#default_config}
        :param fleet_scope_logs_config: fleet_scope_logs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#fleet_scope_logs_config GoogleGkeHubFeature#fleet_scope_logs_config}
        '''
        if isinstance(default_config, dict):
            default_config = GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig(**default_config)
        if isinstance(fleet_scope_logs_config, dict):
            fleet_scope_logs_config = GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig(**fleet_scope_logs_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1092c7c58e734fccb996c1c549826a7626c61d45d2879559bab1695b801ece9)
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
    ) -> typing.Optional["GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig"]:
        '''default_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#default_config GoogleGkeHubFeature#default_config}
        '''
        result = self._values.get("default_config")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig"], result)

    @builtins.property
    def fleet_scope_logs_config(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig"]:
        '''fleet_scope_logs_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#fleet_scope_logs_config GoogleGkeHubFeature#fleet_scope_logs_config}
        '''
        result = self._values.get("fleet_scope_logs_config")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig:
    def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mode: Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#mode GoogleGkeHubFeature#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e84035f25007be86d9fb4adc1572616afc5de73220a19015e9cbc8a61099c53)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#mode GoogleGkeHubFeature#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5b41e0b11a974217ed1cb7e5adacdb225e4f8263326dbc7f8f4645897679172)
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
            type_hints = typing.get_type_hints(_typecheckingstub__987d88ea6015aef5360b5a3c509fdb4cbb81f27a7fde0b9d6fea5eaa068d8769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__114fc0a179098862bd259a125d98beb6371790d2c14fad6952e4325543601a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig:
    def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mode: Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#mode GoogleGkeHubFeature#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d30147e7e49005a62d94e1bc258059df84dc36121aad77dc99646be5a5b107)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#mode GoogleGkeHubFeature#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e0d043d61b3a56a836bd87a2349603ca00cb3559c0b8cef9364b2fd5e547230)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1e7195d440669a390a33b3a9a4a36016f632f9984b8fe41d95dc480195893a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d46d23518f45d4970ef346a33787f55c0e8cc6927089cc20008005dc788bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0809a1e8c2d153d6e28b37e26529c2aa772140653fe404e06998f7b8a194af8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDefaultConfig")
    def put_default_config(self, *, mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mode: Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#mode GoogleGkeHubFeature#mode}
        '''
        value = GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig(
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
        :param mode: Specified if fleet logging feature is enabled. Possible values: ["MODE_UNSPECIFIED", "COPY", "MOVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#mode GoogleGkeHubFeature#mode}
        '''
        value = GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig(
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
    ) -> GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference:
        return typing.cast(GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference, jsii.get(self, "defaultConfig"))

    @builtins.property
    @jsii.member(jsii_name="fleetScopeLogsConfig")
    def fleet_scope_logs_config(
        self,
    ) -> GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference:
        return typing.cast(GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference, jsii.get(self, "fleetScopeLogsConfig"))

    @builtins.property
    @jsii.member(jsii_name="defaultConfigInput")
    def default_config_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig], jsii.get(self, "defaultConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetScopeLogsConfigInput")
    def fleet_scope_logs_config_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig], jsii.get(self, "fleetScopeLogsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0e44599f76cdf54cc6278791c2dbfd3796928a40aafe923e6d24b764f81567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureSpecFleetobservabilityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecFleetobservabilityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29cf13dd41417b92383eb8f5ffd08984e4098a868225e3433f11a864bd62399a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        default_config: typing.Optional[typing.Union[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        fleet_scope_logs_config: typing.Optional[typing.Union[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_config: default_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#default_config GoogleGkeHubFeature#default_config}
        :param fleet_scope_logs_config: fleet_scope_logs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#fleet_scope_logs_config GoogleGkeHubFeature#fleet_scope_logs_config}
        '''
        value = GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig(
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
    ) -> GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference:
        return typing.cast(GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecFleetobservability]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecFleetobservability], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureSpecFleetobservability],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6ca4231f8a846df7e1a33b02b303f564eb4e148eec7a5442977f7e03461aa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecMulticlusteringress",
    jsii_struct_bases=[],
    name_mapping={"config_membership": "configMembership"},
)
class GoogleGkeHubFeatureSpecMulticlusteringress:
    def __init__(self, *, config_membership: builtins.str) -> None:
        '''
        :param config_membership: Fully-qualified Membership name which hosts the MultiClusterIngress CRD. Example: 'projects/foo-proj/locations/global/memberships/bar'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#config_membership GoogleGkeHubFeature#config_membership}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce8c3a62c769980b7f93cf2edbffe98917ecb67fc4a4a6aabc2fb99ee94be14)
            check_type(argname="argument config_membership", value=config_membership, expected_type=type_hints["config_membership"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_membership": config_membership,
        }

    @builtins.property
    def config_membership(self) -> builtins.str:
        '''Fully-qualified Membership name which hosts the MultiClusterIngress CRD. Example: 'projects/foo-proj/locations/global/memberships/bar'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#config_membership GoogleGkeHubFeature#config_membership}
        '''
        result = self._values.get("config_membership")
        assert result is not None, "Required property 'config_membership' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureSpecMulticlusteringress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureSpecMulticlusteringressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecMulticlusteringressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad81127b33c2b0e6813a7026e0d8eda73232a37d2cf37afe703091d9fd111991)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24c07c77d5e970836b08f70883f56fded7253982a2bc1640a3f71c46b57ad843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configMembership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecMulticlusteringress]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecMulticlusteringress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureSpecMulticlusteringress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66151f2dd284af0c5432dec8d73c2f4813e76746a47e860a412435dfa047d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1770caf88405b7f6776e89d06f2fe0159450f981e7b4d930151b9569cbb89b4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClusterupgrade")
    def put_clusterupgrade(
        self,
        *,
        upstream_fleets: typing.Sequence[builtins.str],
        gke_upgrade_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_conditions: typing.Optional[typing.Union[GoogleGkeHubFeatureSpecClusterupgradePostConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param upstream_fleets: Specified if other fleet should be considered as a source of upgrades. Currently, at most one upstream fleet is allowed. The fleet name should be either fleet project number or id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#upstream_fleets GoogleGkeHubFeature#upstream_fleets}
        :param gke_upgrade_overrides: gke_upgrade_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#gke_upgrade_overrides GoogleGkeHubFeature#gke_upgrade_overrides}
        :param post_conditions: post_conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#post_conditions GoogleGkeHubFeature#post_conditions}
        '''
        value = GoogleGkeHubFeatureSpecClusterupgrade(
            upstream_fleets=upstream_fleets,
            gke_upgrade_overrides=gke_upgrade_overrides,
            post_conditions=post_conditions,
        )

        return typing.cast(None, jsii.invoke(self, "putClusterupgrade", [value]))

    @jsii.member(jsii_name="putFleetobservability")
    def put_fleetobservability(
        self,
        *,
        logging_config: typing.Optional[typing.Union[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#logging_config GoogleGkeHubFeature#logging_config}
        '''
        value = GoogleGkeHubFeatureSpecFleetobservability(
            logging_config=logging_config
        )

        return typing.cast(None, jsii.invoke(self, "putFleetobservability", [value]))

    @jsii.member(jsii_name="putMulticlusteringress")
    def put_multiclusteringress(self, *, config_membership: builtins.str) -> None:
        '''
        :param config_membership: Fully-qualified Membership name which hosts the MultiClusterIngress CRD. Example: 'projects/foo-proj/locations/global/memberships/bar'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#config_membership GoogleGkeHubFeature#config_membership}
        '''
        value = GoogleGkeHubFeatureSpecMulticlusteringress(
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
        :param allowed_custom_roles: The list of allowed custom roles (ClusterRoles). If a custom role is not part of this list, it cannot be used in a fleet scope RBACRoleBinding. If a custom role in this list is in use, it cannot be removed from the list until the scope RBACRolebindings using it are deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#allowed_custom_roles GoogleGkeHubFeature#allowed_custom_roles}
        '''
        value = GoogleGkeHubFeatureSpecRbacrolebindingactuation(
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
    def clusterupgrade(self) -> GoogleGkeHubFeatureSpecClusterupgradeOutputReference:
        return typing.cast(GoogleGkeHubFeatureSpecClusterupgradeOutputReference, jsii.get(self, "clusterupgrade"))

    @builtins.property
    @jsii.member(jsii_name="fleetobservability")
    def fleetobservability(
        self,
    ) -> GoogleGkeHubFeatureSpecFleetobservabilityOutputReference:
        return typing.cast(GoogleGkeHubFeatureSpecFleetobservabilityOutputReference, jsii.get(self, "fleetobservability"))

    @builtins.property
    @jsii.member(jsii_name="multiclusteringress")
    def multiclusteringress(
        self,
    ) -> GoogleGkeHubFeatureSpecMulticlusteringressOutputReference:
        return typing.cast(GoogleGkeHubFeatureSpecMulticlusteringressOutputReference, jsii.get(self, "multiclusteringress"))

    @builtins.property
    @jsii.member(jsii_name="rbacrolebindingactuation")
    def rbacrolebindingactuation(
        self,
    ) -> "GoogleGkeHubFeatureSpecRbacrolebindingactuationOutputReference":
        return typing.cast("GoogleGkeHubFeatureSpecRbacrolebindingactuationOutputReference", jsii.get(self, "rbacrolebindingactuation"))

    @builtins.property
    @jsii.member(jsii_name="clusterupgradeInput")
    def clusterupgrade_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecClusterupgrade]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecClusterupgrade], jsii.get(self, "clusterupgradeInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetobservabilityInput")
    def fleetobservability_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecFleetobservability]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecFleetobservability], jsii.get(self, "fleetobservabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="multiclusteringressInput")
    def multiclusteringress_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecMulticlusteringress]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecMulticlusteringress], jsii.get(self, "multiclusteringressInput"))

    @builtins.property
    @jsii.member(jsii_name="rbacrolebindingactuationInput")
    def rbacrolebindingactuation_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureSpecRbacrolebindingactuation"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureSpecRbacrolebindingactuation"], jsii.get(self, "rbacrolebindingactuationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeHubFeatureSpec]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GoogleGkeHubFeatureSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b72535f66bdce188bdaf0358b7749d640baa2c743e6bb2806589b8abf7672ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecRbacrolebindingactuation",
    jsii_struct_bases=[],
    name_mapping={"allowed_custom_roles": "allowedCustomRoles"},
)
class GoogleGkeHubFeatureSpecRbacrolebindingactuation:
    def __init__(
        self,
        *,
        allowed_custom_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_custom_roles: The list of allowed custom roles (ClusterRoles). If a custom role is not part of this list, it cannot be used in a fleet scope RBACRoleBinding. If a custom role in this list is in use, it cannot be removed from the list until the scope RBACRolebindings using it are deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#allowed_custom_roles GoogleGkeHubFeature#allowed_custom_roles}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a15b3942103029f009db52a521132f5a57a889d760b7fbc21148dfee9727e0a9)
            check_type(argname="argument allowed_custom_roles", value=allowed_custom_roles, expected_type=type_hints["allowed_custom_roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_custom_roles is not None:
            self._values["allowed_custom_roles"] = allowed_custom_roles

    @builtins.property
    def allowed_custom_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of allowed custom roles (ClusterRoles).

        If a custom role is not part of this list, it cannot be used in a fleet scope RBACRoleBinding. If a custom role in this list is in use, it cannot be removed from the list until the scope RBACRolebindings using it are deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#allowed_custom_roles GoogleGkeHubFeature#allowed_custom_roles}
        '''
        result = self._values.get("allowed_custom_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureSpecRbacrolebindingactuation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureSpecRbacrolebindingactuationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureSpecRbacrolebindingactuationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76c375d609f6e3d2e19bcf36041e896267a81021303f0e919026a12700a2f960)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0aeedc2bb7419a6c9c9c5abc7f01def23f78c7278d87c52d361a201430fd0aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedCustomRoles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureSpecRbacrolebindingactuation]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureSpecRbacrolebindingactuation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureSpecRbacrolebindingactuation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07060b371ca37df20893e9ada3f2be38b5ab41dce8d8ed6b7fe25fa46e03ddae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeHubFeatureState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9400a53f1d2c02f681ce4aaf18ad33d770c1e17ce71e13290a0f3da83ea19f13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleGkeHubFeatureStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae50adcfd4c021bb948612c54cd9d4eb370d57cca0c2cda74f67effa0087cc82)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFeatureStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af195211492d7dd4f943d15ba7680ef2232af29d41f3bc0425be1fcf319f07b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eac94f3a56ce2d542490d208c97004a63eb59346e3cba6fa5d479ed5f4cee99f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ada1a852188d065886530df98ec57b83a36d5b70e5139f800ae1c86b3d138595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe8c042022e64800699bc7a964d54d4b6fff30cd1ea109dbc4a80cc1ad234527)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> "GoogleGkeHubFeatureStateStateList":
        return typing.cast("GoogleGkeHubFeatureStateStateList", jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeHubFeatureState]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GoogleGkeHubFeatureState]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c08db772ddd689f30144aaf16e7dd0eac64a1330bd8facd99a531ec424e446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureStateState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleGkeHubFeatureStateState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureStateState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureStateStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureStateStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b5a14cc81d2a5c7c1f56e76d50f718d0914086bafbc8a513c98578fc2274399)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleGkeHubFeatureStateStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__385358badaa73434267a107e0d53ae29ec1d513c9a7a66bf177d5507272c859e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFeatureStateStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ccbe1ec311db34a75b8ea0a63571db031670d79e7b908d5b5fb70f23c5d3eda)
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
            type_hints = typing.get_type_hints(_typecheckingstub__748b86fa6ab9125207e0c30ba65d1cf8ec850610a2d9a8a2c257462b08fdca75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca7a663cda0a039122198e7618deb196f2f067da0796f013e72797028018959e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureStateStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureStateStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__678da69eaec2b9729345a7f1531ee6c2f4d2ed3bf86d52eab5bc3a803c3a9f21)
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
    def internal_value(self) -> typing.Optional[GoogleGkeHubFeatureStateState]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureStateState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureStateState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd881efce29d06298e7c7beae8115bd17c9f60d6df33a59cfdfc613fd706978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleGkeHubFeatureTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#create GoogleGkeHubFeature#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#delete GoogleGkeHubFeature#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#update GoogleGkeHubFeature#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcd8cd82bc78b4ced6a17466d5256d68ea5e1a3b993293607e0b93ec72f38089)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#create GoogleGkeHubFeature#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#delete GoogleGkeHubFeature#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature#update GoogleGkeHubFeature#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeature.GoogleGkeHubFeatureTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__daf55a554e788180fc1303e962e2ac4104ed10aad9e012fd74c782c64349ba64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82e57d0cea4e8e1b4e075feb36dd8f8337802da0bd6b6cfd2afe0e7f50e4fa80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3ab78b2e77f8e108d481e055f8addce49c3bae8d4e1b2bb689e121f51c63e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e341a274ce555e736cfb1f453f08b9608812b623a74ecadfa92cf3d0db7a28a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f4c0a2549222a54bcbfb2ed796eef4d60345519178e0215bf45d6aaa0e21d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleGkeHubFeature",
    "GoogleGkeHubFeatureConfig",
    "GoogleGkeHubFeatureFleetDefaultMemberConfig",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGitOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOciOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigMesh",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigMeshOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationList",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary",
    "GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference",
    "GoogleGkeHubFeatureResourceState",
    "GoogleGkeHubFeatureResourceStateList",
    "GoogleGkeHubFeatureResourceStateOutputReference",
    "GoogleGkeHubFeatureSpec",
    "GoogleGkeHubFeatureSpecClusterupgrade",
    "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides",
    "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesList",
    "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesOutputReference",
    "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions",
    "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditionsOutputReference",
    "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade",
    "GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgradeOutputReference",
    "GoogleGkeHubFeatureSpecClusterupgradeOutputReference",
    "GoogleGkeHubFeatureSpecClusterupgradePostConditions",
    "GoogleGkeHubFeatureSpecClusterupgradePostConditionsOutputReference",
    "GoogleGkeHubFeatureSpecFleetobservability",
    "GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig",
    "GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig",
    "GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfigOutputReference",
    "GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig",
    "GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfigOutputReference",
    "GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigOutputReference",
    "GoogleGkeHubFeatureSpecFleetobservabilityOutputReference",
    "GoogleGkeHubFeatureSpecMulticlusteringress",
    "GoogleGkeHubFeatureSpecMulticlusteringressOutputReference",
    "GoogleGkeHubFeatureSpecOutputReference",
    "GoogleGkeHubFeatureSpecRbacrolebindingactuation",
    "GoogleGkeHubFeatureSpecRbacrolebindingactuationOutputReference",
    "GoogleGkeHubFeatureState",
    "GoogleGkeHubFeatureStateList",
    "GoogleGkeHubFeatureStateOutputReference",
    "GoogleGkeHubFeatureStateState",
    "GoogleGkeHubFeatureStateStateList",
    "GoogleGkeHubFeatureStateStateOutputReference",
    "GoogleGkeHubFeatureTimeouts",
    "GoogleGkeHubFeatureTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fcb0a3fd65f9fa47bafa789113e2cc02ccb5128458d34d152ae7bd13698b9aa7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    fleet_default_member_config: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[GoogleGkeHubFeatureSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeHubFeatureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__58f967f1975fad4e1ba0d785a20e7605bac04ac05977e754d73c4f641f0a2538(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f7ee43ae258d522c9ddea24987abb84477958d09875e186a32b9d2d330abbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5541c7fa13f702682f24628bd612b50eb847693374d09fba356f4cf8ec6487(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f22c23edb7c67172605b89e0ec8b04b99e5fa900792a2b5fa0f0e5081dffa64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3db494c632e775b125d48a446928f7094203f9499b2591a62874290572a9201(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8650d74f696329dae2a01fd36941dc53c4a32755ffe0ed2df00e995d086e9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf1728319ee978297c79124f6478064ea7f9cd7b09411f94fa2528c1cded37b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    fleet_default_member_config: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[GoogleGkeHubFeatureSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeHubFeatureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e543bd9e370f2eb2897a9d7d6e37a41cd7e903f77ff903e44457606ed1422178(
    *,
    configmanagement: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement, typing.Dict[builtins.str, typing.Any]]] = None,
    mesh: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigMesh, typing.Dict[builtins.str, typing.Any]]] = None,
    policycontroller: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea580e2e37453bbfd577e8716127d6f1472dc9e2232bc1bac4999e071e69f93(
    *,
    config_sync: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync, typing.Dict[builtins.str, typing.Any]]] = None,
    management: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d13afff405078acd1b3aa212c6e765bbf5e457ce90a0bfd17c9820016f9758cd(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    git: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit, typing.Dict[builtins.str, typing.Any]]] = None,
    metrics_gcp_service_account_email: typing.Optional[builtins.str] = None,
    oci: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci, typing.Dict[builtins.str, typing.Any]]] = None,
    prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0721edb45f7f37b510e07059bf09b7cb4d9fbbf5f84bc9612638b01910e585d8(
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

def _typecheckingstub__69ca12cea6baf74a45cc215787ab5e5571e4b15e9adfe0b122254ce5081c86a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d674e1977682fb7e8baada27b075e67e513b3e7fa6194a1fbdd88b48794948e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd16413611ea85897778be596aa32ac5ade6dd783deb546ee66760cc33d929ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d84128a1235b54c8268f0a1b34c28ed3b4e646ef3c350bbef8f313996b8e5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3326516501d9838b678e2db364776f5613f3dc5847ccfb70501abee4074e5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4bb78b655c841da6d328600412cc59fe133ff1a40748ec28e141b5eb298260(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57cc8603bd2fe5d12b054ec8d3f3fbebb57bd4fee5cae57f5507d8f0dc03fd71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016563e035e5612dbd6ede75a1e8ed695381d29358cd07e0579e8ca241065069(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c6b1303616fe1dfe4298b8cb64d0c1b50b6ed93344f38843b19858852b755c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50993643f6f2eea684201c856ace207ea8116e90d4b1b907a0db7bac98f3532(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncGit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9cfab22367d7ddc9eb4e8e2e6942e5abfbe420dc1930f40c85ad4a9fc7b90b(
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

def _typecheckingstub__3261b51ddaf26d37116b7adf6f35a96b7119887ef164d6f188ec938f88d9d72d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480bc25330085595d5edc13198ae9e268d279fb588e2ec03d1fd49513b7f330b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371eb2a29f8d48c5c678be6235cc737eeef673c2643aee25dea33aba06063aa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15847209393b1a73e01ca1931e8de4512710496174df853a7b0d7b128573b9d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c063d112c5623252658ba71497e4704f935b4b63ef07d0becbd6221bd2cbe9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3bb645f7e8efe18ed9008b95a1916fb4bb0fb05450c4055edd6f00763eb4d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a2c942042dd09684426ea69b99bd0a543c896a3ec00321d51f390842ba24b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e109f493d653966a6ef4872199622a6de2fb577dc1a605f5fff7fabb137cf07d(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSyncOci],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12093991d4573e8b272cd913c816cad93fda263f5781e6fb4710802d39ae02b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2d1c21ff56fa649539990efe326b75ebcd9bbc2763922ceaad2f2b4e15a3bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113b3db8bdaa71efaf995ca7cc6e91451975808c458412795fdb96ba86980e1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1074eb8bed469b6dfa70674e7508fc68b727f3a73d4819a9906c98b7ffa390(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__364e696aa1b39d01aab3aa039de19e783bd8e9c1adb0344bd80756071e8650fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cedf565b3d840e25876cece03876ddec659bde75fc4f9864ac3cf7a0342adc7b(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagementConfigSync],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca17c0a7173decdf3f45ab38a6988afd1e868369f53464576542506bd1089fc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d083b135e516c050de2d42e4a4e16bf35e4cefe56e72248ab9c1d54fec45364d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e5b22a28d29cf3c54e126039d5a0ec911cf227e55d7f09cbffb7b4be05105d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7698b4f15f358e332419974552d05760e0994029d3e92c5ce5ba706243b328(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigConfigmanagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c42dcc8e4ea75751510b2c933502f459fd5dc4af69ee20ef8368a7c140cffd(
    *,
    management: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185134601c70944bb1f7d9bb65b4842ffebb02d54c6802dfd6c9df1c577a363c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9025fbf0d7ee34f3042701e38957e07b761f66810597a18527524680f9b06449(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807901be3db45f3acb440b1fcafd32969740d2201a044e6b1e11bc41299173ca(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigMesh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6710aeb75b71c25ae6d0a4242dfd6b677af815b37af0ccf89decae0228af157c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998fb7c8ba6729775381015285e37dd962563f46b4bcaa298b549479f942bdeb(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e77637cadef0bcfb4b448daeb4a001144abf9c61c0d01fba368560910aa5ec(
    *,
    policy_controller_hub_config: typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig, typing.Dict[builtins.str, typing.Any]],
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b2c5334530be3aa815d63d06209f259fb25df2fb44f19504a733d9c0e7f294(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47b6c718c032d3129d23257cb64e35692e2493552c17033f17854ebb61a4f1cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e595bdaece62a778a5bbe002f57843748ee471243fb73a14a3f5f7a4e4bcc88(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontroller],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c70079cb7cc23fac347a547aac0fcc158bb7155787f4e19e8eee2ab80fe252(
    *,
    install_spec: builtins.str,
    audit_interval_seconds: typing.Optional[jsii.Number] = None,
    constraint_violation_limit: typing.Optional[jsii.Number] = None,
    deployment_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitoring: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring, typing.Dict[builtins.str, typing.Any]]] = None,
    mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policy_content: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent, typing.Dict[builtins.str, typing.Any]]] = None,
    referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3308441b7ae9f33d05065ee589a0779ff2a267a32511c584f7e023683ad70a(
    *,
    component: builtins.str,
    container_resources: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources, typing.Dict[builtins.str, typing.Any]]] = None,
    pod_affinity: typing.Optional[builtins.str] = None,
    pod_toleration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    replica_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7113a8fb31aa110b2e71d6f7dc9620d99465a71fee0746a7c924e72ac0dcb555(
    *,
    limits: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    requests: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b32a2a1ece23dc0bb4330b29a00d47f5d6a59f8888472fe8638ddf66adadd9b(
    *,
    cpu: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee99b498071208d822e8e8e9459b8b38329a953f338b54e8ada6c6edd1285d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37db0a0680e8898e6c1bb71c893bab82b155f337e363d534a307c95bfedbaf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69751878a72cf61595a5c99bad3fd3a5031a1c083697affc0a97f942e89b393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a06870231fa0296828dafb8314662bfb61f0bbdcf13a9692aa4c2233bbabcdc(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57313e86a346efbc2429ea2d4d83cfd8fb74ee9b16dc8733ee7d05e112c1ee80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef027deb50b1bf00eda8e23f899ed7056a741154be66e9a37bad28cb4694a33f(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250e6b65f03205e0275244783889a71170da85ce23f180b0455577eda55a0052(
    *,
    cpu: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825151c0de4e61c8a501e9fdc85ba8de4721ec413e9c2e0c0520ef47c0cb08d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5adc92004c65fb553a89173b76c1eb9cc93860057098b73b8fdf64a05a099a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281059f67f6f47ce11e072b7c373418427051620692d2ceebaaff8040bc65c79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93169b7b782e724083661c774bb7a650f813e359ce45e9d94e35cc49b48f29cc(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fd6cfdc0c4a95d4213a5a53db890ed0af0eb41d878d1bd385c90144752ae70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24b3bfba2612b2cdce8a83169fe44e2331ca145e224d7c3cd718da649a1913a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b668a5d8e5e63458ec8ff62c85950312fa13b60fe78bf0a03aa4b03acb43c3bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd871d736fc0cb512cbc5ef2ddc338aabf871431afc8a2451f425d9d5a107db(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47281aa661e2ab89f93d70b67b6fda12789b97d9ed4639b8b6fad10a4cca6d35(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c23ac9fe172081e158f6808b89867a22f1a845ef16d7181154fccfa2250546(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa56914804517cbf648ab41b4b520801bffcd99ca197fffa40041a0085fff435(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166f2233f7c33885268b5fd2b4244ef7aa2f57883420675b0039b7b3543336d0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f82a6fc04c0ebc0d203c283ac7bb070877f7082f857a020c28e3ab13a031ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0eccf1bb2a2d44c39959b51522425aef9f8ff41f1436b1c89d8f24978a2c241(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d29ef850a3b555ebb0c2b73ce89509ea8f34e14ec66a439ae32c3b25e96c31f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff10dadf25a0fafb360626a6ab15aa32e7766d9beadee48edad11c043a94b4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d41872650ca72d8278cedf55c31f75057db42a95a85095c69ced1c1040908e4(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8bd04083fe3a6a9ba22573a6fb78243df3c31739631e006d94e5cbcdcb0fd7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2e887afce1759186b20c80e09c97691687a42d19159789177c40d0b6027e03(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9c3b814f4301d256267ed62351724e042002276f435c4c4cb4aee718580137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908915d086b5cf6f37116e2f6ab9e300c8a62a9876710a085eca280b50bd2afa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78d5fbea907cca0861a77141cc6e9ac631f37507ffdbc2d7580111c95f3ca24(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016ae138256acc1940d2b711ea9e12bdba0a79ab705881b46e2b5df898e10655(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06280b962343fba1f33b1522b84389eeca7bd9acad5493897e810dcc11712ed3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c833a02899992413b46e1b5ad2655667299bb9a515487f906158c77962c4090(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed52423f07b56fcfed853657f9936c5e7125e096b68c3c8f39b2acd9fa5e502(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ccb72a987a81676b9b6be49ab0d63c35c303215d864901fec6118185f3e37fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e593c6ac5ca9bb575d0779461df3b7eb8a6ac57e99b2110561275bc58ac589b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22c6b0b4e2b13d16bb1eaa049c5fff44dce41830022fcd11e3b8020996e486d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodToleration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca84ef0c3b4cc3d9460d1c5502b3deb118eff6cea840ead9c5405cf9a903acf7(
    *,
    backends: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ad8871c722837f4eb13a23dfbf3b1c4cdbc08944c44f3010d06d15a3258dcf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4053c542f2c4e1f3be55be53e49ff556da86d321fe5864517684e76b4420a2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e0b86e2353c73c6e04b55287176bca17c9d398978ad44630a770d094d44f97(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigMonitoring],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805354dc24c7f02a08debb8e58ec6577760fdb4419189045c99eae98ce067aad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7735f483462dff19d477ca15a2386189da6a2fd94a9c3c9f3391fd523563b6c8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ddced2711338d8353fed2163410156380a696c1d2e135dc9c5c164ae32dc2d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d629c890ce240fb77df97fa30b62708bc324951f16aef49631e6d6ad33a2f6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6487028e8cdf21c229f371bc19d3afd87d4a2d3978f228a7b5c786779d2e664a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d203f944f7c25b322fbea400eb151afaa9da47ca66c35ed53eece492ad23d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959f4a1f06ef8cd9532778684f0dbf187c92d4a728ec314d777d13a948588a69(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758bafa3cee9b182a8bdbb3554bedb7aa7eff5960ec1124d2a895232f59aed88(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9585a2a5df940b6718424eac10eb266da730139d0d0c852f9110f1c821305bfc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b38faff90502dce2ac53da1913e54e465904991fe5075ca41dc2c74e6318d21(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2eda8144401dd8dad9090206d3e3e71142fab1386e43a934be0374021e6458b(
    *,
    bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles, typing.Dict[builtins.str, typing.Any]]]]] = None,
    template_library: typing.Optional[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e846ad5f5cd6613912f8839885784518d783f710dcca2bd33819a2b6b5b904b(
    *,
    bundle: builtins.str,
    exempted_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d53cdee1c35b711a2107b7c9c4d94943a69763cfe9e2fa32c01ca697ad30a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa70578683c046154c04f729097a7488b6e0a1757ef3079f337c57babcb559c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee05e8d7fba69a833bf10e08e60cde8f9f84e5d78727eaf08008b72ccfc3197(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029fe1da5e8036e64095c7b56a3a7e3ad84ad5b62116869d186002dcae9c39d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724b3986972f1f81b4e8a54e550ecc8974cd40042e66016161e1ac193f122d71(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b2b2e1eb0ccaf7dcbb6da583af7a7f015ae2d4181875d2869c4cd63bf51c15(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171e1c93b1cfaa1064bae24fbbd3a1e05bd5902d44f3d07089d9bb86a121aac4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71099e7bbd8c4dd9568e36d8fbd0108c9365aee5e9c5d05599108078da8d637c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4712cc00d8ef1bf34e7810cff3361bd145379d9d359b7fdbec47dde7f46a21c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a92dff9bfb1f4efc0f258b1a9313f32936b937a905c9b149be01efacba6372b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e07aadd97d580a8bc6c5c9b3db01d7dee4b0bf6f10d8178513722f2c505737(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03f752a6d2291fdc6949c016c1a21bf292a59837dadb9273ff00d9ff65b06c3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentBundles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa288494e9d223539a89846ecbcac08f7316837a76a8280e2e3204ec21f8a4e8(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d16fb271116835a3c7e4bb9c18be3fb9883eb970279a7585d985501b263863(
    *,
    installation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645343a72262466d7c0299065e8ba7aeff688ffbbce07799df05ede276809ac8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134bb3cda57603737edf80ed4739a8e495605afcbd753f61724b1ffce2ac562c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c324bd63a87f66a0e3b6db4777b5333cb5e0fb8c95833195b59351e37370190e(
    value: typing.Optional[GoogleGkeHubFeatureFleetDefaultMemberConfigPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1d2d88370d1223823343c2c031752606e794b9abd460e2f3c9a2851ac5125b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d904627009a4f880b9dd170f1b3844d0598e8bf87dbbf9d2c0e7514ae1c5595b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18c3d40393e00090df5a89c64b245879019da5457e7b69a6194aac4b2d16d44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3214317708b2332e2ef93286e0c78e75a8dbeacb70736549fc7c1feeac317d8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a8e710f324d5cc19d9f303b395542f662973af9542a31e607166a6345e8a1a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9823f175e6d5a0c6a5029e73c67c721b74f8809454b294a9fb700e1fd82fe39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8bcaae70ece5f4f953795bd10825e17f0f0f406312be4d914e8be9148f6aa9b(
    value: typing.Optional[GoogleGkeHubFeatureResourceState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d061d7c79bb94b3cd8b8e284adcf8b1dc6311abcb09f92c38bfaad2f62cd10(
    *,
    clusterupgrade: typing.Optional[typing.Union[GoogleGkeHubFeatureSpecClusterupgrade, typing.Dict[builtins.str, typing.Any]]] = None,
    fleetobservability: typing.Optional[typing.Union[GoogleGkeHubFeatureSpecFleetobservability, typing.Dict[builtins.str, typing.Any]]] = None,
    multiclusteringress: typing.Optional[typing.Union[GoogleGkeHubFeatureSpecMulticlusteringress, typing.Dict[builtins.str, typing.Any]]] = None,
    rbacrolebindingactuation: typing.Optional[typing.Union[GoogleGkeHubFeatureSpecRbacrolebindingactuation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38a5823aec2c7ceb7031d11377e5527c67296f4d851450bf1328a1153345db3(
    *,
    upstream_fleets: typing.Sequence[builtins.str],
    gke_upgrade_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    post_conditions: typing.Optional[typing.Union[GoogleGkeHubFeatureSpecClusterupgradePostConditions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b3f77e45b75d3faa47d92594ff21027dc30467c61d636329896dc2922da2f3(
    *,
    post_conditions: typing.Union[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions, typing.Dict[builtins.str, typing.Any]],
    upgrade: typing.Union[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7bf03287de35ab1046413cd74dbd1871cc53d711c35e98a4f42de31c56b4ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533bd44b881a087b4567f64728bff421431ff47959f1ac956661a41e36f1c235(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b6822a846dd4303944127c6aa02527640dcf62d33fc0f3c7774484eb3c2074(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62fcc4f7080f047891885b5670a964a53913cb48194692ee3275cb9769774aa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a19cce341136dd46dc5a1a93f53fa1ede0e40301dc12439f1069a65a9941a18(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f086720447c5ab16bb9dc8e497fcaf8f6e7d30a5b693a2a527f8f3000e621a9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0458b19508303303020514288304054e2e40b89378d07fd80ae52b830fde8f16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd165f23c755660ba0a797be995bfcc7155451c7c0c3b3e2565a3591208bd2e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d9127c751687f67ed8cc633366440ee724b7da83876fd6135cf309d9923cbc(
    *,
    soaking: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46389715736951be3b80b6f68de765f6eb89777ea8a08c0d4d0ae922d5c64bfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380f515575148f98a5927553f68d800bb62cfb7c105310e4c347283ba4921933(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f109d4de656564984dfcba05220051815d248feb1297c16eb506c3ba71086a8(
    value: typing.Optional[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesPostConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c2cc45d44393705ef271d2bd2540ff977bb63251bcdecc5dff84d31a6284a8(
    *,
    name: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab93205b017f0140600d625ca3b87fb9226c5073b43eddc70a301123d240d5ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d273ecf8e55039e9f61edb0bca5d4b005c9ef39c8586d86dfd4dc28f0d294032(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c385e70de7d0eee48d3a395302c03790bb4d6cd438ff520671b665097687b99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c29b74a02791faab0044d58461babe9fa6ab336c2bb50b571c02f3d6cc7eb85(
    value: typing.Optional[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverridesUpgrade],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01eaebcd1d22d9f66ff9e742b829ff1c49aad63219e88205db077c0290c1ccbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b875caba6c5bc6e68a7473dd25b4cf9d51dfa8fb81f7dd2b9e3c1e8c809b7a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureSpecClusterupgradeGkeUpgradeOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6445d9edcaf8429642eb4a4ce9ee167dad08a374a2177e5ce8fedb4879038619(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b697b1d3e7db5f6d93ad0fcff166309003a2b2ad025aaddf195698e4342934d0(
    value: typing.Optional[GoogleGkeHubFeatureSpecClusterupgrade],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507ea075dd732441f2baf98e609ff2e3ba8be484a70aa9027764f951a280a5af(
    *,
    soaking: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38474516932ddb9d3036e299baf46eae85e6dd3d445b9c48911d389e56f0624(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f3fe9e3c3a8b5b788ee1c87e7e2ee47691335ca4ded14d711cc3628e6cc8fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0bb4a9840dae1902b5b6de51fe57c436813184d367d742b50b9a257eac046f(
    value: typing.Optional[GoogleGkeHubFeatureSpecClusterupgradePostConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90cc420bb6c8200aca13bc9b30339e23450c89bc33b34c6826aca627336e1a64(
    *,
    logging_config: typing.Optional[typing.Union[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1092c7c58e734fccb996c1c549826a7626c61d45d2879559bab1695b801ece9(
    *,
    default_config: typing.Optional[typing.Union[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    fleet_scope_logs_config: typing.Optional[typing.Union[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e84035f25007be86d9fb4adc1572616afc5de73220a19015e9cbc8a61099c53(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b41e0b11a974217ed1cb7e5adacdb225e4f8263326dbc7f8f4645897679172(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987d88ea6015aef5360b5a3c509fdb4cbb81f27a7fde0b9d6fea5eaa068d8769(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114fc0a179098862bd259a125d98beb6371790d2c14fad6952e4325543601a82(
    value: typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigDefaultConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d30147e7e49005a62d94e1bc258059df84dc36121aad77dc99646be5a5b107(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0d043d61b3a56a836bd87a2349603ca00cb3559c0b8cef9364b2fd5e547230(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e7195d440669a390a33b3a9a4a36016f632f9984b8fe41d95dc480195893a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d46d23518f45d4970ef346a33787f55c0e8cc6927089cc20008005dc788bea(
    value: typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfigFleetScopeLogsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0809a1e8c2d153d6e28b37e26529c2aa772140653fe404e06998f7b8a194af8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0e44599f76cdf54cc6278791c2dbfd3796928a40aafe923e6d24b764f81567(
    value: typing.Optional[GoogleGkeHubFeatureSpecFleetobservabilityLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29cf13dd41417b92383eb8f5ffd08984e4098a868225e3433f11a864bd62399a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6ca4231f8a846df7e1a33b02b303f564eb4e148eec7a5442977f7e03461aa0(
    value: typing.Optional[GoogleGkeHubFeatureSpecFleetobservability],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce8c3a62c769980b7f93cf2edbffe98917ecb67fc4a4a6aabc2fb99ee94be14(
    *,
    config_membership: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad81127b33c2b0e6813a7026e0d8eda73232a37d2cf37afe703091d9fd111991(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c07c77d5e970836b08f70883f56fded7253982a2bc1640a3f71c46b57ad843(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66151f2dd284af0c5432dec8d73c2f4813e76746a47e860a412435dfa047d3e(
    value: typing.Optional[GoogleGkeHubFeatureSpecMulticlusteringress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1770caf88405b7f6776e89d06f2fe0159450f981e7b4d930151b9569cbb89b4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b72535f66bdce188bdaf0358b7749d640baa2c743e6bb2806589b8abf7672ee7(
    value: typing.Optional[GoogleGkeHubFeatureSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15b3942103029f009db52a521132f5a57a889d760b7fbc21148dfee9727e0a9(
    *,
    allowed_custom_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c375d609f6e3d2e19bcf36041e896267a81021303f0e919026a12700a2f960(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aeedc2bb7419a6c9c9c5abc7f01def23f78c7278d87c52d361a201430fd0aee(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07060b371ca37df20893e9ada3f2be38b5ab41dce8d8ed6b7fe25fa46e03ddae(
    value: typing.Optional[GoogleGkeHubFeatureSpecRbacrolebindingactuation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9400a53f1d2c02f681ce4aaf18ad33d770c1e17ce71e13290a0f3da83ea19f13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae50adcfd4c021bb948612c54cd9d4eb370d57cca0c2cda74f67effa0087cc82(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af195211492d7dd4f943d15ba7680ef2232af29d41f3bc0425be1fcf319f07b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac94f3a56ce2d542490d208c97004a63eb59346e3cba6fa5d479ed5f4cee99f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada1a852188d065886530df98ec57b83a36d5b70e5139f800ae1c86b3d138595(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe8c042022e64800699bc7a964d54d4b6fff30cd1ea109dbc4a80cc1ad234527(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c08db772ddd689f30144aaf16e7dd0eac64a1330bd8facd99a531ec424e446(
    value: typing.Optional[GoogleGkeHubFeatureState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5a14cc81d2a5c7c1f56e76d50f718d0914086bafbc8a513c98578fc2274399(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385358badaa73434267a107e0d53ae29ec1d513c9a7a66bf177d5507272c859e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccbe1ec311db34a75b8ea0a63571db031670d79e7b908d5b5fb70f23c5d3eda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748b86fa6ab9125207e0c30ba65d1cf8ec850610a2d9a8a2c257462b08fdca75(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7a663cda0a039122198e7618deb196f2f067da0796f013e72797028018959e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678da69eaec2b9729345a7f1531ee6c2f4d2ed3bf86d52eab5bc3a803c3a9f21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd881efce29d06298e7c7beae8115bd17c9f60d6df33a59cfdfc613fd706978(
    value: typing.Optional[GoogleGkeHubFeatureStateState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd8cd82bc78b4ced6a17466d5256d68ea5e1a3b993293607e0b93ec72f38089(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf55a554e788180fc1303e962e2ac4104ed10aad9e012fd74c782c64349ba64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e57d0cea4e8e1b4e075feb36dd8f8337802da0bd6b6cfd2afe0e7f50e4fa80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3ab78b2e77f8e108d481e055f8addce49c3bae8d4e1b2bb689e121f51c63e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e341a274ce555e736cfb1f453f08b9608812b623a74ecadfa92cf3d0db7a28a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f4c0a2549222a54bcbfb2ed796eef4d60345519178e0215bf45d6aaa0e21d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
