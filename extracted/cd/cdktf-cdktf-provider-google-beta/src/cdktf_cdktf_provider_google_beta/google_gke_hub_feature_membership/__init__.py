r'''
# `google_gke_hub_feature_membership`

Refer to the Terraform Registry for docs: [`google_gke_hub_feature_membership`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership).
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


class GoogleGkeHubFeatureMembership(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembership",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership google_gke_hub_feature_membership}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        feature: builtins.str,
        location: builtins.str,
        membership: builtins.str,
        configmanagement: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagement", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        membership_location: typing.Optional[builtins.str] = None,
        mesh: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        policycontroller: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipPolicycontroller", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership google_gke_hub_feature_membership} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param feature: The name of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#feature GoogleGkeHubFeatureMembership#feature}
        :param location: The location of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#location GoogleGkeHubFeatureMembership#location}
        :param membership: The name of the membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#membership GoogleGkeHubFeatureMembership#membership}
        :param configmanagement: configmanagement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#configmanagement GoogleGkeHubFeatureMembership#configmanagement}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#id GoogleGkeHubFeatureMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param membership_location: The location of the membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#membership_location GoogleGkeHubFeatureMembership#membership_location}
        :param mesh: mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#mesh GoogleGkeHubFeatureMembership#mesh}
        :param policycontroller: policycontroller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policycontroller GoogleGkeHubFeatureMembership#policycontroller}
        :param project: The project of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#project GoogleGkeHubFeatureMembership#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#timeouts GoogleGkeHubFeatureMembership#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0b329ce2d05634c944e2255fda1d2c15cbf151adf11be93d9c4d1405e05220)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleGkeHubFeatureMembershipConfig(
            feature=feature,
            location=location,
            membership=membership,
            configmanagement=configmanagement,
            id=id,
            membership_location=membership_location,
            mesh=mesh,
            policycontroller=policycontroller,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleGkeHubFeatureMembership resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleGkeHubFeatureMembership to import.
        :param import_from_id: The id of the existing GoogleGkeHubFeatureMembership that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleGkeHubFeatureMembership to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d7a908ab625d0d48ce4d400681dd52e44c533c33188c1881a13cdde6b86aca3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfigmanagement")
    def put_configmanagement(
        self,
        *,
        binauthz: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementBinauthz", typing.Dict[builtins.str, typing.Any]]] = None,
        config_sync: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementConfigSync", typing.Dict[builtins.str, typing.Any]]] = None,
        hierarchy_controller: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController", typing.Dict[builtins.str, typing.Any]]] = None,
        management: typing.Optional[builtins.str] = None,
        policy_controller: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementPolicyController", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param binauthz: binauthz block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#binauthz GoogleGkeHubFeatureMembership#binauthz}
        :param config_sync: config_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#config_sync GoogleGkeHubFeatureMembership#config_sync}
        :param hierarchy_controller: hierarchy_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#hierarchy_controller GoogleGkeHubFeatureMembership#hierarchy_controller}
        :param management: Set this field to MANAGEMENT_AUTOMATIC to enable Config Sync auto-upgrades, and set this field to MANAGEMENT_MANUAL or MANAGEMENT_UNSPECIFIED to disable Config Sync auto-upgrades. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#management GoogleGkeHubFeatureMembership#management}
        :param policy_controller: policy_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_controller GoogleGkeHubFeatureMembership#policy_controller}
        :param version: Optional. Version of ACM to install. Defaults to the latest version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#version GoogleGkeHubFeatureMembership#version}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagement(
            binauthz=binauthz,
            config_sync=config_sync,
            hierarchy_controller=hierarchy_controller,
            management=management,
            policy_controller=policy_controller,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putConfigmanagement", [value]))

    @jsii.member(jsii_name="putMesh")
    def put_mesh(
        self,
        *,
        control_plane: typing.Optional[builtins.str] = None,
        management: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control_plane: **DEPRECATED** Whether to automatically manage Service Mesh control planes. Possible values: CONTROL_PLANE_MANAGEMENT_UNSPECIFIED, AUTOMATIC, MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#control_plane GoogleGkeHubFeatureMembership#control_plane}
        :param management: Whether to automatically manage Service Mesh. Possible values: MANAGEMENT_UNSPECIFIED, MANAGEMENT_AUTOMATIC, MANAGEMENT_MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#management GoogleGkeHubFeatureMembership#management}
        '''
        value = GoogleGkeHubFeatureMembershipMesh(
            control_plane=control_plane, management=management
        )

        return typing.cast(None, jsii.invoke(self, "putMesh", [value]))

    @jsii.member(jsii_name="putPolicycontroller")
    def put_policycontroller(
        self,
        *,
        policy_controller_hub_config: typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig", typing.Dict[builtins.str, typing.Any]],
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param policy_controller_hub_config: policy_controller_hub_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_controller_hub_config GoogleGkeHubFeatureMembership#policy_controller_hub_config}
        :param version: Optional. Version of Policy Controller to install. Defaults to the latest version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#version GoogleGkeHubFeatureMembership#version}
        '''
        value = GoogleGkeHubFeatureMembershipPolicycontroller(
            policy_controller_hub_config=policy_controller_hub_config, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putPolicycontroller", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#create GoogleGkeHubFeatureMembership#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#delete GoogleGkeHubFeatureMembership#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#update GoogleGkeHubFeatureMembership#update}.
        '''
        value = GoogleGkeHubFeatureMembershipTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConfigmanagement")
    def reset_configmanagement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigmanagement", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMembershipLocation")
    def reset_membership_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembershipLocation", []))

    @jsii.member(jsii_name="resetMesh")
    def reset_mesh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMesh", []))

    @jsii.member(jsii_name="resetPolicycontroller")
    def reset_policycontroller(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicycontroller", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="configmanagement")
    def configmanagement(
        self,
    ) -> "GoogleGkeHubFeatureMembershipConfigmanagementOutputReference":
        return typing.cast("GoogleGkeHubFeatureMembershipConfigmanagementOutputReference", jsii.get(self, "configmanagement"))

    @builtins.property
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> "GoogleGkeHubFeatureMembershipMeshOutputReference":
        return typing.cast("GoogleGkeHubFeatureMembershipMeshOutputReference", jsii.get(self, "mesh"))

    @builtins.property
    @jsii.member(jsii_name="policycontroller")
    def policycontroller(
        self,
    ) -> "GoogleGkeHubFeatureMembershipPolicycontrollerOutputReference":
        return typing.cast("GoogleGkeHubFeatureMembershipPolicycontrollerOutputReference", jsii.get(self, "policycontroller"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleGkeHubFeatureMembershipTimeoutsOutputReference":
        return typing.cast("GoogleGkeHubFeatureMembershipTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="configmanagementInput")
    def configmanagement_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagement"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagement"], jsii.get(self, "configmanagementInput"))

    @builtins.property
    @jsii.member(jsii_name="featureInput")
    def feature_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="membershipInput")
    def membership_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "membershipInput"))

    @builtins.property
    @jsii.member(jsii_name="membershipLocationInput")
    def membership_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "membershipLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="meshInput")
    def mesh_input(self) -> typing.Optional["GoogleGkeHubFeatureMembershipMesh"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipMesh"], jsii.get(self, "meshInput"))

    @builtins.property
    @jsii.member(jsii_name="policycontrollerInput")
    def policycontroller_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipPolicycontroller"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipPolicycontroller"], jsii.get(self, "policycontrollerInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeHubFeatureMembershipTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeHubFeatureMembershipTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="feature")
    def feature(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "feature"))

    @feature.setter
    def feature(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62872bdfceafad454f1f77b15f0c4cc026f50a42b15c1ba4ae1e073493d445cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "feature", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0958d3b43f6eeee77da3758cde573467dcc5caf896edce568f597a324e95a596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026490971551372bb2b4367c899e7d13d507691fcd381768b3818da3e4687d8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membership")
    def membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "membership"))

    @membership.setter
    def membership(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b83bed14422792af7953f5b45e04cf6f355b207c43f6d8e8c84d5f3625b5217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membershipLocation")
    def membership_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "membershipLocation"))

    @membership_location.setter
    def membership_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a94dcd8c44e4d90793d3fdd02f2f2341ee7d07d2339008dad97d7888fa6e957f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membershipLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf9355e466a5d9bc98e79e3e26b9069d4848147b9de0e5c7e2116507a9f86f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "feature": "feature",
        "location": "location",
        "membership": "membership",
        "configmanagement": "configmanagement",
        "id": "id",
        "membership_location": "membershipLocation",
        "mesh": "mesh",
        "policycontroller": "policycontroller",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleGkeHubFeatureMembershipConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        feature: builtins.str,
        location: builtins.str,
        membership: builtins.str,
        configmanagement: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagement", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        membership_location: typing.Optional[builtins.str] = None,
        mesh: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        policycontroller: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipPolicycontroller", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param feature: The name of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#feature GoogleGkeHubFeatureMembership#feature}
        :param location: The location of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#location GoogleGkeHubFeatureMembership#location}
        :param membership: The name of the membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#membership GoogleGkeHubFeatureMembership#membership}
        :param configmanagement: configmanagement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#configmanagement GoogleGkeHubFeatureMembership#configmanagement}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#id GoogleGkeHubFeatureMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param membership_location: The location of the membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#membership_location GoogleGkeHubFeatureMembership#membership_location}
        :param mesh: mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#mesh GoogleGkeHubFeatureMembership#mesh}
        :param policycontroller: policycontroller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policycontroller GoogleGkeHubFeatureMembership#policycontroller}
        :param project: The project of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#project GoogleGkeHubFeatureMembership#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#timeouts GoogleGkeHubFeatureMembership#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(configmanagement, dict):
            configmanagement = GoogleGkeHubFeatureMembershipConfigmanagement(**configmanagement)
        if isinstance(mesh, dict):
            mesh = GoogleGkeHubFeatureMembershipMesh(**mesh)
        if isinstance(policycontroller, dict):
            policycontroller = GoogleGkeHubFeatureMembershipPolicycontroller(**policycontroller)
        if isinstance(timeouts, dict):
            timeouts = GoogleGkeHubFeatureMembershipTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc454f576b0fc2b00803677a901ef7a86701247db18f878efe02b250d0b540e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument feature", value=feature, expected_type=type_hints["feature"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument membership", value=membership, expected_type=type_hints["membership"])
            check_type(argname="argument configmanagement", value=configmanagement, expected_type=type_hints["configmanagement"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument membership_location", value=membership_location, expected_type=type_hints["membership_location"])
            check_type(argname="argument mesh", value=mesh, expected_type=type_hints["mesh"])
            check_type(argname="argument policycontroller", value=policycontroller, expected_type=type_hints["policycontroller"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "feature": feature,
            "location": location,
            "membership": membership,
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
        if configmanagement is not None:
            self._values["configmanagement"] = configmanagement
        if id is not None:
            self._values["id"] = id
        if membership_location is not None:
            self._values["membership_location"] = membership_location
        if mesh is not None:
            self._values["mesh"] = mesh
        if policycontroller is not None:
            self._values["policycontroller"] = policycontroller
        if project is not None:
            self._values["project"] = project
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
    def feature(self) -> builtins.str:
        '''The name of the feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#feature GoogleGkeHubFeatureMembership#feature}
        '''
        result = self._values.get("feature")
        assert result is not None, "Required property 'feature' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#location GoogleGkeHubFeatureMembership#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def membership(self) -> builtins.str:
        '''The name of the membership.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#membership GoogleGkeHubFeatureMembership#membership}
        '''
        result = self._values.get("membership")
        assert result is not None, "Required property 'membership' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configmanagement(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagement"]:
        '''configmanagement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#configmanagement GoogleGkeHubFeatureMembership#configmanagement}
        '''
        result = self._values.get("configmanagement")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagement"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#id GoogleGkeHubFeatureMembership#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def membership_location(self) -> typing.Optional[builtins.str]:
        '''The location of the membership.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#membership_location GoogleGkeHubFeatureMembership#membership_location}
        '''
        result = self._values.get("membership_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh(self) -> typing.Optional["GoogleGkeHubFeatureMembershipMesh"]:
        '''mesh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#mesh GoogleGkeHubFeatureMembership#mesh}
        '''
        result = self._values.get("mesh")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipMesh"], result)

    @builtins.property
    def policycontroller(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipPolicycontroller"]:
        '''policycontroller block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policycontroller GoogleGkeHubFeatureMembership#policycontroller}
        '''
        result = self._values.get("policycontroller")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipPolicycontroller"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project of the feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#project GoogleGkeHubFeatureMembership#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleGkeHubFeatureMembershipTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#timeouts GoogleGkeHubFeatureMembership#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagement",
    jsii_struct_bases=[],
    name_mapping={
        "binauthz": "binauthz",
        "config_sync": "configSync",
        "hierarchy_controller": "hierarchyController",
        "management": "management",
        "policy_controller": "policyController",
        "version": "version",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagement:
    def __init__(
        self,
        *,
        binauthz: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementBinauthz", typing.Dict[builtins.str, typing.Any]]] = None,
        config_sync: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementConfigSync", typing.Dict[builtins.str, typing.Any]]] = None,
        hierarchy_controller: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController", typing.Dict[builtins.str, typing.Any]]] = None,
        management: typing.Optional[builtins.str] = None,
        policy_controller: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementPolicyController", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param binauthz: binauthz block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#binauthz GoogleGkeHubFeatureMembership#binauthz}
        :param config_sync: config_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#config_sync GoogleGkeHubFeatureMembership#config_sync}
        :param hierarchy_controller: hierarchy_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#hierarchy_controller GoogleGkeHubFeatureMembership#hierarchy_controller}
        :param management: Set this field to MANAGEMENT_AUTOMATIC to enable Config Sync auto-upgrades, and set this field to MANAGEMENT_MANUAL or MANAGEMENT_UNSPECIFIED to disable Config Sync auto-upgrades. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#management GoogleGkeHubFeatureMembership#management}
        :param policy_controller: policy_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_controller GoogleGkeHubFeatureMembership#policy_controller}
        :param version: Optional. Version of ACM to install. Defaults to the latest version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#version GoogleGkeHubFeatureMembership#version}
        '''
        if isinstance(binauthz, dict):
            binauthz = GoogleGkeHubFeatureMembershipConfigmanagementBinauthz(**binauthz)
        if isinstance(config_sync, dict):
            config_sync = GoogleGkeHubFeatureMembershipConfigmanagementConfigSync(**config_sync)
        if isinstance(hierarchy_controller, dict):
            hierarchy_controller = GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController(**hierarchy_controller)
        if isinstance(policy_controller, dict):
            policy_controller = GoogleGkeHubFeatureMembershipConfigmanagementPolicyController(**policy_controller)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673cdaf2b6ede0f68164ef94e08c87a8859b1245ac5838d1574e6f62dd273404)
            check_type(argname="argument binauthz", value=binauthz, expected_type=type_hints["binauthz"])
            check_type(argname="argument config_sync", value=config_sync, expected_type=type_hints["config_sync"])
            check_type(argname="argument hierarchy_controller", value=hierarchy_controller, expected_type=type_hints["hierarchy_controller"])
            check_type(argname="argument management", value=management, expected_type=type_hints["management"])
            check_type(argname="argument policy_controller", value=policy_controller, expected_type=type_hints["policy_controller"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if binauthz is not None:
            self._values["binauthz"] = binauthz
        if config_sync is not None:
            self._values["config_sync"] = config_sync
        if hierarchy_controller is not None:
            self._values["hierarchy_controller"] = hierarchy_controller
        if management is not None:
            self._values["management"] = management
        if policy_controller is not None:
            self._values["policy_controller"] = policy_controller
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def binauthz(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementBinauthz"]:
        '''binauthz block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#binauthz GoogleGkeHubFeatureMembership#binauthz}
        '''
        result = self._values.get("binauthz")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementBinauthz"], result)

    @builtins.property
    def config_sync(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementConfigSync"]:
        '''config_sync block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#config_sync GoogleGkeHubFeatureMembership#config_sync}
        '''
        result = self._values.get("config_sync")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementConfigSync"], result)

    @builtins.property
    def hierarchy_controller(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController"]:
        '''hierarchy_controller block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#hierarchy_controller GoogleGkeHubFeatureMembership#hierarchy_controller}
        '''
        result = self._values.get("hierarchy_controller")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController"], result)

    @builtins.property
    def management(self) -> typing.Optional[builtins.str]:
        '''Set this field to MANAGEMENT_AUTOMATIC to enable Config Sync auto-upgrades, and set this field to MANAGEMENT_MANUAL or MANAGEMENT_UNSPECIFIED to disable Config Sync auto-upgrades.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#management GoogleGkeHubFeatureMembership#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_controller(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementPolicyController"]:
        '''policy_controller block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_controller GoogleGkeHubFeatureMembership#policy_controller}
        '''
        result = self._values.get("policy_controller")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementPolicyController"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Optional. Version of ACM to install. Defaults to the latest version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#version GoogleGkeHubFeatureMembership#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementBinauthz",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleGkeHubFeatureMembershipConfigmanagementBinauthz:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether binauthz is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04225f057deab844c0cb925b29cad3893f701acf41f98f3132d42c2afb3ef3a)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether binauthz is enabled in this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementBinauthz(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipConfigmanagementBinauthzOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementBinauthzOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ccaf84a28f547aa26e9ab25245859391b3a22e96a645ceffe71511cd995c2c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5e4c12084bc62c3dc923dc0158909a8b392638774937a49a714438d0209db909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b76c6c4faf5a0f9077c6b3fbdc82feef33b6cd96a01b492887650117f2bc726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSync",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_overrides": "deploymentOverrides",
        "enabled": "enabled",
        "git": "git",
        "metrics_gcp_service_account_email": "metricsGcpServiceAccountEmail",
        "oci": "oci",
        "prevent_drift": "preventDrift",
        "source_format": "sourceFormat",
        "stop_syncing": "stopSyncing",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagementConfigSync:
    def __init__(
        self,
        *,
        deployment_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        git: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit", typing.Dict[builtins.str, typing.Any]]] = None,
        metrics_gcp_service_account_email: typing.Optional[builtins.str] = None,
        oci: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci", typing.Dict[builtins.str, typing.Any]]] = None,
        prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_format: typing.Optional[builtins.str] = None,
        stop_syncing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param deployment_overrides: deployment_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#deployment_overrides GoogleGkeHubFeatureMembership#deployment_overrides}
        :param enabled: Enables the installation of ConfigSync. If set to true, ConfigSync resources will be created and the other ConfigSync fields will be applied if exist. If set to false, all other ConfigSync fields will be ignored, ConfigSync resources will be deleted. If omitted, ConfigSync resources will be managed depends on the presence of the git or oci field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#git GoogleGkeHubFeatureMembership#git}
        :param metrics_gcp_service_account_email: Deprecated: If Workload Identity Federation for GKE is enabled, Google Cloud Service Account is no longer needed for exporting Config Sync metrics: https://cloud.google.com/kubernetes-engine/enterprise/config-sync/docs/how-to/monitor-config-sync-cloud-monitoring#custom-monitoring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#metrics_gcp_service_account_email GoogleGkeHubFeatureMembership#metrics_gcp_service_account_email}
        :param oci: oci block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#oci GoogleGkeHubFeatureMembership#oci}
        :param prevent_drift: Set to true to enable the Config Sync admission webhook to prevent drifts. If set to ``false``, disables the Config Sync admission webhook and does not prevent drifts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#prevent_drift GoogleGkeHubFeatureMembership#prevent_drift}
        :param source_format: Specifies whether the Config Sync Repo is in "hierarchical" or "unstructured" mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#source_format GoogleGkeHubFeatureMembership#source_format}
        :param stop_syncing: Set to true to stop syncing configs for a single cluster. Default: false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#stop_syncing GoogleGkeHubFeatureMembership#stop_syncing}
        '''
        if isinstance(git, dict):
            git = GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit(**git)
        if isinstance(oci, dict):
            oci = GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci(**oci)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b061211c1a2c8d4fad557434b81bcefd5bade26fbd8ea7552b2fea3b03ed06)
            check_type(argname="argument deployment_overrides", value=deployment_overrides, expected_type=type_hints["deployment_overrides"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument git", value=git, expected_type=type_hints["git"])
            check_type(argname="argument metrics_gcp_service_account_email", value=metrics_gcp_service_account_email, expected_type=type_hints["metrics_gcp_service_account_email"])
            check_type(argname="argument oci", value=oci, expected_type=type_hints["oci"])
            check_type(argname="argument prevent_drift", value=prevent_drift, expected_type=type_hints["prevent_drift"])
            check_type(argname="argument source_format", value=source_format, expected_type=type_hints["source_format"])
            check_type(argname="argument stop_syncing", value=stop_syncing, expected_type=type_hints["stop_syncing"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deployment_overrides is not None:
            self._values["deployment_overrides"] = deployment_overrides
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
        if stop_syncing is not None:
            self._values["stop_syncing"] = stop_syncing

    @builtins.property
    def deployment_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides"]]]:
        '''deployment_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#deployment_overrides GoogleGkeHubFeatureMembership#deployment_overrides}
        '''
        result = self._values.get("deployment_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides"]]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the installation of ConfigSync.

        If set to true, ConfigSync resources will be created and the other ConfigSync fields will be applied if exist. If set to false, all other ConfigSync fields will be ignored, ConfigSync resources will be deleted. If omitted, ConfigSync resources will be managed depends on the presence of the git or oci field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def git(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit"]:
        '''git block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#git GoogleGkeHubFeatureMembership#git}
        '''
        result = self._values.get("git")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit"], result)

    @builtins.property
    def metrics_gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''Deprecated: If Workload Identity Federation for GKE is enabled, Google Cloud Service Account is no longer needed for exporting Config Sync metrics: https://cloud.google.com/kubernetes-engine/enterprise/config-sync/docs/how-to/monitor-config-sync-cloud-monitoring#custom-monitoring.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#metrics_gcp_service_account_email GoogleGkeHubFeatureMembership#metrics_gcp_service_account_email}
        '''
        result = self._values.get("metrics_gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oci(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci"]:
        '''oci block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#oci GoogleGkeHubFeatureMembership#oci}
        '''
        result = self._values.get("oci")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci"], result)

    @builtins.property
    def prevent_drift(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to enable the Config Sync admission webhook to prevent drifts.

        If set to ``false``, disables the Config Sync admission webhook and does not prevent drifts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#prevent_drift GoogleGkeHubFeatureMembership#prevent_drift}
        '''
        result = self._values.get("prevent_drift")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_format(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the Config Sync Repo is in "hierarchical" or "unstructured" mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#source_format GoogleGkeHubFeatureMembership#source_format}
        '''
        result = self._values.get("source_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stop_syncing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to stop syncing configs for a single cluster. Default: false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#stop_syncing GoogleGkeHubFeatureMembership#stop_syncing}
        '''
        result = self._values.get("stop_syncing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementConfigSync(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "containers": "containers",
        "deployment_name": "deploymentName",
        "deployment_namespace": "deploymentNamespace",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides:
    def __init__(
        self,
        *,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        deployment_name: typing.Optional[builtins.str] = None,
        deployment_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#containers GoogleGkeHubFeatureMembership#containers}
        :param deployment_name: The name of the Deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#deployment_name GoogleGkeHubFeatureMembership#deployment_name}
        :param deployment_namespace: The namespace of the Deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#deployment_namespace GoogleGkeHubFeatureMembership#deployment_namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd2c15bb4725666e77845b22d24e13b8c8976c203b1c8a488548ad6625eba838)
            check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
            check_type(argname="argument deployment_name", value=deployment_name, expected_type=type_hints["deployment_name"])
            check_type(argname="argument deployment_namespace", value=deployment_namespace, expected_type=type_hints["deployment_namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if containers is not None:
            self._values["containers"] = containers
        if deployment_name is not None:
            self._values["deployment_name"] = deployment_name
        if deployment_namespace is not None:
            self._values["deployment_namespace"] = deployment_namespace

    @builtins.property
    def containers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers"]]]:
        '''containers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#containers GoogleGkeHubFeatureMembership#containers}
        '''
        result = self._values.get("containers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers"]]], result)

    @builtins.property
    def deployment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Deployment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#deployment_name GoogleGkeHubFeatureMembership#deployment_name}
        '''
        result = self._values.get("deployment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the Deployment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#deployment_namespace GoogleGkeHubFeatureMembership#deployment_namespace}
        '''
        result = self._values.get("deployment_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers",
    jsii_struct_bases=[],
    name_mapping={
        "container_name": "containerName",
        "cpu_limit": "cpuLimit",
        "cpu_request": "cpuRequest",
        "memory_limit": "memoryLimit",
        "memory_request": "memoryRequest",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers:
    def __init__(
        self,
        *,
        container_name: typing.Optional[builtins.str] = None,
        cpu_limit: typing.Optional[builtins.str] = None,
        cpu_request: typing.Optional[builtins.str] = None,
        memory_limit: typing.Optional[builtins.str] = None,
        memory_request: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_name: The name of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#container_name GoogleGkeHubFeatureMembership#container_name}
        :param cpu_limit: The CPU limit of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#cpu_limit GoogleGkeHubFeatureMembership#cpu_limit}
        :param cpu_request: The CPU request of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#cpu_request GoogleGkeHubFeatureMembership#cpu_request}
        :param memory_limit: The memory limit of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#memory_limit GoogleGkeHubFeatureMembership#memory_limit}
        :param memory_request: The memory request of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#memory_request GoogleGkeHubFeatureMembership#memory_request}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb93f64e45d29e9efe7b52b31ba856a6ca8793c5c8608abad31594022ee18a9a)
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument cpu_limit", value=cpu_limit, expected_type=type_hints["cpu_limit"])
            check_type(argname="argument cpu_request", value=cpu_request, expected_type=type_hints["cpu_request"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
            check_type(argname="argument memory_request", value=memory_request, expected_type=type_hints["memory_request"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_name is not None:
            self._values["container_name"] = container_name
        if cpu_limit is not None:
            self._values["cpu_limit"] = cpu_limit
        if cpu_request is not None:
            self._values["cpu_request"] = cpu_request
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit
        if memory_request is not None:
            self._values["memory_request"] = memory_request

    @builtins.property
    def container_name(self) -> typing.Optional[builtins.str]:
        '''The name of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#container_name GoogleGkeHubFeatureMembership#container_name}
        '''
        result = self._values.get("container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_limit(self) -> typing.Optional[builtins.str]:
        '''The CPU limit of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#cpu_limit GoogleGkeHubFeatureMembership#cpu_limit}
        '''
        result = self._values.get("cpu_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_request(self) -> typing.Optional[builtins.str]:
        '''The CPU request of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#cpu_request GoogleGkeHubFeatureMembership#cpu_request}
        '''
        result = self._values.get("cpu_request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory_limit(self) -> typing.Optional[builtins.str]:
        '''The memory limit of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#memory_limit GoogleGkeHubFeatureMembership#memory_limit}
        '''
        result = self._values.get("memory_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory_request(self) -> typing.Optional[builtins.str]:
        '''The memory request of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#memory_request GoogleGkeHubFeatureMembership#memory_request}
        '''
        result = self._values.get("memory_request")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43ffa452456d8344354109ed36ff44f3f9c716147d98d74bf50476cf7a1a4b73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c92af53791e072d1bf428d7bf570b1921f732e604b6891dad90485872a2a1d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fbc12efafb6b520ef8ae4bd82c27c1e3da1ec9322a1b3cd0d9b3da2449363b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62c0d3a6501caac8eafcb01734e3cfe33beed35220c6df4b11e41f443036aca9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f6bb96759fb9bbbfee432af2c2393964a97a92431c8152caaed973e8c17f75c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a6ab582294fce73c16399c4035ecfeacd58f2778d24522b5141ee4c1c2de92a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31c02c146d04e7071ab30a38f10a3e8f9c02093325827aef5ee979b5eebbade8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContainerName")
    def reset_container_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerName", []))

    @jsii.member(jsii_name="resetCpuLimit")
    def reset_cpu_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuLimit", []))

    @jsii.member(jsii_name="resetCpuRequest")
    def reset_cpu_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuRequest", []))

    @jsii.member(jsii_name="resetMemoryLimit")
    def reset_memory_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryLimit", []))

    @jsii.member(jsii_name="resetMemoryRequest")
    def reset_memory_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryRequest", []))

    @builtins.property
    @jsii.member(jsii_name="containerNameInput")
    def container_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuLimitInput")
    def cpu_limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuRequestInput")
    def cpu_request_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryLimitInput")
    def memory_limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryRequestInput")
    def memory_request_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="containerName")
    def container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerName"))

    @container_name.setter
    def container_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bfce67092d97c86ae188c68107061c656d413de82a124b020c3ad6d9ce91206)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuLimit")
    def cpu_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuLimit"))

    @cpu_limit.setter
    def cpu_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1179cfada2964d1a2ab8fbb945b4c3d9ea6d3099f852bbd36b891d97e9990a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuRequest")
    def cpu_request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuRequest"))

    @cpu_request.setter
    def cpu_request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5709fa8b361195b11d2ebb51b73982975c357eff6648d78eb89dd4a8e64ed03a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryLimit")
    def memory_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memoryLimit"))

    @memory_limit.setter
    def memory_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84737783ad14da09bd5485f69d080157e962be6286dcea75c874071af76c6818)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryRequest")
    def memory_request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memoryRequest"))

    @memory_request.setter
    def memory_request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3106df2077b8e47c7b699e614049e051a911a6e3a8d23c504e70cd71427d01b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6517691602b1cc2547fb757f62e4148c14100f0c5cde8cf42fb387ae2a7ba69e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__628550d3524678ef8d1d593ce9c50059b99cd6a85ed7d42d19988d59e88d1ba6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b536985ab1773a7b1eca24da0fbc4d6292e8648160b091d9330100c68875bc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5616392e35b43d270e3f4fc3327d371e9a87875b08bf8aa2e1c6d7337bc08545)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d6b1e870b376cbeb736bd17f782b7cbc4a4c7f144e662e2ecee3cfd0d459f91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3018a7a65a5b2050080ffa0f90f1e5483a822822d3aa2206df13f9a32f84916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ea7aeff29238c6828b36873a9fc384fcc8ae26906ade301c0f1d159d840245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bbbba33795ddedb60a2805fecda17c61045574986055b905b5eead58a582766)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putContainers")
    def put_containers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba702b749ffafcb1c4eac187a0b33851c76f9ca3f3a94573716efa1a0250e726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainers", [value]))

    @jsii.member(jsii_name="resetContainers")
    def reset_containers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainers", []))

    @jsii.member(jsii_name="resetDeploymentName")
    def reset_deployment_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentName", []))

    @jsii.member(jsii_name="resetDeploymentNamespace")
    def reset_deployment_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentNamespace", []))

    @builtins.property
    @jsii.member(jsii_name="containers")
    def containers(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersList:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersList, jsii.get(self, "containers"))

    @builtins.property
    @jsii.member(jsii_name="containersInput")
    def containers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]], jsii.get(self, "containersInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentNameInput")
    def deployment_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentNamespaceInput")
    def deployment_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentName")
    def deployment_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentName"))

    @deployment_name.setter
    def deployment_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae26b3c82a2aaa3ceec5e0cd589d57253d405f930428423d42211f6cc063c6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentNamespace")
    def deployment_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentNamespace"))

    @deployment_namespace.setter
    def deployment_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b2926a4c9c394033bc5268b532f5116335ed95d1e0c0437854d7fef9f3eb038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__554635c5a86661c39b6297195d29e47583649b82b4987980b236a151f7b086d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit",
    jsii_struct_bases=[],
    name_mapping={
        "gcp_service_account_email": "gcpServiceAccountEmail",
        "https_proxy": "httpsProxy",
        "policy_dir": "policyDir",
        "secret_type": "secretType",
        "sync_branch": "syncBranch",
        "sync_repo": "syncRepo",
        "sync_rev": "syncRev",
        "sync_wait_secs": "syncWaitSecs",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit:
    def __init__(
        self,
        *,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        secret_type: typing.Optional[builtins.str] = None,
        sync_branch: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_rev: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gcp_service_account_email: The GCP Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#gcp_service_account_email GoogleGkeHubFeatureMembership#gcp_service_account_email}
        :param https_proxy: URL for the HTTPS proxy to be used when communicating with the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#https_proxy GoogleGkeHubFeatureMembership#https_proxy}
        :param policy_dir: The path within the Git repository that represents the top level of the repo to sync. Default: the root directory of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_dir GoogleGkeHubFeatureMembership#policy_dir}
        :param secret_type: Type of secret configured for access to the Git repo. Must be one of ssh, cookiefile, gcenode, token, gcpserviceaccount or none. The validation of this is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#secret_type GoogleGkeHubFeatureMembership#secret_type}
        :param sync_branch: The branch of the repository to sync from. Default: master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_branch GoogleGkeHubFeatureMembership#sync_branch}
        :param sync_repo: The URL of the Git repository to use as the source of truth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_repo GoogleGkeHubFeatureMembership#sync_repo}
        :param sync_rev: Git revision (tag or hash) to check out. Default HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_rev GoogleGkeHubFeatureMembership#sync_rev}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_wait_secs GoogleGkeHubFeatureMembership#sync_wait_secs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522bb8107583a9bd504bbc0a88d70d193e145ce1e06bde67bb83c4e49c978ef0)
            check_type(argname="argument gcp_service_account_email", value=gcp_service_account_email, expected_type=type_hints["gcp_service_account_email"])
            check_type(argname="argument https_proxy", value=https_proxy, expected_type=type_hints["https_proxy"])
            check_type(argname="argument policy_dir", value=policy_dir, expected_type=type_hints["policy_dir"])
            check_type(argname="argument secret_type", value=secret_type, expected_type=type_hints["secret_type"])
            check_type(argname="argument sync_branch", value=sync_branch, expected_type=type_hints["sync_branch"])
            check_type(argname="argument sync_repo", value=sync_repo, expected_type=type_hints["sync_repo"])
            check_type(argname="argument sync_rev", value=sync_rev, expected_type=type_hints["sync_rev"])
            check_type(argname="argument sync_wait_secs", value=sync_wait_secs, expected_type=type_hints["sync_wait_secs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gcp_service_account_email is not None:
            self._values["gcp_service_account_email"] = gcp_service_account_email
        if https_proxy is not None:
            self._values["https_proxy"] = https_proxy
        if policy_dir is not None:
            self._values["policy_dir"] = policy_dir
        if secret_type is not None:
            self._values["secret_type"] = secret_type
        if sync_branch is not None:
            self._values["sync_branch"] = sync_branch
        if sync_repo is not None:
            self._values["sync_repo"] = sync_repo
        if sync_rev is not None:
            self._values["sync_rev"] = sync_rev
        if sync_wait_secs is not None:
            self._values["sync_wait_secs"] = sync_wait_secs

    @builtins.property
    def gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''The GCP Service Account Email used for auth when secretType is gcpServiceAccount.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#gcp_service_account_email GoogleGkeHubFeatureMembership#gcp_service_account_email}
        '''
        result = self._values.get("gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_proxy(self) -> typing.Optional[builtins.str]:
        '''URL for the HTTPS proxy to be used when communicating with the Git repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#https_proxy GoogleGkeHubFeatureMembership#https_proxy}
        '''
        result = self._values.get("https_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_dir(self) -> typing.Optional[builtins.str]:
        '''The path within the Git repository that represents the top level of the repo to sync.

        Default: the root directory of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_dir GoogleGkeHubFeatureMembership#policy_dir}
        '''
        result = self._values.get("policy_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_type(self) -> typing.Optional[builtins.str]:
        '''Type of secret configured for access to the Git repo.

        Must be one of ssh, cookiefile, gcenode, token, gcpserviceaccount or none. The validation of this is case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#secret_type GoogleGkeHubFeatureMembership#secret_type}
        '''
        result = self._values.get("secret_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_branch(self) -> typing.Optional[builtins.str]:
        '''The branch of the repository to sync from. Default: master.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_branch GoogleGkeHubFeatureMembership#sync_branch}
        '''
        result = self._values.get("sync_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_repo(self) -> typing.Optional[builtins.str]:
        '''The URL of the Git repository to use as the source of truth.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_repo GoogleGkeHubFeatureMembership#sync_repo}
        '''
        result = self._values.get("sync_repo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_rev(self) -> typing.Optional[builtins.str]:
        '''Git revision (tag or hash) to check out. Default HEAD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_rev GoogleGkeHubFeatureMembership#sync_rev}
        '''
        result = self._values.get("sync_rev")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_wait_secs(self) -> typing.Optional[builtins.str]:
        '''Period in seconds between consecutive syncs. Default: 15.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_wait_secs GoogleGkeHubFeatureMembership#sync_wait_secs}
        '''
        result = self._values.get("sync_wait_secs")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d2da75bf48b92eba5bc3158a896ab3aebe0b6716c430da291f45da5ca95500)
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

    @jsii.member(jsii_name="resetSecretType")
    def reset_secret_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretType", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bbb743348fc43111f1567ac0610ac3d6dff9c7562083a1fc22943e5738383831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsProxy")
    def https_proxy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsProxy"))

    @https_proxy.setter
    def https_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d9469d57214be7b6f662759aed696b58cdbb99d64a7cd04642f72aa8f7e48f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyDir")
    def policy_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDir"))

    @policy_dir.setter
    def policy_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2963c67df0ee74ee7e84e5973f998ae53a4503f4f6739ec2d7a4f3ab327b561d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretType")
    def secret_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretType"))

    @secret_type.setter
    def secret_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f10700065e46b3ec1e8fb174b913a6a51decfb8075e09350db7020ce779d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncBranch")
    def sync_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncBranch"))

    @sync_branch.setter
    def sync_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26675f5523359c070f8fb775fb18716fd8fa2f3bb6f13578e7910464ff8cf46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncRepo")
    def sync_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRepo"))

    @sync_repo.setter
    def sync_repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42d85c9e8df10282a54068d6e9935b4ec4caa701f7d43f3515a6c31179ded0c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRepo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncRev")
    def sync_rev(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRev"))

    @sync_rev.setter
    def sync_rev(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4b0761bbbc1158b733837e824c1e7a4570d2f0a7c1b6c60eb484a99b7ea593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRev", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecs")
    def sync_wait_secs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncWaitSecs"))

    @sync_wait_secs.setter
    def sync_wait_secs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20512acf91ddba89927c8fc325bed1d5210bef80b857d393761002e3ec7b3478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncWaitSecs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773106aa5a71f1fe66e70ded79460931dd2e73ccfdc2eb289cebe3a02344181e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci",
    jsii_struct_bases=[],
    name_mapping={
        "gcp_service_account_email": "gcpServiceAccountEmail",
        "policy_dir": "policyDir",
        "secret_type": "secretType",
        "sync_repo": "syncRepo",
        "sync_wait_secs": "syncWaitSecs",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci:
    def __init__(
        self,
        *,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        secret_type: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gcp_service_account_email: The GCP Service Account Email used for auth when secret_type is gcpserviceaccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#gcp_service_account_email GoogleGkeHubFeatureMembership#gcp_service_account_email}
        :param policy_dir: The absolute path of the directory that contains the local resources. Default: the root directory of the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_dir GoogleGkeHubFeatureMembership#policy_dir}
        :param secret_type: Type of secret configured for access to the OCI Image. Must be one of gcenode, gcpserviceaccount or none. The validation of this is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#secret_type GoogleGkeHubFeatureMembership#secret_type}
        :param sync_repo: The OCI image repository URL for the package to sync from. e.g. LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME/PACKAGE_NAME. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_repo GoogleGkeHubFeatureMembership#sync_repo}
        :param sync_wait_secs: Period in seconds(int64 format) between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_wait_secs GoogleGkeHubFeatureMembership#sync_wait_secs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd4d5eb981ba65901bf2946568f738edde7b90817be9020c2d38418cd25d01f)
            check_type(argname="argument gcp_service_account_email", value=gcp_service_account_email, expected_type=type_hints["gcp_service_account_email"])
            check_type(argname="argument policy_dir", value=policy_dir, expected_type=type_hints["policy_dir"])
            check_type(argname="argument secret_type", value=secret_type, expected_type=type_hints["secret_type"])
            check_type(argname="argument sync_repo", value=sync_repo, expected_type=type_hints["sync_repo"])
            check_type(argname="argument sync_wait_secs", value=sync_wait_secs, expected_type=type_hints["sync_wait_secs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gcp_service_account_email is not None:
            self._values["gcp_service_account_email"] = gcp_service_account_email
        if policy_dir is not None:
            self._values["policy_dir"] = policy_dir
        if secret_type is not None:
            self._values["secret_type"] = secret_type
        if sync_repo is not None:
            self._values["sync_repo"] = sync_repo
        if sync_wait_secs is not None:
            self._values["sync_wait_secs"] = sync_wait_secs

    @builtins.property
    def gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''The GCP Service Account Email used for auth when secret_type is gcpserviceaccount.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#gcp_service_account_email GoogleGkeHubFeatureMembership#gcp_service_account_email}
        '''
        result = self._values.get("gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_dir(self) -> typing.Optional[builtins.str]:
        '''The absolute path of the directory that contains the local resources. Default: the root directory of the image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_dir GoogleGkeHubFeatureMembership#policy_dir}
        '''
        result = self._values.get("policy_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_type(self) -> typing.Optional[builtins.str]:
        '''Type of secret configured for access to the OCI Image.

        Must be one of gcenode, gcpserviceaccount or none. The validation of this is case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#secret_type GoogleGkeHubFeatureMembership#secret_type}
        '''
        result = self._values.get("secret_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_repo(self) -> typing.Optional[builtins.str]:
        '''The OCI image repository URL for the package to sync from. e.g. LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME/PACKAGE_NAME.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_repo GoogleGkeHubFeatureMembership#sync_repo}
        '''
        result = self._values.get("sync_repo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_wait_secs(self) -> typing.Optional[builtins.str]:
        '''Period in seconds(int64 format) between consecutive syncs. Default: 15.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_wait_secs GoogleGkeHubFeatureMembership#sync_wait_secs}
        '''
        result = self._values.get("sync_wait_secs")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2849418628ccfb2315571f2ff3f65c91f264460f538a3471a4e3f4d3806b8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGcpServiceAccountEmail")
    def reset_gcp_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpServiceAccountEmail", []))

    @jsii.member(jsii_name="resetPolicyDir")
    def reset_policy_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyDir", []))

    @jsii.member(jsii_name="resetSecretType")
    def reset_secret_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretType", []))

    @jsii.member(jsii_name="resetSyncRepo")
    def reset_sync_repo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncRepo", []))

    @jsii.member(jsii_name="resetSyncWaitSecs")
    def reset_sync_wait_secs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncWaitSecs", []))

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
    @jsii.member(jsii_name="gcpServiceAccountEmail")
    def gcp_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccountEmail"))

    @gcp_service_account_email.setter
    def gcp_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d26efccc73bba21b697ee9259baf0a47590ce24598b91d24e26432f6e138d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyDir")
    def policy_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDir"))

    @policy_dir.setter
    def policy_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b53a90aef8f2e04c657e158d6c39cef10c94fae202cd25f6d11646dcfa752d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretType")
    def secret_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretType"))

    @secret_type.setter
    def secret_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7730f004cd7fc4ddaf529723d942e4e3f338e517b9c49b29508bf437703c845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncRepo")
    def sync_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRepo"))

    @sync_repo.setter
    def sync_repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75328af60c0d1afdb7dc6a3726b7d260638544163a94af3c192edf3608a921d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRepo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecs")
    def sync_wait_secs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncWaitSecs"))

    @sync_wait_secs.setter
    def sync_wait_secs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfce158029b7637a2d734e6c6a3803f140be001093c1e21cde805cee0a0a26e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncWaitSecs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca09f24f1ec363bb702596d30042fb19469408b7209e0e101c36a22c14e33ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047282ccb356309cbe5ace85f01c64af12fb2abe45d58b180e6101e731aa4aca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeploymentOverrides")
    def put_deployment_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9b966e56683b318d7661cfd90dc3476113e6dacd3061e48fdf6afebeec1c6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeploymentOverrides", [value]))

    @jsii.member(jsii_name="putGit")
    def put_git(
        self,
        *,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        secret_type: typing.Optional[builtins.str] = None,
        sync_branch: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_rev: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gcp_service_account_email: The GCP Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#gcp_service_account_email GoogleGkeHubFeatureMembership#gcp_service_account_email}
        :param https_proxy: URL for the HTTPS proxy to be used when communicating with the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#https_proxy GoogleGkeHubFeatureMembership#https_proxy}
        :param policy_dir: The path within the Git repository that represents the top level of the repo to sync. Default: the root directory of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_dir GoogleGkeHubFeatureMembership#policy_dir}
        :param secret_type: Type of secret configured for access to the Git repo. Must be one of ssh, cookiefile, gcenode, token, gcpserviceaccount or none. The validation of this is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#secret_type GoogleGkeHubFeatureMembership#secret_type}
        :param sync_branch: The branch of the repository to sync from. Default: master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_branch GoogleGkeHubFeatureMembership#sync_branch}
        :param sync_repo: The URL of the Git repository to use as the source of truth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_repo GoogleGkeHubFeatureMembership#sync_repo}
        :param sync_rev: Git revision (tag or hash) to check out. Default HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_rev GoogleGkeHubFeatureMembership#sync_rev}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_wait_secs GoogleGkeHubFeatureMembership#sync_wait_secs}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit(
            gcp_service_account_email=gcp_service_account_email,
            https_proxy=https_proxy,
            policy_dir=policy_dir,
            secret_type=secret_type,
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
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        secret_type: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gcp_service_account_email: The GCP Service Account Email used for auth when secret_type is gcpserviceaccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#gcp_service_account_email GoogleGkeHubFeatureMembership#gcp_service_account_email}
        :param policy_dir: The absolute path of the directory that contains the local resources. Default: the root directory of the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_dir GoogleGkeHubFeatureMembership#policy_dir}
        :param secret_type: Type of secret configured for access to the OCI Image. Must be one of gcenode, gcpserviceaccount or none. The validation of this is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#secret_type GoogleGkeHubFeatureMembership#secret_type}
        :param sync_repo: The OCI image repository URL for the package to sync from. e.g. LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME/PACKAGE_NAME. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_repo GoogleGkeHubFeatureMembership#sync_repo}
        :param sync_wait_secs: Period in seconds(int64 format) between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#sync_wait_secs GoogleGkeHubFeatureMembership#sync_wait_secs}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci(
            gcp_service_account_email=gcp_service_account_email,
            policy_dir=policy_dir,
            secret_type=secret_type,
            sync_repo=sync_repo,
            sync_wait_secs=sync_wait_secs,
        )

        return typing.cast(None, jsii.invoke(self, "putOci", [value]))

    @jsii.member(jsii_name="resetDeploymentOverrides")
    def reset_deployment_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentOverrides", []))

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

    @jsii.member(jsii_name="resetStopSyncing")
    def reset_stop_syncing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStopSyncing", []))

    @builtins.property
    @jsii.member(jsii_name="deploymentOverrides")
    def deployment_overrides(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesList:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesList, jsii.get(self, "deploymentOverrides"))

    @builtins.property
    @jsii.member(jsii_name="git")
    def git(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference, jsii.get(self, "git"))

    @builtins.property
    @jsii.member(jsii_name="oci")
    def oci(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference, jsii.get(self, "oci"))

    @builtins.property
    @jsii.member(jsii_name="deploymentOverridesInput")
    def deployment_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]], jsii.get(self, "deploymentOverridesInput"))

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
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit], jsii.get(self, "gitInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsGcpServiceAccountEmailInput")
    def metrics_gcp_service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricsGcpServiceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="ociInput")
    def oci_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci], jsii.get(self, "ociInput"))

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
    @jsii.member(jsii_name="stopSyncingInput")
    def stop_syncing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stopSyncingInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__25272a7927a94ec9236b4ee4db181a9311f2bbef2c9bfdc67b2fc38dc9e0b914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsGcpServiceAccountEmail")
    def metrics_gcp_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricsGcpServiceAccountEmail"))

    @metrics_gcp_service_account_email.setter
    def metrics_gcp_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea81931103bff4e166f0cf752a93c24b5ec4a969bc7f65c2020bca44d41d4c9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6820a5620129cc3c93a53c4f2c95b355b437da49af19691c8c7a73ebd973a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventDrift", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFormat")
    def source_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFormat"))

    @source_format.setter
    def source_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4094b68a0609037532af69c466ae51b836b2075f358d9f79aaae1bdce2bf32b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stopSyncing")
    def stop_syncing(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stopSyncing"))

    @stop_syncing.setter
    def stop_syncing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52daa8ddf37aa524b3a192c7f12e2315b434f194d8f71c19495a86510be36d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopSyncing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd25ad1da63bf090cd3f39600fd52aa32f34ba770e0cfd2925de4788e79444dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "enable_hierarchical_resource_quota": "enableHierarchicalResourceQuota",
        "enable_pod_tree_labels": "enablePodTreeLabels",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_hierarchical_resource_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_pod_tree_labels: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: **DEPRECATED** Configuring Hierarchy Controller through the configmanagement feature is no longer recommended. Use https://github.com/kubernetes-sigs/hierarchical-namespaces instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        :param enable_hierarchical_resource_quota: Whether hierarchical resource quota is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enable_hierarchical_resource_quota GoogleGkeHubFeatureMembership#enable_hierarchical_resource_quota}
        :param enable_pod_tree_labels: Whether pod tree labels are enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enable_pod_tree_labels GoogleGkeHubFeatureMembership#enable_pod_tree_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa8cd921ea3bccd5713a7ce72e5d069f79f3e1ef2c002146d20f255cd94856b2)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enable_hierarchical_resource_quota", value=enable_hierarchical_resource_quota, expected_type=type_hints["enable_hierarchical_resource_quota"])
            check_type(argname="argument enable_pod_tree_labels", value=enable_pod_tree_labels, expected_type=type_hints["enable_pod_tree_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_hierarchical_resource_quota is not None:
            self._values["enable_hierarchical_resource_quota"] = enable_hierarchical_resource_quota
        if enable_pod_tree_labels is not None:
            self._values["enable_pod_tree_labels"] = enable_pod_tree_labels

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''**DEPRECATED** Configuring Hierarchy Controller through the configmanagement feature is no longer recommended. Use https://github.com/kubernetes-sigs/hierarchical-namespaces instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_hierarchical_resource_quota(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether hierarchical resource quota is enabled in this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enable_hierarchical_resource_quota GoogleGkeHubFeatureMembership#enable_hierarchical_resource_quota}
        '''
        result = self._values.get("enable_hierarchical_resource_quota")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_pod_tree_labels(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether pod tree labels are enabled in this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enable_pod_tree_labels GoogleGkeHubFeatureMembership#enable_pod_tree_labels}
        '''
        result = self._values.get("enable_pod_tree_labels")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b95d561d2e336ffaff77ab4e4abcd5597bdb153ca78a17a7417abf9193e9c34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEnableHierarchicalResourceQuota")
    def reset_enable_hierarchical_resource_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableHierarchicalResourceQuota", []))

    @jsii.member(jsii_name="resetEnablePodTreeLabels")
    def reset_enable_pod_tree_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePodTreeLabels", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHierarchicalResourceQuotaInput")
    def enable_hierarchical_resource_quota_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHierarchicalResourceQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePodTreeLabelsInput")
    def enable_pod_tree_labels_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePodTreeLabelsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2197ebc77aebabbccb3b8117d0e11c8d5ca89434746a96d6dfb4149aa52a22fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableHierarchicalResourceQuota")
    def enable_hierarchical_resource_quota(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHierarchicalResourceQuota"))

    @enable_hierarchical_resource_quota.setter
    def enable_hierarchical_resource_quota(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c92b3cd9d85efc171ddd92e9f274aa042c8b5919bcb1fcb706263105896271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHierarchicalResourceQuota", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePodTreeLabels")
    def enable_pod_tree_labels(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePodTreeLabels"))

    @enable_pod_tree_labels.setter
    def enable_pod_tree_labels(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db5495bf3427f1eb8f1b60c4064b199b2c1986767d547367c2318f836e47b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePodTreeLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752b4e6199457f99c63eb48bfee9c7bd347d9c7cf04203c4e7dcb5ef3edf0d42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureMembershipConfigmanagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b4f920a39c7b1c45a712235cbffd0082b5858b473f040eef0da90f1f32730f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBinauthz")
    def put_binauthz(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether binauthz is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementBinauthz(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putBinauthz", [value]))

    @jsii.member(jsii_name="putConfigSync")
    def put_config_sync(
        self,
        *,
        deployment_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        git: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit, typing.Dict[builtins.str, typing.Any]]] = None,
        metrics_gcp_service_account_email: typing.Optional[builtins.str] = None,
        oci: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci, typing.Dict[builtins.str, typing.Any]]] = None,
        prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_format: typing.Optional[builtins.str] = None,
        stop_syncing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param deployment_overrides: deployment_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#deployment_overrides GoogleGkeHubFeatureMembership#deployment_overrides}
        :param enabled: Enables the installation of ConfigSync. If set to true, ConfigSync resources will be created and the other ConfigSync fields will be applied if exist. If set to false, all other ConfigSync fields will be ignored, ConfigSync resources will be deleted. If omitted, ConfigSync resources will be managed depends on the presence of the git or oci field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#git GoogleGkeHubFeatureMembership#git}
        :param metrics_gcp_service_account_email: Deprecated: If Workload Identity Federation for GKE is enabled, Google Cloud Service Account is no longer needed for exporting Config Sync metrics: https://cloud.google.com/kubernetes-engine/enterprise/config-sync/docs/how-to/monitor-config-sync-cloud-monitoring#custom-monitoring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#metrics_gcp_service_account_email GoogleGkeHubFeatureMembership#metrics_gcp_service_account_email}
        :param oci: oci block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#oci GoogleGkeHubFeatureMembership#oci}
        :param prevent_drift: Set to true to enable the Config Sync admission webhook to prevent drifts. If set to ``false``, disables the Config Sync admission webhook and does not prevent drifts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#prevent_drift GoogleGkeHubFeatureMembership#prevent_drift}
        :param source_format: Specifies whether the Config Sync Repo is in "hierarchical" or "unstructured" mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#source_format GoogleGkeHubFeatureMembership#source_format}
        :param stop_syncing: Set to true to stop syncing configs for a single cluster. Default: false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#stop_syncing GoogleGkeHubFeatureMembership#stop_syncing}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementConfigSync(
            deployment_overrides=deployment_overrides,
            enabled=enabled,
            git=git,
            metrics_gcp_service_account_email=metrics_gcp_service_account_email,
            oci=oci,
            prevent_drift=prevent_drift,
            source_format=source_format,
            stop_syncing=stop_syncing,
        )

        return typing.cast(None, jsii.invoke(self, "putConfigSync", [value]))

    @jsii.member(jsii_name="putHierarchyController")
    def put_hierarchy_controller(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_hierarchical_resource_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_pod_tree_labels: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: **DEPRECATED** Configuring Hierarchy Controller through the configmanagement feature is no longer recommended. Use https://github.com/kubernetes-sigs/hierarchical-namespaces instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        :param enable_hierarchical_resource_quota: Whether hierarchical resource quota is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enable_hierarchical_resource_quota GoogleGkeHubFeatureMembership#enable_hierarchical_resource_quota}
        :param enable_pod_tree_labels: Whether pod tree labels are enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enable_pod_tree_labels GoogleGkeHubFeatureMembership#enable_pod_tree_labels}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController(
            enabled=enabled,
            enable_hierarchical_resource_quota=enable_hierarchical_resource_quota,
            enable_pod_tree_labels=enable_pod_tree_labels,
        )

        return typing.cast(None, jsii.invoke(self, "putHierarchyController", [value]))

    @jsii.member(jsii_name="putPolicyController")
    def put_policy_controller(
        self,
        *,
        audit_interval_seconds: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        template_library_installed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param audit_interval_seconds: Sets the interval for Policy Controller Audit Scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#audit_interval_seconds GoogleGkeHubFeatureMembership#audit_interval_seconds}
        :param enabled: Enables the installation of Policy Controller. If false, the rest of PolicyController fields take no effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#exemptable_namespaces GoogleGkeHubFeatureMembership#exemptable_namespaces}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#log_denies_enabled GoogleGkeHubFeatureMembership#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#monitoring GoogleGkeHubFeatureMembership#monitoring}
        :param mutation_enabled: Enable or disable mutation in policy controller. If true, mutation CRDs, webhook and controller deployment will be deployed to the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#mutation_enabled GoogleGkeHubFeatureMembership#mutation_enabled}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#referential_rules_enabled GoogleGkeHubFeatureMembership#referential_rules_enabled}
        :param template_library_installed: Installs the default template library along with Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#template_library_installed GoogleGkeHubFeatureMembership#template_library_installed}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementPolicyController(
            audit_interval_seconds=audit_interval_seconds,
            enabled=enabled,
            exemptable_namespaces=exemptable_namespaces,
            log_denies_enabled=log_denies_enabled,
            monitoring=monitoring,
            mutation_enabled=mutation_enabled,
            referential_rules_enabled=referential_rules_enabled,
            template_library_installed=template_library_installed,
        )

        return typing.cast(None, jsii.invoke(self, "putPolicyController", [value]))

    @jsii.member(jsii_name="resetBinauthz")
    def reset_binauthz(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinauthz", []))

    @jsii.member(jsii_name="resetConfigSync")
    def reset_config_sync(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigSync", []))

    @jsii.member(jsii_name="resetHierarchyController")
    def reset_hierarchy_controller(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHierarchyController", []))

    @jsii.member(jsii_name="resetManagement")
    def reset_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagement", []))

    @jsii.member(jsii_name="resetPolicyController")
    def reset_policy_controller(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyController", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="binauthz")
    def binauthz(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementBinauthzOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementBinauthzOutputReference, jsii.get(self, "binauthz"))

    @builtins.property
    @jsii.member(jsii_name="configSync")
    def config_sync(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference, jsii.get(self, "configSync"))

    @builtins.property
    @jsii.member(jsii_name="hierarchyController")
    def hierarchy_controller(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference, jsii.get(self, "hierarchyController"))

    @builtins.property
    @jsii.member(jsii_name="policyController")
    def policy_controller(
        self,
    ) -> "GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference":
        return typing.cast("GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference", jsii.get(self, "policyController"))

    @builtins.property
    @jsii.member(jsii_name="binauthzInput")
    def binauthz_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz], jsii.get(self, "binauthzInput"))

    @builtins.property
    @jsii.member(jsii_name="configSyncInput")
    def config_sync_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync], jsii.get(self, "configSyncInput"))

    @builtins.property
    @jsii.member(jsii_name="hierarchyControllerInput")
    def hierarchy_controller_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController], jsii.get(self, "hierarchyControllerInput"))

    @builtins.property
    @jsii.member(jsii_name="managementInput")
    def management_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managementInput"))

    @builtins.property
    @jsii.member(jsii_name="policyControllerInput")
    def policy_controller_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementPolicyController"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementPolicyController"], jsii.get(self, "policyControllerInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e9ed1242b07ff2a314b428f0630072e67d770f8029051ad7c65c62e15d9c6e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "management", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3bb65c10d9a5d4a130a3fbf44656c5548601ed2e3192c184a5ab253ee3dd47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagement]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba0472bf1aab5e3e538c38efaa57adb346fe186ce6b354a3ad40d47f191762e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementPolicyController",
    jsii_struct_bases=[],
    name_mapping={
        "audit_interval_seconds": "auditIntervalSeconds",
        "enabled": "enabled",
        "exemptable_namespaces": "exemptableNamespaces",
        "log_denies_enabled": "logDeniesEnabled",
        "monitoring": "monitoring",
        "mutation_enabled": "mutationEnabled",
        "referential_rules_enabled": "referentialRulesEnabled",
        "template_library_installed": "templateLibraryInstalled",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagementPolicyController:
    def __init__(
        self,
        *,
        audit_interval_seconds: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        template_library_installed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param audit_interval_seconds: Sets the interval for Policy Controller Audit Scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#audit_interval_seconds GoogleGkeHubFeatureMembership#audit_interval_seconds}
        :param enabled: Enables the installation of Policy Controller. If false, the rest of PolicyController fields take no effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#exemptable_namespaces GoogleGkeHubFeatureMembership#exemptable_namespaces}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#log_denies_enabled GoogleGkeHubFeatureMembership#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#monitoring GoogleGkeHubFeatureMembership#monitoring}
        :param mutation_enabled: Enable or disable mutation in policy controller. If true, mutation CRDs, webhook and controller deployment will be deployed to the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#mutation_enabled GoogleGkeHubFeatureMembership#mutation_enabled}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#referential_rules_enabled GoogleGkeHubFeatureMembership#referential_rules_enabled}
        :param template_library_installed: Installs the default template library along with Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#template_library_installed GoogleGkeHubFeatureMembership#template_library_installed}
        '''
        if isinstance(monitoring, dict):
            monitoring = GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring(**monitoring)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e638940c8c715fbc156b9b6355555ffdf29a8dbafe84a8590b4b2147cf3f148)
            check_type(argname="argument audit_interval_seconds", value=audit_interval_seconds, expected_type=type_hints["audit_interval_seconds"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument exemptable_namespaces", value=exemptable_namespaces, expected_type=type_hints["exemptable_namespaces"])
            check_type(argname="argument log_denies_enabled", value=log_denies_enabled, expected_type=type_hints["log_denies_enabled"])
            check_type(argname="argument monitoring", value=monitoring, expected_type=type_hints["monitoring"])
            check_type(argname="argument mutation_enabled", value=mutation_enabled, expected_type=type_hints["mutation_enabled"])
            check_type(argname="argument referential_rules_enabled", value=referential_rules_enabled, expected_type=type_hints["referential_rules_enabled"])
            check_type(argname="argument template_library_installed", value=template_library_installed, expected_type=type_hints["template_library_installed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audit_interval_seconds is not None:
            self._values["audit_interval_seconds"] = audit_interval_seconds
        if enabled is not None:
            self._values["enabled"] = enabled
        if exemptable_namespaces is not None:
            self._values["exemptable_namespaces"] = exemptable_namespaces
        if log_denies_enabled is not None:
            self._values["log_denies_enabled"] = log_denies_enabled
        if monitoring is not None:
            self._values["monitoring"] = monitoring
        if mutation_enabled is not None:
            self._values["mutation_enabled"] = mutation_enabled
        if referential_rules_enabled is not None:
            self._values["referential_rules_enabled"] = referential_rules_enabled
        if template_library_installed is not None:
            self._values["template_library_installed"] = template_library_installed

    @builtins.property
    def audit_interval_seconds(self) -> typing.Optional[builtins.str]:
        '''Sets the interval for Policy Controller Audit Scans (in seconds). When set to 0, this disables audit functionality altogether.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#audit_interval_seconds GoogleGkeHubFeatureMembership#audit_interval_seconds}
        '''
        result = self._values.get("audit_interval_seconds")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the installation of Policy Controller. If false, the rest of PolicyController fields take no effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exemptable_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of namespaces that are excluded from Policy Controller checks.

        Namespaces do not need to currently exist on the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#exemptable_namespaces GoogleGkeHubFeatureMembership#exemptable_namespaces}
        '''
        result = self._values.get("exemptable_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def log_denies_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Logs all denies and dry run failures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#log_denies_enabled GoogleGkeHubFeatureMembership#log_denies_enabled}
        '''
        result = self._values.get("log_denies_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monitoring(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring"]:
        '''monitoring block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#monitoring GoogleGkeHubFeatureMembership#monitoring}
        '''
        result = self._values.get("monitoring")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring"], result)

    @builtins.property
    def mutation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable mutation in policy controller.

        If true, mutation CRDs, webhook and controller deployment will be deployed to the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#mutation_enabled GoogleGkeHubFeatureMembership#mutation_enabled}
        '''
        result = self._values.get("mutation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def referential_rules_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#referential_rules_enabled GoogleGkeHubFeatureMembership#referential_rules_enabled}
        '''
        result = self._values.get("referential_rules_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def template_library_installed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Installs the default template library along with Policy Controller.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#template_library_installed GoogleGkeHubFeatureMembership#template_library_installed}
        '''
        result = self._values.get("template_library_installed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementPolicyController(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring",
    jsii_struct_bases=[],
    name_mapping={"backends": "backends"},
)
class GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring:
    def __init__(
        self,
        *,
        backends: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param backends: Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#backends GoogleGkeHubFeatureMembership#backends}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c46b4eed8b3413d8a103dc814d01a3a1e8910f46d714d75809d0ca0523497962)
            check_type(argname="argument backends", value=backends, expected_type=type_hints["backends"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backends is not None:
            self._values["backends"] = backends

    @builtins.property
    def backends(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#backends GoogleGkeHubFeatureMembership#backends}
        '''
        result = self._values.get("backends")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2828c9499ab339bd608500255c84bcfd7fd04f31afaddbdbe646da4aa14e5046)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08114d8c1874c0b70da8028a3219f781ab9475f10d7e8de9227925615bd09f75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backends", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56aae9e90a6d26a7fd64323d3d1ea5dac4645f6b63fd85eaf34c9ca2572625fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d01a6308da6a2ea089b19c438f90175ae8e7723c5eb3c027bedb9de60b7c2d1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMonitoring")
    def put_monitoring(
        self,
        *,
        backends: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param backends: Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#backends GoogleGkeHubFeatureMembership#backends}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring(
            backends=backends
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoring", [value]))

    @jsii.member(jsii_name="resetAuditIntervalSeconds")
    def reset_audit_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuditIntervalSeconds", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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

    @jsii.member(jsii_name="resetReferentialRulesEnabled")
    def reset_referential_rules_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferentialRulesEnabled", []))

    @jsii.member(jsii_name="resetTemplateLibraryInstalled")
    def reset_template_library_installed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateLibraryInstalled", []))

    @builtins.property
    @jsii.member(jsii_name="monitoring")
    def monitoring(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference, jsii.get(self, "monitoring"))

    @builtins.property
    @jsii.member(jsii_name="auditIntervalSecondsInput")
    def audit_interval_seconds_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "auditIntervalSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="exemptableNamespacesInput")
    def exemptable_namespaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exemptableNamespacesInput"))

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
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring], jsii.get(self, "monitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="mutationEnabledInput")
    def mutation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mutationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="referentialRulesEnabledInput")
    def referential_rules_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "referentialRulesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="templateLibraryInstalledInput")
    def template_library_installed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "templateLibraryInstalledInput"))

    @builtins.property
    @jsii.member(jsii_name="auditIntervalSeconds")
    def audit_interval_seconds(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "auditIntervalSeconds"))

    @audit_interval_seconds.setter
    def audit_interval_seconds(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f6bd92abe8eda74a1dc751933ccc9f78e8709b1f4e4280dca9f6d1f33712181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auditIntervalSeconds", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__07510763f8e532dc8cd31e94f893b0d360a679d33a1a80d195a7dbd6384181e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exemptableNamespaces")
    def exemptable_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exemptableNamespaces"))

    @exemptable_namespaces.setter
    def exemptable_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb109ff29bbfd1e2769227f6f49ff3799f8e4b6b6fe60602c98096cbacdf1d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exemptableNamespaces", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__bdf4e7fef3f5b42771685f38994fc5b6b15f94ef04791fb108714f466ea1e454)
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
            type_hints = typing.get_type_hints(_typecheckingstub__969da8e1b8fe0675c96fb33e5b7b1ebc7b4f232aa2dc6c37060c2779fac5cd67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43448b9f005e2e7d89e24f3359225cd8c2ada459f7a6525b1daf8fc31bb3d341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referentialRulesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateLibraryInstalled")
    def template_library_installed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "templateLibraryInstalled"))

    @template_library_installed.setter
    def template_library_installed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e39b1e0b78621b7cc569d326f553aa1e47d9e8a7d1fbf024c24e100b04f57c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateLibraryInstalled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyController]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyController], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyController],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2481b1b520b71b8e2947e25b676f3a045438237afb75341ccf06fc510c022778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipMesh",
    jsii_struct_bases=[],
    name_mapping={"control_plane": "controlPlane", "management": "management"},
)
class GoogleGkeHubFeatureMembershipMesh:
    def __init__(
        self,
        *,
        control_plane: typing.Optional[builtins.str] = None,
        management: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control_plane: **DEPRECATED** Whether to automatically manage Service Mesh control planes. Possible values: CONTROL_PLANE_MANAGEMENT_UNSPECIFIED, AUTOMATIC, MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#control_plane GoogleGkeHubFeatureMembership#control_plane}
        :param management: Whether to automatically manage Service Mesh. Possible values: MANAGEMENT_UNSPECIFIED, MANAGEMENT_AUTOMATIC, MANAGEMENT_MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#management GoogleGkeHubFeatureMembership#management}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35e02410be6366371ef684ffe9ad2f718f113946d1bc8b099a10b00600d23a1f)
            check_type(argname="argument control_plane", value=control_plane, expected_type=type_hints["control_plane"])
            check_type(argname="argument management", value=management, expected_type=type_hints["management"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if control_plane is not None:
            self._values["control_plane"] = control_plane
        if management is not None:
            self._values["management"] = management

    @builtins.property
    def control_plane(self) -> typing.Optional[builtins.str]:
        '''**DEPRECATED** Whether to automatically manage Service Mesh control planes. Possible values: CONTROL_PLANE_MANAGEMENT_UNSPECIFIED, AUTOMATIC, MANUAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#control_plane GoogleGkeHubFeatureMembership#control_plane}
        '''
        result = self._values.get("control_plane")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def management(self) -> typing.Optional[builtins.str]:
        '''Whether to automatically manage Service Mesh. Possible values: MANAGEMENT_UNSPECIFIED, MANAGEMENT_AUTOMATIC, MANAGEMENT_MANUAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#management GoogleGkeHubFeatureMembership#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipMesh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipMeshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipMeshOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb914b84ea122ed7e2712b07b2d9c9dc3377791756040d6200068806301255a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetControlPlane")
    def reset_control_plane(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlane", []))

    @jsii.member(jsii_name="resetManagement")
    def reset_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagement", []))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInput")
    def control_plane_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlPlaneInput"))

    @builtins.property
    @jsii.member(jsii_name="managementInput")
    def management_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managementInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlane")
    def control_plane(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlane"))

    @control_plane.setter
    def control_plane(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31b4aa8e522d7506c6d54156d51c99d9ae3748fbd75621af8ac842067742c71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlane", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "management"))

    @management.setter
    def management(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b460959e6130a0c71d2f8528cb9c26edf5ce367d138d479c25b81755396e4188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "management", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeHubFeatureMembershipMesh]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipMesh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipMesh],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c6346e3d79f710d4f7a24211fe3f852ca4f2bee64a5ddec97aa54abd564be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontroller",
    jsii_struct_bases=[],
    name_mapping={
        "policy_controller_hub_config": "policyControllerHubConfig",
        "version": "version",
    },
)
class GoogleGkeHubFeatureMembershipPolicycontroller:
    def __init__(
        self,
        *,
        policy_controller_hub_config: typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig", typing.Dict[builtins.str, typing.Any]],
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param policy_controller_hub_config: policy_controller_hub_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_controller_hub_config GoogleGkeHubFeatureMembership#policy_controller_hub_config}
        :param version: Optional. Version of Policy Controller to install. Defaults to the latest version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#version GoogleGkeHubFeatureMembership#version}
        '''
        if isinstance(policy_controller_hub_config, dict):
            policy_controller_hub_config = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig(**policy_controller_hub_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdc574274da9fff76ede7119f148b2fe03e9e13b27729e8ce1fc8221ddf18e13)
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
    ) -> "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig":
        '''policy_controller_hub_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_controller_hub_config GoogleGkeHubFeatureMembership#policy_controller_hub_config}
        '''
        result = self._values.get("policy_controller_hub_config")
        assert result is not None, "Required property 'policy_controller_hub_config' is missing"
        return typing.cast("GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig", result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Optional. Version of Policy Controller to install. Defaults to the latest version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#version GoogleGkeHubFeatureMembership#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipPolicycontroller(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipPolicycontrollerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538924dd1464055bf5738b2d324f68fcd218aec40de03bb2b5f999af89040d38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPolicyControllerHubConfig")
    def put_policy_controller_hub_config(
        self,
        *,
        audit_interval_seconds: typing.Optional[jsii.Number] = None,
        constraint_violation_limit: typing.Optional[jsii.Number] = None,
        deployment_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        install_spec: typing.Optional[builtins.str] = None,
        log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_content: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent", typing.Dict[builtins.str, typing.Any]]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param audit_interval_seconds: Sets the interval for Policy Controller Audit Scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#audit_interval_seconds GoogleGkeHubFeatureMembership#audit_interval_seconds}
        :param constraint_violation_limit: The maximum number of audit violations to be stored in a constraint. If not set, the internal default of 20 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#constraint_violation_limit GoogleGkeHubFeatureMembership#constraint_violation_limit}
        :param deployment_configs: deployment_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#deployment_configs GoogleGkeHubFeatureMembership#deployment_configs}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#exemptable_namespaces GoogleGkeHubFeatureMembership#exemptable_namespaces}
        :param install_spec: Configures the mode of the Policy Controller installation. Possible values: INSTALL_SPEC_UNSPECIFIED, INSTALL_SPEC_NOT_INSTALLED, INSTALL_SPEC_ENABLED, INSTALL_SPEC_SUSPENDED, INSTALL_SPEC_DETACHED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#install_spec GoogleGkeHubFeatureMembership#install_spec}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#log_denies_enabled GoogleGkeHubFeatureMembership#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#monitoring GoogleGkeHubFeatureMembership#monitoring}
        :param mutation_enabled: Enables the ability to mutate resources using Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#mutation_enabled GoogleGkeHubFeatureMembership#mutation_enabled}
        :param policy_content: policy_content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_content GoogleGkeHubFeatureMembership#policy_content}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#referential_rules_enabled GoogleGkeHubFeatureMembership#referential_rules_enabled}
        '''
        value = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig(
            audit_interval_seconds=audit_interval_seconds,
            constraint_violation_limit=constraint_violation_limit,
            deployment_configs=deployment_configs,
            exemptable_namespaces=exemptable_namespaces,
            install_spec=install_spec,
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
    ) -> "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigOutputReference":
        return typing.cast("GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigOutputReference", jsii.get(self, "policyControllerHubConfig"))

    @builtins.property
    @jsii.member(jsii_name="policyControllerHubConfigInput")
    def policy_controller_hub_config_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig"], jsii.get(self, "policyControllerHubConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fbeb96eab6aded586b77803bc1868880ef65e5273e17790207ecd3284ff13ecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipPolicycontroller]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipPolicycontroller], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontroller],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b9974b3365c5f530aae0d04e8568597ecb795e1644d2ae16035225eb5d1c34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig",
    jsii_struct_bases=[],
    name_mapping={
        "audit_interval_seconds": "auditIntervalSeconds",
        "constraint_violation_limit": "constraintViolationLimit",
        "deployment_configs": "deploymentConfigs",
        "exemptable_namespaces": "exemptableNamespaces",
        "install_spec": "installSpec",
        "log_denies_enabled": "logDeniesEnabled",
        "monitoring": "monitoring",
        "mutation_enabled": "mutationEnabled",
        "policy_content": "policyContent",
        "referential_rules_enabled": "referentialRulesEnabled",
    },
)
class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig:
    def __init__(
        self,
        *,
        audit_interval_seconds: typing.Optional[jsii.Number] = None,
        constraint_violation_limit: typing.Optional[jsii.Number] = None,
        deployment_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        install_spec: typing.Optional[builtins.str] = None,
        log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_content: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent", typing.Dict[builtins.str, typing.Any]]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param audit_interval_seconds: Sets the interval for Policy Controller Audit Scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#audit_interval_seconds GoogleGkeHubFeatureMembership#audit_interval_seconds}
        :param constraint_violation_limit: The maximum number of audit violations to be stored in a constraint. If not set, the internal default of 20 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#constraint_violation_limit GoogleGkeHubFeatureMembership#constraint_violation_limit}
        :param deployment_configs: deployment_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#deployment_configs GoogleGkeHubFeatureMembership#deployment_configs}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#exemptable_namespaces GoogleGkeHubFeatureMembership#exemptable_namespaces}
        :param install_spec: Configures the mode of the Policy Controller installation. Possible values: INSTALL_SPEC_UNSPECIFIED, INSTALL_SPEC_NOT_INSTALLED, INSTALL_SPEC_ENABLED, INSTALL_SPEC_SUSPENDED, INSTALL_SPEC_DETACHED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#install_spec GoogleGkeHubFeatureMembership#install_spec}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#log_denies_enabled GoogleGkeHubFeatureMembership#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#monitoring GoogleGkeHubFeatureMembership#monitoring}
        :param mutation_enabled: Enables the ability to mutate resources using Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#mutation_enabled GoogleGkeHubFeatureMembership#mutation_enabled}
        :param policy_content: policy_content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_content GoogleGkeHubFeatureMembership#policy_content}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#referential_rules_enabled GoogleGkeHubFeatureMembership#referential_rules_enabled}
        '''
        if isinstance(monitoring, dict):
            monitoring = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring(**monitoring)
        if isinstance(policy_content, dict):
            policy_content = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent(**policy_content)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e001413611735258210195e4a2c30760be6ea81c77169948ef39c486a02d10)
            check_type(argname="argument audit_interval_seconds", value=audit_interval_seconds, expected_type=type_hints["audit_interval_seconds"])
            check_type(argname="argument constraint_violation_limit", value=constraint_violation_limit, expected_type=type_hints["constraint_violation_limit"])
            check_type(argname="argument deployment_configs", value=deployment_configs, expected_type=type_hints["deployment_configs"])
            check_type(argname="argument exemptable_namespaces", value=exemptable_namespaces, expected_type=type_hints["exemptable_namespaces"])
            check_type(argname="argument install_spec", value=install_spec, expected_type=type_hints["install_spec"])
            check_type(argname="argument log_denies_enabled", value=log_denies_enabled, expected_type=type_hints["log_denies_enabled"])
            check_type(argname="argument monitoring", value=monitoring, expected_type=type_hints["monitoring"])
            check_type(argname="argument mutation_enabled", value=mutation_enabled, expected_type=type_hints["mutation_enabled"])
            check_type(argname="argument policy_content", value=policy_content, expected_type=type_hints["policy_content"])
            check_type(argname="argument referential_rules_enabled", value=referential_rules_enabled, expected_type=type_hints["referential_rules_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audit_interval_seconds is not None:
            self._values["audit_interval_seconds"] = audit_interval_seconds
        if constraint_violation_limit is not None:
            self._values["constraint_violation_limit"] = constraint_violation_limit
        if deployment_configs is not None:
            self._values["deployment_configs"] = deployment_configs
        if exemptable_namespaces is not None:
            self._values["exemptable_namespaces"] = exemptable_namespaces
        if install_spec is not None:
            self._values["install_spec"] = install_spec
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
    def audit_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''Sets the interval for Policy Controller Audit Scans (in seconds). When set to 0, this disables audit functionality altogether.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#audit_interval_seconds GoogleGkeHubFeatureMembership#audit_interval_seconds}
        '''
        result = self._values.get("audit_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def constraint_violation_limit(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of audit violations to be stored in a constraint.

        If not set, the internal default of 20 will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#constraint_violation_limit GoogleGkeHubFeatureMembership#constraint_violation_limit}
        '''
        result = self._values.get("constraint_violation_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def deployment_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs"]]]:
        '''deployment_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#deployment_configs GoogleGkeHubFeatureMembership#deployment_configs}
        '''
        result = self._values.get("deployment_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs"]]], result)

    @builtins.property
    def exemptable_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of namespaces that are excluded from Policy Controller checks.

        Namespaces do not need to currently exist on the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#exemptable_namespaces GoogleGkeHubFeatureMembership#exemptable_namespaces}
        '''
        result = self._values.get("exemptable_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def install_spec(self) -> typing.Optional[builtins.str]:
        '''Configures the mode of the Policy Controller installation. Possible values: INSTALL_SPEC_UNSPECIFIED, INSTALL_SPEC_NOT_INSTALLED, INSTALL_SPEC_ENABLED, INSTALL_SPEC_SUSPENDED, INSTALL_SPEC_DETACHED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#install_spec GoogleGkeHubFeatureMembership#install_spec}
        '''
        result = self._values.get("install_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_denies_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Logs all denies and dry run failures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#log_denies_enabled GoogleGkeHubFeatureMembership#log_denies_enabled}
        '''
        result = self._values.get("log_denies_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monitoring(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring"]:
        '''monitoring block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#monitoring GoogleGkeHubFeatureMembership#monitoring}
        '''
        result = self._values.get("monitoring")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring"], result)

    @builtins.property
    def mutation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the ability to mutate resources using Policy Controller.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#mutation_enabled GoogleGkeHubFeatureMembership#mutation_enabled}
        '''
        result = self._values.get("mutation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def policy_content(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent"]:
        '''policy_content block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#policy_content GoogleGkeHubFeatureMembership#policy_content}
        '''
        result = self._values.get("policy_content")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent"], result)

    @builtins.property
    def referential_rules_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#referential_rules_enabled GoogleGkeHubFeatureMembership#referential_rules_enabled}
        '''
        result = self._values.get("referential_rules_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "component_name": "componentName",
        "container_resources": "containerResources",
        "pod_affinity": "podAffinity",
        "pod_tolerations": "podTolerations",
        "replica_count": "replicaCount",
    },
)
class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs:
    def __init__(
        self,
        *,
        component_name: builtins.str,
        container_resources: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources", typing.Dict[builtins.str, typing.Any]]] = None,
        pod_affinity: typing.Optional[builtins.str] = None,
        pod_tolerations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param component_name: The name for the key in the map for which this object is mapped to in the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#component_name GoogleGkeHubFeatureMembership#component_name}
        :param container_resources: container_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#container_resources GoogleGkeHubFeatureMembership#container_resources}
        :param pod_affinity: Pod affinity configuration. Possible values: AFFINITY_UNSPECIFIED, NO_AFFINITY, ANTI_AFFINITY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#pod_affinity GoogleGkeHubFeatureMembership#pod_affinity}
        :param pod_tolerations: pod_tolerations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#pod_tolerations GoogleGkeHubFeatureMembership#pod_tolerations}
        :param replica_count: Pod replica count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#replica_count GoogleGkeHubFeatureMembership#replica_count}
        '''
        if isinstance(container_resources, dict):
            container_resources = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources(**container_resources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d8a7ebe422b4d857b23b651b53fbd5f36e80d1cef9e5124155b1d7ca21d679)
            check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
            check_type(argname="argument container_resources", value=container_resources, expected_type=type_hints["container_resources"])
            check_type(argname="argument pod_affinity", value=pod_affinity, expected_type=type_hints["pod_affinity"])
            check_type(argname="argument pod_tolerations", value=pod_tolerations, expected_type=type_hints["pod_tolerations"])
            check_type(argname="argument replica_count", value=replica_count, expected_type=type_hints["replica_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "component_name": component_name,
        }
        if container_resources is not None:
            self._values["container_resources"] = container_resources
        if pod_affinity is not None:
            self._values["pod_affinity"] = pod_affinity
        if pod_tolerations is not None:
            self._values["pod_tolerations"] = pod_tolerations
        if replica_count is not None:
            self._values["replica_count"] = replica_count

    @builtins.property
    def component_name(self) -> builtins.str:
        '''The name for the key in the map for which this object is mapped to in the API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#component_name GoogleGkeHubFeatureMembership#component_name}
        '''
        result = self._values.get("component_name")
        assert result is not None, "Required property 'component_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_resources(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources"]:
        '''container_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#container_resources GoogleGkeHubFeatureMembership#container_resources}
        '''
        result = self._values.get("container_resources")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources"], result)

    @builtins.property
    def pod_affinity(self) -> typing.Optional[builtins.str]:
        '''Pod affinity configuration. Possible values: AFFINITY_UNSPECIFIED, NO_AFFINITY, ANTI_AFFINITY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#pod_affinity GoogleGkeHubFeatureMembership#pod_affinity}
        '''
        result = self._values.get("pod_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_tolerations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations"]]]:
        '''pod_tolerations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#pod_tolerations GoogleGkeHubFeatureMembership#pod_tolerations}
        '''
        result = self._values.get("pod_tolerations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations"]]], result)

    @builtins.property
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''Pod replica count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#replica_count GoogleGkeHubFeatureMembership#replica_count}
        '''
        result = self._values.get("replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources",
    jsii_struct_bases=[],
    name_mapping={"limits": "limits", "requests": "requests"},
)
class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources:
    def __init__(
        self,
        *,
        limits: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        requests: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#limits GoogleGkeHubFeatureMembership#limits}
        :param requests: requests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#requests GoogleGkeHubFeatureMembership#requests}
        '''
        if isinstance(limits, dict):
            limits = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits(**limits)
        if isinstance(requests, dict):
            requests = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests(**requests)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f426ede36cc1088caa05765ada27c2481c20bed2e818d241957a88f5c179d565)
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
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits"]:
        '''limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#limits GoogleGkeHubFeatureMembership#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits"], result)

    @builtins.property
    def requests(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"]:
        '''requests block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#requests GoogleGkeHubFeatureMembership#requests}
        '''
        result = self._values.get("requests")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory"},
)
class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#cpu GoogleGkeHubFeatureMembership#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#memory GoogleGkeHubFeatureMembership#memory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8a2414f1aa082dd9312ce7ca515f87759030b06a19faa80384fe41eba22973c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#cpu GoogleGkeHubFeatureMembership#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Memory requirement expressed in Kubernetes resource units.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#memory GoogleGkeHubFeatureMembership#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b187e9b3f620e39859fa3654eb142d3c0921caea399e4509261b52bce79d2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50fab6f090331c4e6163b8d5f53741d71fb01788cec8b51601842b141338c117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc9574fcc0feee41f0146af56ae957179596e3ab531207c5a9b073a54af527e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f74cf1ced27dfeb16620c7283d41c0a35dd50bd1446d4f291f4533ba8f7bf975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79bd9087d68eac051d174f6c17c522f46f479d42c3f9a8032d688ae493596cb5)
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
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#cpu GoogleGkeHubFeatureMembership#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#memory GoogleGkeHubFeatureMembership#memory}
        '''
        value = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits(
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
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#cpu GoogleGkeHubFeatureMembership#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#memory GoogleGkeHubFeatureMembership#memory}
        '''
        value = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests(
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
    ) -> GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference, jsii.get(self, "limits"))

    @builtins.property
    @jsii.member(jsii_name="requests")
    def requests(
        self,
    ) -> "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference":
        return typing.cast("GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference", jsii.get(self, "requests"))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="requestsInput")
    def requests_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"], jsii.get(self, "requestsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a42ace71451c7412fc347b2f6e806045dfa092f2a85a0efcd602cd07981eec2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory"},
)
class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#cpu GoogleGkeHubFeatureMembership#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#memory GoogleGkeHubFeatureMembership#memory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c719305f0aa26722a81bfd7126e3134b1ded4dca1b6c07779dfae14deceb10ba)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#cpu GoogleGkeHubFeatureMembership#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Memory requirement expressed in Kubernetes resource units.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#memory GoogleGkeHubFeatureMembership#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1339ae2d35a21e2849ff2eb12b23fa210edb0e657a670ad8ecb19c8d0cca329)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63c6d63a449b8fecd1b031c64ed98c3e7c1c9774f10cd4c53e5f76b92cf45690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__259f536e852ceb447bacdaa629f25af93901c7218cef6f83a767b5cdffaa7faa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ee26a94c6559c8d3ffd4dbb47b20f9c38abc22562289b35dac46e7a6f70a92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bf1426ee90d5df02bbffb1a965f296c48b98c71268adc6f484564208df95d3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4885fba9f7a90a87cbdcd72388ef0a5f52b75621f9df76e073f2ca317800c63c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697559b1487febd9ff36ac3b24cb17a48b06bd2e8c2e5247cdf2817591cbbb4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2612e38c78fef49139e13d48e71486c8fc46571c4a620ab43bc8699dbbdc5679)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9a6221c180578f5ca069881d22d7fd0e676f2a53547d3393932b3338c1acdd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8913dd86d91d22fc5690503256ca7e8fb9bc615292090268927f9ba360c4c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8004c71ec8772b4c80eca7ac22946b103ecf9d8d72b127d956d39c229b46786)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putContainerResources")
    def put_container_resources(
        self,
        *,
        limits: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits, typing.Dict[builtins.str, typing.Any]]] = None,
        requests: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#limits GoogleGkeHubFeatureMembership#limits}
        :param requests: requests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#requests GoogleGkeHubFeatureMembership#requests}
        '''
        value = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources(
            limits=limits, requests=requests
        )

        return typing.cast(None, jsii.invoke(self, "putContainerResources", [value]))

    @jsii.member(jsii_name="putPodTolerations")
    def put_pod_tolerations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d3d67581e7a9a8880e7bbcfe5ad8acdf3f442829a06c7176dccf7429775274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPodTolerations", [value]))

    @jsii.member(jsii_name="resetContainerResources")
    def reset_container_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerResources", []))

    @jsii.member(jsii_name="resetPodAffinity")
    def reset_pod_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodAffinity", []))

    @jsii.member(jsii_name="resetPodTolerations")
    def reset_pod_tolerations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodTolerations", []))

    @jsii.member(jsii_name="resetReplicaCount")
    def reset_replica_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaCount", []))

    @builtins.property
    @jsii.member(jsii_name="containerResources")
    def container_resources(
        self,
    ) -> GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference, jsii.get(self, "containerResources"))

    @builtins.property
    @jsii.member(jsii_name="podTolerations")
    def pod_tolerations(
        self,
    ) -> "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsList":
        return typing.cast("GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsList", jsii.get(self, "podTolerations"))

    @builtins.property
    @jsii.member(jsii_name="componentNameInput")
    def component_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "componentNameInput"))

    @builtins.property
    @jsii.member(jsii_name="containerResourcesInput")
    def container_resources_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources], jsii.get(self, "containerResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="podAffinityInput")
    def pod_affinity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="podTolerationsInput")
    def pod_tolerations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations"]]], jsii.get(self, "podTolerationsInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaCountInput")
    def replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="componentName")
    def component_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "componentName"))

    @component_name.setter
    def component_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6c4e54a2a5e68b435eadfe5ed63be38a27e684a79debeb7230fd860265f36d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podAffinity")
    def pod_affinity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podAffinity"))

    @pod_affinity.setter
    def pod_affinity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e4093c0665876b37c901143060d4a53fa988522438f093252d9865a30a6530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaCount")
    def replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCount"))

    @replica_count.setter
    def replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ec7d8de6df38052c6e0e9f49633490164513acc4fba0453bddd41ba3556579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cadf8ca27708c5502c622fe9d4bf4d69dfe07aafd38f47b37b62190c6cddcd52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations",
    jsii_struct_bases=[],
    name_mapping={
        "effect": "effect",
        "key": "key",
        "operator": "operator",
        "value": "value",
    },
)
class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations:
    def __init__(
        self,
        *,
        effect: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Matches a taint effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#effect GoogleGkeHubFeatureMembership#effect}
        :param key: Matches a taint key (not necessarily unique). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#key GoogleGkeHubFeatureMembership#key}
        :param operator: Matches a taint operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#operator GoogleGkeHubFeatureMembership#operator}
        :param value: Matches a taint value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#value GoogleGkeHubFeatureMembership#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997643aefc2ec0dfc62c3a4c2edfb4d99cbd388196ff627946726a9c8a505538)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#effect GoogleGkeHubFeatureMembership#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Matches a taint key (not necessarily unique).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#key GoogleGkeHubFeatureMembership#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Matches a taint operator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#operator GoogleGkeHubFeatureMembership#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Matches a taint value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#value GoogleGkeHubFeatureMembership#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bde608202f17193aefe815a7303000caeeb1aa32e8b1d78363b9db926704c1f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7313f8741a6f84859d438852df408383a631b5b8024cee3f2f605b7417d452)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d301745833f3c097ac8fb9360cb34b14bb6bec8b2e8c1d6f0891561cc20538f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40f153fcd0e0288875961d59d647318eb425fee2e8f3440af85bc3294ab1a215)
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
            type_hints = typing.get_type_hints(_typecheckingstub__634dba8256442d6691b2b11a3a2209bc059267657c1271c5be4857f446924efa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264045e1e20a577615054cbb792686b77cc0437badc33dbec2c5d17a26491d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8587b2495c535138dd7a94001c49625d2f55ba0b82a0314b232c9123f3c38230)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9299f67685f0c0e33c952397c6b47767e6541bfc4671363ddb1de995d2a159f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44acf298d3c9957ff73359ae8ea73a5f7581eee747f5567e8e2fba1b61326592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0cb6243d2a39213773901c9f46f4b621c7c0e380a992e9ada41dd25da2c94a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6efd0e4984ba0d91aae208bc467f6734d1915ca28753b913568e0bcb85b5024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef7070e3d3465b4f9633c155489afb2ddba21b9e62a886842eb6cab54e5786a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring",
    jsii_struct_bases=[],
    name_mapping={"backends": "backends"},
)
class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring:
    def __init__(
        self,
        *,
        backends: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param backends: Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#backends GoogleGkeHubFeatureMembership#backends}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc934eb7161ce2c8c7a6ceec95b3def20a4c229e53aac9364760ddd6cacfec8)
            check_type(argname="argument backends", value=backends, expected_type=type_hints["backends"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backends is not None:
            self._values["backends"] = backends

    @builtins.property
    def backends(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#backends GoogleGkeHubFeatureMembership#backends}
        '''
        result = self._values.get("backends")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f50b7d0654263b0a0f0c3db2c6c649a762b3990b939e2a6a20ec992c3b23c1b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__352b284852be561143839d59966c7c7a4bc57d1f2770bb76c909c1043bce43bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backends", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9b5155d64618ea53426de993d7c1025a06cefe3b16e31aff87a38e3d1470824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f6eeda859597129b1369c2c4f0dcabbe4ec7a892a2a723ccc154e3df5724ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeploymentConfigs")
    def put_deployment_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbbca61360b0837eb2a8bf3b967d4e3513588358d41fa612e34b7b95fe505da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeploymentConfigs", [value]))

    @jsii.member(jsii_name="putMonitoring")
    def put_monitoring(
        self,
        *,
        backends: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param backends: Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#backends GoogleGkeHubFeatureMembership#backends}
        '''
        value = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring(
            backends=backends
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoring", [value]))

    @jsii.member(jsii_name="putPolicyContent")
    def put_policy_content(
        self,
        *,
        bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        template_library: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bundles: bundles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#bundles GoogleGkeHubFeatureMembership#bundles}
        :param template_library: template_library block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#template_library GoogleGkeHubFeatureMembership#template_library}
        '''
        value = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent(
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

    @jsii.member(jsii_name="resetInstallSpec")
    def reset_install_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstallSpec", []))

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
    ) -> GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList:
        return typing.cast(GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList, jsii.get(self, "deploymentConfigs"))

    @builtins.property
    @jsii.member(jsii_name="monitoring")
    def monitoring(
        self,
    ) -> GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference, jsii.get(self, "monitoring"))

    @builtins.property
    @jsii.member(jsii_name="policyContent")
    def policy_content(
        self,
    ) -> "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference":
        return typing.cast("GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference", jsii.get(self, "policyContent"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]], jsii.get(self, "deploymentConfigsInput"))

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
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring], jsii.get(self, "monitoringInput"))

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
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent"], jsii.get(self, "policyContentInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2227be24e2ac9350b31d73dc78059d38d013d22cb634225d22970c58b6f15101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auditIntervalSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="constraintViolationLimit")
    def constraint_violation_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "constraintViolationLimit"))

    @constraint_violation_limit.setter
    def constraint_violation_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e9885d8dcdbde902b03c8e8c8a8bbf35ee5ce6535d16d0208e068962807c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constraintViolationLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exemptableNamespaces")
    def exemptable_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exemptableNamespaces"))

    @exemptable_namespaces.setter
    def exemptable_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1112831fed83328b51d24c407feda01fafbfacf59128b0f978141e11b4b5ce10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exemptableNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="installSpec")
    def install_spec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "installSpec"))

    @install_spec.setter
    def install_spec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86399577fb2aac237d60576214573be1048a6a9aaca2d760a305fca79c51661f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e1f0bc8a59e4b3da4fab1311901804a83cc972c4693947e1e150741d75ecb8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74f23736d489ebbcc1405fac65b02dd18eacfa978b465f806ea8ae606fe79e14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30f44d80f82be3699d7bdc360115b052496587480743c754d740ffec5f50114a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referentialRulesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4bc7e9c68203dd803a8396c08a29aa825782a6f048b8a942731c3c79db0b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent",
    jsii_struct_bases=[],
    name_mapping={"bundles": "bundles", "template_library": "templateLibrary"},
)
class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent:
    def __init__(
        self,
        *,
        bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        template_library: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bundles: bundles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#bundles GoogleGkeHubFeatureMembership#bundles}
        :param template_library: template_library block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#template_library GoogleGkeHubFeatureMembership#template_library}
        '''
        if isinstance(template_library, dict):
            template_library = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary(**template_library)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec868d81697343f300ef9bccee72f379198a06900af16723fe79705c47e42e63)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles"]]]:
        '''bundles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#bundles GoogleGkeHubFeatureMembership#bundles}
        '''
        result = self._values.get("bundles")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles"]]], result)

    @builtins.property
    def template_library(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"]:
        '''template_library block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#template_library GoogleGkeHubFeatureMembership#template_library}
        '''
        result = self._values.get("template_library")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles",
    jsii_struct_bases=[],
    name_mapping={
        "bundle_name": "bundleName",
        "exempted_namespaces": "exemptedNamespaces",
    },
)
class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles:
    def __init__(
        self,
        *,
        bundle_name: builtins.str,
        exempted_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bundle_name: The name for the key in the map for which this object is mapped to in the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#bundle_name GoogleGkeHubFeatureMembership#bundle_name}
        :param exempted_namespaces: The set of namespaces to be exempted from the bundle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#exempted_namespaces GoogleGkeHubFeatureMembership#exempted_namespaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5325efcc11d9eef79d719e375ba11f8d3d09111bc7e2e2f03ab18fbcafb3af3)
            check_type(argname="argument bundle_name", value=bundle_name, expected_type=type_hints["bundle_name"])
            check_type(argname="argument exempted_namespaces", value=exempted_namespaces, expected_type=type_hints["exempted_namespaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bundle_name": bundle_name,
        }
        if exempted_namespaces is not None:
            self._values["exempted_namespaces"] = exempted_namespaces

    @builtins.property
    def bundle_name(self) -> builtins.str:
        '''The name for the key in the map for which this object is mapped to in the API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#bundle_name GoogleGkeHubFeatureMembership#bundle_name}
        '''
        result = self._values.get("bundle_name")
        assert result is not None, "Required property 'bundle_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exempted_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of namespaces to be exempted from the bundle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#exempted_namespaces GoogleGkeHubFeatureMembership#exempted_namespaces}
        '''
        result = self._values.get("exempted_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf0efd019bc73a99b8001f6cfc39080a74846362bb35435d2ce5cb7a843e1887)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0e0a5d073e5b326467b1df0e5b21173fe98c69667d81fba118e385941bae6e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be251736b888b3862eeae37babf350b6ef9dbbdf33366fd6197ebabb0919d88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fecbf2ac8c30f5d8377f0661b20078576b7e245f15d9187135a2c2579a306420)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2f686781c283da4bfd751b3fd3eb781200c12dcd7e774b0db7072fbb3b3d872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2bd91cdd95cd0981119c11ba4d1900ccb38d0839577e1de265ace2a7017d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78260af711849087d6c0a8504cfd4532f4897ec416168d6ceec20360a7fa22bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExemptedNamespaces")
    def reset_exempted_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExemptedNamespaces", []))

    @builtins.property
    @jsii.member(jsii_name="bundleNameInput")
    def bundle_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bundleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="exemptedNamespacesInput")
    def exempted_namespaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exemptedNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="bundleName")
    def bundle_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bundleName"))

    @bundle_name.setter
    def bundle_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0cb4a01edc7fe73a65e64ea259cabdde2ebe4cd69648a0c9177f85f0d5dd70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exemptedNamespaces")
    def exempted_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exemptedNamespaces"))

    @exempted_namespaces.setter
    def exempted_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f140041b8380d62c28633b7c46d4e585dfc0d75990c99a175482e73267133cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exemptedNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1096a07909601635776f36f9158c40052d063701433ff19fbfc0302b5c555c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050d37ff3221737acadf9fb1b041a7e0d3ce43571f9dcfc557d41e2a8bbdff6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBundles")
    def put_bundles(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d74e250bd046936ef367d242b425c6d2b6673bdc3edae7e45c20251f868fa87e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBundles", [value]))

    @jsii.member(jsii_name="putTemplateLibrary")
    def put_template_library(
        self,
        *,
        installation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param installation: Configures the manner in which the template library is installed on the cluster. Possible values: INSTALLATION_UNSPECIFIED, NOT_INSTALLED, ALL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#installation GoogleGkeHubFeatureMembership#installation}
        '''
        value = GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary(
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
    ) -> GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList:
        return typing.cast(GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList, jsii.get(self, "bundles"))

    @builtins.property
    @jsii.member(jsii_name="templateLibrary")
    def template_library(
        self,
    ) -> "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference":
        return typing.cast("GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference", jsii.get(self, "templateLibrary"))

    @builtins.property
    @jsii.member(jsii_name="bundlesInput")
    def bundles_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]], jsii.get(self, "bundlesInput"))

    @builtins.property
    @jsii.member(jsii_name="templateLibraryInput")
    def template_library_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"], jsii.get(self, "templateLibraryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30acc396f082242ee6c6bc88cd184efae2499cdabd0b04ff41b4be04f2b8fb79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary",
    jsii_struct_bases=[],
    name_mapping={"installation": "installation"},
)
class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary:
    def __init__(self, *, installation: typing.Optional[builtins.str] = None) -> None:
        '''
        :param installation: Configures the manner in which the template library is installed on the cluster. Possible values: INSTALLATION_UNSPECIFIED, NOT_INSTALLED, ALL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#installation GoogleGkeHubFeatureMembership#installation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060a59ec4eddafa8b70e439f9dd2a9414f560677ccd00b559278a05e99077ad0)
            check_type(argname="argument installation", value=installation, expected_type=type_hints["installation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if installation is not None:
            self._values["installation"] = installation

    @builtins.property
    def installation(self) -> typing.Optional[builtins.str]:
        '''Configures the manner in which the template library is installed on the cluster. Possible values: INSTALLATION_UNSPECIFIED, NOT_INSTALLED, ALL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#installation GoogleGkeHubFeatureMembership#installation}
        '''
        result = self._values.get("installation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75538687f1b4ff19b91bc995d0f500b5763878e2165b4b10ec9650d6b1e52226)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aedc45b4c5a66f919a985c38ccd3aa8008cf0385bff93d43e3c6db26ec4e65a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "installation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1139943854c6eba5f89533a5bb534301cf9770d1d8a4921e7bd89f5c1f741eee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleGkeHubFeatureMembershipTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#create GoogleGkeHubFeatureMembership#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#delete GoogleGkeHubFeatureMembership#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#update GoogleGkeHubFeatureMembership#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a5bb553abd7a22c1eef52885c45e32a464c3d13a2cb9ba05c35244e50d82ec)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#create GoogleGkeHubFeatureMembership#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#delete GoogleGkeHubFeatureMembership#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_hub_feature_membership#update GoogleGkeHubFeatureMembership#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6273023536f4923ee7de0139f5a5d0a048595de0f1fc0c33bdc0358d195a6d09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e53abf0c160bc0d17541f80358f0e22eb774c20d3233f32a9a9292b64601753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c1edb8d698cb137a7065b80e72ac3c9e83d23fa0f17931b0409683e6426131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d939169d09167475d5a307fac867b82315cd395870ce355147b21116e755a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848039da9a6a00355ba120a472de2b78fe7cc7bea4c93809f6064fe0eedbaed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleGkeHubFeatureMembership",
    "GoogleGkeHubFeatureMembershipConfig",
    "GoogleGkeHubFeatureMembershipConfigmanagement",
    "GoogleGkeHubFeatureMembershipConfigmanagementBinauthz",
    "GoogleGkeHubFeatureMembershipConfigmanagementBinauthzOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSync",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersList",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesList",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController",
    "GoogleGkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementPolicyController",
    "GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring",
    "GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference",
    "GoogleGkeHubFeatureMembershipMesh",
    "GoogleGkeHubFeatureMembershipMeshOutputReference",
    "GoogleGkeHubFeatureMembershipPolicycontroller",
    "GoogleGkeHubFeatureMembershipPolicycontrollerOutputReference",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsList",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsOutputReference",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigOutputReference",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary",
    "GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference",
    "GoogleGkeHubFeatureMembershipTimeouts",
    "GoogleGkeHubFeatureMembershipTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bb0b329ce2d05634c944e2255fda1d2c15cbf151adf11be93d9c4d1405e05220(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    feature: builtins.str,
    location: builtins.str,
    membership: builtins.str,
    configmanagement: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagement, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    membership_location: typing.Optional[builtins.str] = None,
    mesh: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipMesh, typing.Dict[builtins.str, typing.Any]]] = None,
    policycontroller: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipPolicycontroller, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8d7a908ab625d0d48ce4d400681dd52e44c533c33188c1881a13cdde6b86aca3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62872bdfceafad454f1f77b15f0c4cc026f50a42b15c1ba4ae1e073493d445cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0958d3b43f6eeee77da3758cde573467dcc5caf896edce568f597a324e95a596(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026490971551372bb2b4367c899e7d13d507691fcd381768b3818da3e4687d8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b83bed14422792af7953f5b45e04cf6f355b207c43f6d8e8c84d5f3625b5217(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94dcd8c44e4d90793d3fdd02f2f2341ee7d07d2339008dad97d7888fa6e957f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf9355e466a5d9bc98e79e3e26b9069d4848147b9de0e5c7e2116507a9f86f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc454f576b0fc2b00803677a901ef7a86701247db18f878efe02b250d0b540e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    feature: builtins.str,
    location: builtins.str,
    membership: builtins.str,
    configmanagement: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagement, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    membership_location: typing.Optional[builtins.str] = None,
    mesh: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipMesh, typing.Dict[builtins.str, typing.Any]]] = None,
    policycontroller: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipPolicycontroller, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673cdaf2b6ede0f68164ef94e08c87a8859b1245ac5838d1574e6f62dd273404(
    *,
    binauthz: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz, typing.Dict[builtins.str, typing.Any]]] = None,
    config_sync: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync, typing.Dict[builtins.str, typing.Any]]] = None,
    hierarchy_controller: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController, typing.Dict[builtins.str, typing.Any]]] = None,
    management: typing.Optional[builtins.str] = None,
    policy_controller: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementPolicyController, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04225f057deab844c0cb925b29cad3893f701acf41f98f3132d42c2afb3ef3a(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ccaf84a28f547aa26e9ab25245859391b3a22e96a645ceffe71511cd995c2c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4c12084bc62c3dc923dc0158909a8b392638774937a49a714438d0209db909(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b76c6c4faf5a0f9077c6b3fbdc82feef33b6cd96a01b492887650117f2bc726(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b061211c1a2c8d4fad557434b81bcefd5bade26fbd8ea7552b2fea3b03ed06(
    *,
    deployment_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    git: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit, typing.Dict[builtins.str, typing.Any]]] = None,
    metrics_gcp_service_account_email: typing.Optional[builtins.str] = None,
    oci: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci, typing.Dict[builtins.str, typing.Any]]] = None,
    prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_format: typing.Optional[builtins.str] = None,
    stop_syncing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2c15bb4725666e77845b22d24e13b8c8976c203b1c8a488548ad6625eba838(
    *,
    containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deployment_name: typing.Optional[builtins.str] = None,
    deployment_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb93f64e45d29e9efe7b52b31ba856a6ca8793c5c8608abad31594022ee18a9a(
    *,
    container_name: typing.Optional[builtins.str] = None,
    cpu_limit: typing.Optional[builtins.str] = None,
    cpu_request: typing.Optional[builtins.str] = None,
    memory_limit: typing.Optional[builtins.str] = None,
    memory_request: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ffa452456d8344354109ed36ff44f3f9c716147d98d74bf50476cf7a1a4b73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c92af53791e072d1bf428d7bf570b1921f732e604b6891dad90485872a2a1d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fbc12efafb6b520ef8ae4bd82c27c1e3da1ec9322a1b3cd0d9b3da2449363b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c0d3a6501caac8eafcb01734e3cfe33beed35220c6df4b11e41f443036aca9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6bb96759fb9bbbfee432af2c2393964a97a92431c8152caaed973e8c17f75c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a6ab582294fce73c16399c4035ecfeacd58f2778d24522b5141ee4c1c2de92a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c02c146d04e7071ab30a38f10a3e8f9c02093325827aef5ee979b5eebbade8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfce67092d97c86ae188c68107061c656d413de82a124b020c3ad6d9ce91206(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1179cfada2964d1a2ab8fbb945b4c3d9ea6d3099f852bbd36b891d97e9990a6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5709fa8b361195b11d2ebb51b73982975c357eff6648d78eb89dd4a8e64ed03a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84737783ad14da09bd5485f69d080157e962be6286dcea75c874071af76c6818(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3106df2077b8e47c7b699e614049e051a911a6e3a8d23c504e70cd71427d01b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6517691602b1cc2547fb757f62e4148c14100f0c5cde8cf42fb387ae2a7ba69e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628550d3524678ef8d1d593ce9c50059b99cd6a85ed7d42d19988d59e88d1ba6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b536985ab1773a7b1eca24da0fbc4d6292e8648160b091d9330100c68875bc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5616392e35b43d270e3f4fc3327d371e9a87875b08bf8aa2e1c6d7337bc08545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6b1e870b376cbeb736bd17f782b7cbc4a4c7f144e662e2ecee3cfd0d459f91(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3018a7a65a5b2050080ffa0f90f1e5483a822822d3aa2206df13f9a32f84916(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ea7aeff29238c6828b36873a9fc384fcc8ae26906ade301c0f1d159d840245(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bbbba33795ddedb60a2805fecda17c61045574986055b905b5eead58a582766(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba702b749ffafcb1c4eac187a0b33851c76f9ca3f3a94573716efa1a0250e726(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae26b3c82a2aaa3ceec5e0cd589d57253d405f930428423d42211f6cc063c6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2926a4c9c394033bc5268b532f5116335ed95d1e0c0437854d7fef9f3eb038(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554635c5a86661c39b6297195d29e47583649b82b4987980b236a151f7b086d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522bb8107583a9bd504bbc0a88d70d193e145ce1e06bde67bb83c4e49c978ef0(
    *,
    gcp_service_account_email: typing.Optional[builtins.str] = None,
    https_proxy: typing.Optional[builtins.str] = None,
    policy_dir: typing.Optional[builtins.str] = None,
    secret_type: typing.Optional[builtins.str] = None,
    sync_branch: typing.Optional[builtins.str] = None,
    sync_repo: typing.Optional[builtins.str] = None,
    sync_rev: typing.Optional[builtins.str] = None,
    sync_wait_secs: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d2da75bf48b92eba5bc3158a896ab3aebe0b6716c430da291f45da5ca95500(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb743348fc43111f1567ac0610ac3d6dff9c7562083a1fc22943e5738383831(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d9469d57214be7b6f662759aed696b58cdbb99d64a7cd04642f72aa8f7e48f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2963c67df0ee74ee7e84e5973f998ae53a4503f4f6739ec2d7a4f3ab327b561d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f10700065e46b3ec1e8fb174b913a6a51decfb8075e09350db7020ce779d4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26675f5523359c070f8fb775fb18716fd8fa2f3bb6f13578e7910464ff8cf46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d85c9e8df10282a54068d6e9935b4ec4caa701f7d43f3515a6c31179ded0c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4b0761bbbc1158b733837e824c1e7a4570d2f0a7c1b6c60eb484a99b7ea593(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20512acf91ddba89927c8fc325bed1d5210bef80b857d393761002e3ec7b3478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773106aa5a71f1fe66e70ded79460931dd2e73ccfdc2eb289cebe3a02344181e(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd4d5eb981ba65901bf2946568f738edde7b90817be9020c2d38418cd25d01f(
    *,
    gcp_service_account_email: typing.Optional[builtins.str] = None,
    policy_dir: typing.Optional[builtins.str] = None,
    secret_type: typing.Optional[builtins.str] = None,
    sync_repo: typing.Optional[builtins.str] = None,
    sync_wait_secs: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2849418628ccfb2315571f2ff3f65c91f264460f538a3471a4e3f4d3806b8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d26efccc73bba21b697ee9259baf0a47590ce24598b91d24e26432f6e138d23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b53a90aef8f2e04c657e158d6c39cef10c94fae202cd25f6d11646dcfa752d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7730f004cd7fc4ddaf529723d942e4e3f338e517b9c49b29508bf437703c845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75328af60c0d1afdb7dc6a3726b7d260638544163a94af3c192edf3608a921d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfce158029b7637a2d734e6c6a3803f140be001093c1e21cde805cee0a0a26e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca09f24f1ec363bb702596d30042fb19469408b7209e0e101c36a22c14e33ff5(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047282ccb356309cbe5ace85f01c64af12fb2abe45d58b180e6101e731aa4aca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9b966e56683b318d7661cfd90dc3476113e6dacd3061e48fdf6afebeec1c6c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25272a7927a94ec9236b4ee4db181a9311f2bbef2c9bfdc67b2fc38dc9e0b914(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea81931103bff4e166f0cf752a93c24b5ec4a969bc7f65c2020bca44d41d4c9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6820a5620129cc3c93a53c4f2c95b355b437da49af19691c8c7a73ebd973a6d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4094b68a0609037532af69c466ae51b836b2075f358d9f79aaae1bdce2bf32b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52daa8ddf37aa524b3a192c7f12e2315b434f194d8f71c19495a86510be36d41(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd25ad1da63bf090cd3f39600fd52aa32f34ba770e0cfd2925de4788e79444dd(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8cd921ea3bccd5713a7ce72e5d069f79f3e1ef2c002146d20f255cd94856b2(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_hierarchical_resource_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_pod_tree_labels: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b95d561d2e336ffaff77ab4e4abcd5597bdb153ca78a17a7417abf9193e9c34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2197ebc77aebabbccb3b8117d0e11c8d5ca89434746a96d6dfb4149aa52a22fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c92b3cd9d85efc171ddd92e9f274aa042c8b5919bcb1fcb706263105896271(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db5495bf3427f1eb8f1b60c4064b199b2c1986767d547367c2318f836e47b5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752b4e6199457f99c63eb48bfee9c7bd347d9c7cf04203c4e7dcb5ef3edf0d42(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b4f920a39c7b1c45a712235cbffd0082b5858b473f040eef0da90f1f32730f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ed1242b07ff2a314b428f0630072e67d770f8029051ad7c65c62e15d9c6e0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3bb65c10d9a5d4a130a3fbf44656c5548601ed2e3192c184a5ab253ee3dd47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0472bf1aab5e3e538c38efaa57adb346fe186ce6b354a3ad40d47f191762e9(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e638940c8c715fbc156b9b6355555ffdf29a8dbafe84a8590b4b2147cf3f148(
    *,
    audit_interval_seconds: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitoring: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring, typing.Dict[builtins.str, typing.Any]]] = None,
    mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    template_library_installed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46b4eed8b3413d8a103dc814d01a3a1e8910f46d714d75809d0ca0523497962(
    *,
    backends: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2828c9499ab339bd608500255c84bcfd7fd04f31afaddbdbe646da4aa14e5046(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08114d8c1874c0b70da8028a3219f781ab9475f10d7e8de9227925615bd09f75(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56aae9e90a6d26a7fd64323d3d1ea5dac4645f6b63fd85eaf34c9ca2572625fa(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01a6308da6a2ea089b19c438f90175ae8e7723c5eb3c027bedb9de60b7c2d1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6bd92abe8eda74a1dc751933ccc9f78e8709b1f4e4280dca9f6d1f33712181(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07510763f8e532dc8cd31e94f893b0d360a679d33a1a80d195a7dbd6384181e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb109ff29bbfd1e2769227f6f49ff3799f8e4b6b6fe60602c98096cbacdf1d88(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf4e7fef3f5b42771685f38994fc5b6b15f94ef04791fb108714f466ea1e454(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969da8e1b8fe0675c96fb33e5b7b1ebc7b4f232aa2dc6c37060c2779fac5cd67(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43448b9f005e2e7d89e24f3359225cd8c2ada459f7a6525b1daf8fc31bb3d341(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e39b1e0b78621b7cc569d326f553aa1e47d9e8a7d1fbf024c24e100b04f57c8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2481b1b520b71b8e2947e25b676f3a045438237afb75341ccf06fc510c022778(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyController],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e02410be6366371ef684ffe9ad2f718f113946d1bc8b099a10b00600d23a1f(
    *,
    control_plane: typing.Optional[builtins.str] = None,
    management: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb914b84ea122ed7e2712b07b2d9c9dc3377791756040d6200068806301255a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31b4aa8e522d7506c6d54156d51c99d9ae3748fbd75621af8ac842067742c71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b460959e6130a0c71d2f8528cb9c26edf5ce367d138d479c25b81755396e4188(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c6346e3d79f710d4f7a24211fe3f852ca4f2bee64a5ddec97aa54abd564be0(
    value: typing.Optional[GoogleGkeHubFeatureMembershipMesh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc574274da9fff76ede7119f148b2fe03e9e13b27729e8ce1fc8221ddf18e13(
    *,
    policy_controller_hub_config: typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig, typing.Dict[builtins.str, typing.Any]],
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538924dd1464055bf5738b2d324f68fcd218aec40de03bb2b5f999af89040d38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbeb96eab6aded586b77803bc1868880ef65e5273e17790207ecd3284ff13ecc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b9974b3365c5f530aae0d04e8568597ecb795e1644d2ae16035225eb5d1c34(
    value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontroller],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e001413611735258210195e4a2c30760be6ea81c77169948ef39c486a02d10(
    *,
    audit_interval_seconds: typing.Optional[jsii.Number] = None,
    constraint_violation_limit: typing.Optional[jsii.Number] = None,
    deployment_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    install_spec: typing.Optional[builtins.str] = None,
    log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitoring: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring, typing.Dict[builtins.str, typing.Any]]] = None,
    mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policy_content: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent, typing.Dict[builtins.str, typing.Any]]] = None,
    referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d8a7ebe422b4d857b23b651b53fbd5f36e80d1cef9e5124155b1d7ca21d679(
    *,
    component_name: builtins.str,
    container_resources: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources, typing.Dict[builtins.str, typing.Any]]] = None,
    pod_affinity: typing.Optional[builtins.str] = None,
    pod_tolerations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    replica_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f426ede36cc1088caa05765ada27c2481c20bed2e818d241957a88f5c179d565(
    *,
    limits: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    requests: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a2414f1aa082dd9312ce7ca515f87759030b06a19faa80384fe41eba22973c(
    *,
    cpu: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b187e9b3f620e39859fa3654eb142d3c0921caea399e4509261b52bce79d2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fab6f090331c4e6163b8d5f53741d71fb01788cec8b51601842b141338c117(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc9574fcc0feee41f0146af56ae957179596e3ab531207c5a9b073a54af527e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74cf1ced27dfeb16620c7283d41c0a35dd50bd1446d4f291f4533ba8f7bf975(
    value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79bd9087d68eac051d174f6c17c522f46f479d42c3f9a8032d688ae493596cb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42ace71451c7412fc347b2f6e806045dfa092f2a85a0efcd602cd07981eec2d(
    value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c719305f0aa26722a81bfd7126e3134b1ded4dca1b6c07779dfae14deceb10ba(
    *,
    cpu: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1339ae2d35a21e2849ff2eb12b23fa210edb0e657a670ad8ecb19c8d0cca329(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c6d63a449b8fecd1b031c64ed98c3e7c1c9774f10cd4c53e5f76b92cf45690(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259f536e852ceb447bacdaa629f25af93901c7218cef6f83a767b5cdffaa7faa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ee26a94c6559c8d3ffd4dbb47b20f9c38abc22562289b35dac46e7a6f70a92(
    value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf1426ee90d5df02bbffb1a965f296c48b98c71268adc6f484564208df95d3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4885fba9f7a90a87cbdcd72388ef0a5f52b75621f9df76e073f2ca317800c63c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697559b1487febd9ff36ac3b24cb17a48b06bd2e8c2e5247cdf2817591cbbb4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2612e38c78fef49139e13d48e71486c8fc46571c4a620ab43bc8699dbbdc5679(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a6221c180578f5ca069881d22d7fd0e676f2a53547d3393932b3338c1acdd1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8913dd86d91d22fc5690503256ca7e8fb9bc615292090268927f9ba360c4c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8004c71ec8772b4c80eca7ac22946b103ecf9d8d72b127d956d39c229b46786(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d3d67581e7a9a8880e7bbcfe5ad8acdf3f442829a06c7176dccf7429775274(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6c4e54a2a5e68b435eadfe5ed63be38a27e684a79debeb7230fd860265f36d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e4093c0665876b37c901143060d4a53fa988522438f093252d9865a30a6530(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ec7d8de6df38052c6e0e9f49633490164513acc4fba0453bddd41ba3556579(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cadf8ca27708c5502c622fe9d4bf4d69dfe07aafd38f47b37b62190c6cddcd52(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997643aefc2ec0dfc62c3a4c2edfb4d99cbd388196ff627946726a9c8a505538(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde608202f17193aefe815a7303000caeeb1aa32e8b1d78363b9db926704c1f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7313f8741a6f84859d438852df408383a631b5b8024cee3f2f605b7417d452(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d301745833f3c097ac8fb9360cb34b14bb6bec8b2e8c1d6f0891561cc20538f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f153fcd0e0288875961d59d647318eb425fee2e8f3440af85bc3294ab1a215(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634dba8256442d6691b2b11a3a2209bc059267657c1271c5be4857f446924efa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264045e1e20a577615054cbb792686b77cc0437badc33dbec2c5d17a26491d0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8587b2495c535138dd7a94001c49625d2f55ba0b82a0314b232c9123f3c38230(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9299f67685f0c0e33c952397c6b47767e6541bfc4671363ddb1de995d2a159f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44acf298d3c9957ff73359ae8ea73a5f7581eee747f5567e8e2fba1b61326592(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0cb6243d2a39213773901c9f46f4b621c7c0e380a992e9ada41dd25da2c94a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6efd0e4984ba0d91aae208bc467f6734d1915ca28753b913568e0bcb85b5024(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7070e3d3465b4f9633c155489afb2ddba21b9e62a886842eb6cab54e5786a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc934eb7161ce2c8c7a6ceec95b3def20a4c229e53aac9364760ddd6cacfec8(
    *,
    backends: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50b7d0654263b0a0f0c3db2c6c649a762b3990b939e2a6a20ec992c3b23c1b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352b284852be561143839d59966c7c7a4bc57d1f2770bb76c909c1043bce43bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b5155d64618ea53426de993d7c1025a06cefe3b16e31aff87a38e3d1470824(
    value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f6eeda859597129b1369c2c4f0dcabbe4ec7a892a2a723ccc154e3df5724ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbca61360b0837eb2a8bf3b967d4e3513588358d41fa612e34b7b95fe505da7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2227be24e2ac9350b31d73dc78059d38d013d22cb634225d22970c58b6f15101(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e9885d8dcdbde902b03c8e8c8a8bbf35ee5ce6535d16d0208e068962807c86(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1112831fed83328b51d24c407feda01fafbfacf59128b0f978141e11b4b5ce10(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86399577fb2aac237d60576214573be1048a6a9aaca2d760a305fca79c51661f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1f0bc8a59e4b3da4fab1311901804a83cc972c4693947e1e150741d75ecb8d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f23736d489ebbcc1405fac65b02dd18eacfa978b465f806ea8ae606fe79e14(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f44d80f82be3699d7bdc360115b052496587480743c754d740ffec5f50114a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4bc7e9c68203dd803a8396c08a29aa825782a6f048b8a942731c3c79db0b69(
    value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec868d81697343f300ef9bccee72f379198a06900af16723fe79705c47e42e63(
    *,
    bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles, typing.Dict[builtins.str, typing.Any]]]]] = None,
    template_library: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5325efcc11d9eef79d719e375ba11f8d3d09111bc7e2e2f03ab18fbcafb3af3(
    *,
    bundle_name: builtins.str,
    exempted_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0efd019bc73a99b8001f6cfc39080a74846362bb35435d2ce5cb7a843e1887(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0e0a5d073e5b326467b1df0e5b21173fe98c69667d81fba118e385941bae6e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be251736b888b3862eeae37babf350b6ef9dbbdf33366fd6197ebabb0919d88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecbf2ac8c30f5d8377f0661b20078576b7e245f15d9187135a2c2579a306420(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f686781c283da4bfd751b3fd3eb781200c12dcd7e774b0db7072fbb3b3d872(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2bd91cdd95cd0981119c11ba4d1900ccb38d0839577e1de265ace2a7017d97(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78260af711849087d6c0a8504cfd4532f4897ec416168d6ceec20360a7fa22bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0cb4a01edc7fe73a65e64ea259cabdde2ebe4cd69648a0c9177f85f0d5dd70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f140041b8380d62c28633b7c46d4e585dfc0d75990c99a175482e73267133cee(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1096a07909601635776f36f9158c40052d063701433ff19fbfc0302b5c555c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050d37ff3221737acadf9fb1b041a7e0d3ce43571f9dcfc557d41e2a8bbdff6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74e250bd046936ef367d242b425c6d2b6673bdc3edae7e45c20251f868fa87e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30acc396f082242ee6c6bc88cd184efae2499cdabd0b04ff41b4be04f2b8fb79(
    value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060a59ec4eddafa8b70e439f9dd2a9414f560677ccd00b559278a05e99077ad0(
    *,
    installation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75538687f1b4ff19b91bc995d0f500b5763878e2165b4b10ec9650d6b1e52226(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedc45b4c5a66f919a985c38ccd3aa8008cf0385bff93d43e3c6db26ec4e65a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1139943854c6eba5f89533a5bb534301cf9770d1d8a4921e7bd89f5c1f741eee(
    value: typing.Optional[GoogleGkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a5bb553abd7a22c1eef52885c45e32a464c3d13a2cb9ba05c35244e50d82ec(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6273023536f4923ee7de0139f5a5d0a048595de0f1fc0c33bdc0358d195a6d09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e53abf0c160bc0d17541f80358f0e22eb774c20d3233f32a9a9292b64601753(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c1edb8d698cb137a7065b80e72ac3c9e83d23fa0f17931b0409683e6426131(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d939169d09167475d5a307fac867b82315cd395870ce355147b21116e755a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848039da9a6a00355ba120a472de2b78fe7cc7bea4c93809f6064fe0eedbaed4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
