r'''
# `google_gke_hub_feature_membership`

Refer to the Terraform Registry for docs: [`google_gke_hub_feature_membership`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership).
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


class GkeHubFeatureMembership(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembership",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership google_gke_hub_feature_membership}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        feature: builtins.str,
        location: builtins.str,
        membership: builtins.str,
        configmanagement: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagement", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        membership_location: typing.Optional[builtins.str] = None,
        mesh: typing.Optional[typing.Union["GkeHubFeatureMembershipMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        policycontroller: typing.Optional[typing.Union["GkeHubFeatureMembershipPolicycontroller", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeHubFeatureMembershipTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership google_gke_hub_feature_membership} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param feature: The name of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#feature GkeHubFeatureMembership#feature}
        :param location: The location of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#location GkeHubFeatureMembership#location}
        :param membership: The name of the membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#membership GkeHubFeatureMembership#membership}
        :param configmanagement: configmanagement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#configmanagement GkeHubFeatureMembership#configmanagement}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#id GkeHubFeatureMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param membership_location: The location of the membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#membership_location GkeHubFeatureMembership#membership_location}
        :param mesh: mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#mesh GkeHubFeatureMembership#mesh}
        :param policycontroller: policycontroller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policycontroller GkeHubFeatureMembership#policycontroller}
        :param project: The project of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#project GkeHubFeatureMembership#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#timeouts GkeHubFeatureMembership#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a96870167bc32cdbfdcac336a73c454273cb1475d43f37aa777572ec248fe2b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GkeHubFeatureMembershipConfig(
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
        '''Generates CDKTF code for importing a GkeHubFeatureMembership resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeHubFeatureMembership to import.
        :param import_from_id: The id of the existing GkeHubFeatureMembership that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeHubFeatureMembership to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2aee590de1843789c8ef1dea10a2768edb3a48fee230631a1789a29505465e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfigmanagement")
    def put_configmanagement(
        self,
        *,
        binauthz: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagementBinauthz", typing.Dict[builtins.str, typing.Any]]] = None,
        config_sync: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagementConfigSync", typing.Dict[builtins.str, typing.Any]]] = None,
        hierarchy_controller: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagementHierarchyController", typing.Dict[builtins.str, typing.Any]]] = None,
        management: typing.Optional[builtins.str] = None,
        policy_controller: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagementPolicyController", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param binauthz: binauthz block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#binauthz GkeHubFeatureMembership#binauthz}
        :param config_sync: config_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#config_sync GkeHubFeatureMembership#config_sync}
        :param hierarchy_controller: hierarchy_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#hierarchy_controller GkeHubFeatureMembership#hierarchy_controller}
        :param management: Set this field to MANAGEMENT_AUTOMATIC to enable Config Sync auto-upgrades, and set this field to MANAGEMENT_MANUAL or MANAGEMENT_UNSPECIFIED to disable Config Sync auto-upgrades. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#management GkeHubFeatureMembership#management}
        :param policy_controller: policy_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_controller GkeHubFeatureMembership#policy_controller}
        :param version: Optional. Version of ACM to install. Defaults to the latest version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#version GkeHubFeatureMembership#version}
        '''
        value = GkeHubFeatureMembershipConfigmanagement(
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
        :param control_plane: **DEPRECATED** Whether to automatically manage Service Mesh control planes. Possible values: CONTROL_PLANE_MANAGEMENT_UNSPECIFIED, AUTOMATIC, MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#control_plane GkeHubFeatureMembership#control_plane}
        :param management: Whether to automatically manage Service Mesh. Possible values: MANAGEMENT_UNSPECIFIED, MANAGEMENT_AUTOMATIC, MANAGEMENT_MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#management GkeHubFeatureMembership#management}
        '''
        value = GkeHubFeatureMembershipMesh(
            control_plane=control_plane, management=management
        )

        return typing.cast(None, jsii.invoke(self, "putMesh", [value]))

    @jsii.member(jsii_name="putPolicycontroller")
    def put_policycontroller(
        self,
        *,
        policy_controller_hub_config: typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig", typing.Dict[builtins.str, typing.Any]],
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param policy_controller_hub_config: policy_controller_hub_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_controller_hub_config GkeHubFeatureMembership#policy_controller_hub_config}
        :param version: Optional. Version of Policy Controller to install. Defaults to the latest version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#version GkeHubFeatureMembership#version}
        '''
        value = GkeHubFeatureMembershipPolicycontroller(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#create GkeHubFeatureMembership#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#delete GkeHubFeatureMembership#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#update GkeHubFeatureMembership#update}.
        '''
        value = GkeHubFeatureMembershipTimeouts(
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
    ) -> "GkeHubFeatureMembershipConfigmanagementOutputReference":
        return typing.cast("GkeHubFeatureMembershipConfigmanagementOutputReference", jsii.get(self, "configmanagement"))

    @builtins.property
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> "GkeHubFeatureMembershipMeshOutputReference":
        return typing.cast("GkeHubFeatureMembershipMeshOutputReference", jsii.get(self, "mesh"))

    @builtins.property
    @jsii.member(jsii_name="policycontroller")
    def policycontroller(
        self,
    ) -> "GkeHubFeatureMembershipPolicycontrollerOutputReference":
        return typing.cast("GkeHubFeatureMembershipPolicycontrollerOutputReference", jsii.get(self, "policycontroller"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GkeHubFeatureMembershipTimeoutsOutputReference":
        return typing.cast("GkeHubFeatureMembershipTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="configmanagementInput")
    def configmanagement_input(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipConfigmanagement"]:
        return typing.cast(typing.Optional["GkeHubFeatureMembershipConfigmanagement"], jsii.get(self, "configmanagementInput"))

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
    def mesh_input(self) -> typing.Optional["GkeHubFeatureMembershipMesh"]:
        return typing.cast(typing.Optional["GkeHubFeatureMembershipMesh"], jsii.get(self, "meshInput"))

    @builtins.property
    @jsii.member(jsii_name="policycontrollerInput")
    def policycontroller_input(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipPolicycontroller"]:
        return typing.cast(typing.Optional["GkeHubFeatureMembershipPolicycontroller"], jsii.get(self, "policycontrollerInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeHubFeatureMembershipTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeHubFeatureMembershipTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="feature")
    def feature(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "feature"))

    @feature.setter
    def feature(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3512006e65eab1a04198554dcdfc7196f0a342cfaef0f6c6eb6fbcf93d00a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "feature", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54665bf3a6d4aac656975ceaeabc90ae7c54b56d5bc87779704ed754f305f1b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf1ded7253a545b531d5a3d11c9bfd3b06f0ee6705499a2b777c5ccf549907b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membership")
    def membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "membership"))

    @membership.setter
    def membership(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9d1532736e4c16b290c3dc87d4e5ac1e2223ac2e9dc329efce725c8789cb8dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membershipLocation")
    def membership_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "membershipLocation"))

    @membership_location.setter
    def membership_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23fed7629d4b6fff80f0b47acb25749d4ccc87e5aaf8106f2d0d47126e1c5b46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membershipLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00a47c92acacc4bbf6a29ebed750df6dba1e9fe1e1af9054edde70a9a4abebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfig",
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
class GkeHubFeatureMembershipConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        configmanagement: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagement", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        membership_location: typing.Optional[builtins.str] = None,
        mesh: typing.Optional[typing.Union["GkeHubFeatureMembershipMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        policycontroller: typing.Optional[typing.Union["GkeHubFeatureMembershipPolicycontroller", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeHubFeatureMembershipTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param feature: The name of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#feature GkeHubFeatureMembership#feature}
        :param location: The location of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#location GkeHubFeatureMembership#location}
        :param membership: The name of the membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#membership GkeHubFeatureMembership#membership}
        :param configmanagement: configmanagement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#configmanagement GkeHubFeatureMembership#configmanagement}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#id GkeHubFeatureMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param membership_location: The location of the membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#membership_location GkeHubFeatureMembership#membership_location}
        :param mesh: mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#mesh GkeHubFeatureMembership#mesh}
        :param policycontroller: policycontroller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policycontroller GkeHubFeatureMembership#policycontroller}
        :param project: The project of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#project GkeHubFeatureMembership#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#timeouts GkeHubFeatureMembership#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(configmanagement, dict):
            configmanagement = GkeHubFeatureMembershipConfigmanagement(**configmanagement)
        if isinstance(mesh, dict):
            mesh = GkeHubFeatureMembershipMesh(**mesh)
        if isinstance(policycontroller, dict):
            policycontroller = GkeHubFeatureMembershipPolicycontroller(**policycontroller)
        if isinstance(timeouts, dict):
            timeouts = GkeHubFeatureMembershipTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1011a9208bab4a587190961eecb477d69b286a0c9e569ed8a407abb498efcd7d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#feature GkeHubFeatureMembership#feature}
        '''
        result = self._values.get("feature")
        assert result is not None, "Required property 'feature' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#location GkeHubFeatureMembership#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def membership(self) -> builtins.str:
        '''The name of the membership.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#membership GkeHubFeatureMembership#membership}
        '''
        result = self._values.get("membership")
        assert result is not None, "Required property 'membership' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configmanagement(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipConfigmanagement"]:
        '''configmanagement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#configmanagement GkeHubFeatureMembership#configmanagement}
        '''
        result = self._values.get("configmanagement")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipConfigmanagement"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#id GkeHubFeatureMembership#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def membership_location(self) -> typing.Optional[builtins.str]:
        '''The location of the membership.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#membership_location GkeHubFeatureMembership#membership_location}
        '''
        result = self._values.get("membership_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh(self) -> typing.Optional["GkeHubFeatureMembershipMesh"]:
        '''mesh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#mesh GkeHubFeatureMembership#mesh}
        '''
        result = self._values.get("mesh")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipMesh"], result)

    @builtins.property
    def policycontroller(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipPolicycontroller"]:
        '''policycontroller block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policycontroller GkeHubFeatureMembership#policycontroller}
        '''
        result = self._values.get("policycontroller")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipPolicycontroller"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project of the feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#project GkeHubFeatureMembership#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeHubFeatureMembershipTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#timeouts GkeHubFeatureMembership#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagement",
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
class GkeHubFeatureMembershipConfigmanagement:
    def __init__(
        self,
        *,
        binauthz: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagementBinauthz", typing.Dict[builtins.str, typing.Any]]] = None,
        config_sync: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagementConfigSync", typing.Dict[builtins.str, typing.Any]]] = None,
        hierarchy_controller: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagementHierarchyController", typing.Dict[builtins.str, typing.Any]]] = None,
        management: typing.Optional[builtins.str] = None,
        policy_controller: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagementPolicyController", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param binauthz: binauthz block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#binauthz GkeHubFeatureMembership#binauthz}
        :param config_sync: config_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#config_sync GkeHubFeatureMembership#config_sync}
        :param hierarchy_controller: hierarchy_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#hierarchy_controller GkeHubFeatureMembership#hierarchy_controller}
        :param management: Set this field to MANAGEMENT_AUTOMATIC to enable Config Sync auto-upgrades, and set this field to MANAGEMENT_MANUAL or MANAGEMENT_UNSPECIFIED to disable Config Sync auto-upgrades. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#management GkeHubFeatureMembership#management}
        :param policy_controller: policy_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_controller GkeHubFeatureMembership#policy_controller}
        :param version: Optional. Version of ACM to install. Defaults to the latest version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#version GkeHubFeatureMembership#version}
        '''
        if isinstance(binauthz, dict):
            binauthz = GkeHubFeatureMembershipConfigmanagementBinauthz(**binauthz)
        if isinstance(config_sync, dict):
            config_sync = GkeHubFeatureMembershipConfigmanagementConfigSync(**config_sync)
        if isinstance(hierarchy_controller, dict):
            hierarchy_controller = GkeHubFeatureMembershipConfigmanagementHierarchyController(**hierarchy_controller)
        if isinstance(policy_controller, dict):
            policy_controller = GkeHubFeatureMembershipConfigmanagementPolicyController(**policy_controller)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1726b90741e6331d8b802a147dacd909f44fc57506ef5c7b888888f5c988c88a)
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
    ) -> typing.Optional["GkeHubFeatureMembershipConfigmanagementBinauthz"]:
        '''binauthz block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#binauthz GkeHubFeatureMembership#binauthz}
        '''
        result = self._values.get("binauthz")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipConfigmanagementBinauthz"], result)

    @builtins.property
    def config_sync(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipConfigmanagementConfigSync"]:
        '''config_sync block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#config_sync GkeHubFeatureMembership#config_sync}
        '''
        result = self._values.get("config_sync")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipConfigmanagementConfigSync"], result)

    @builtins.property
    def hierarchy_controller(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipConfigmanagementHierarchyController"]:
        '''hierarchy_controller block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#hierarchy_controller GkeHubFeatureMembership#hierarchy_controller}
        '''
        result = self._values.get("hierarchy_controller")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipConfigmanagementHierarchyController"], result)

    @builtins.property
    def management(self) -> typing.Optional[builtins.str]:
        '''Set this field to MANAGEMENT_AUTOMATIC to enable Config Sync auto-upgrades, and set this field to MANAGEMENT_MANUAL or MANAGEMENT_UNSPECIFIED to disable Config Sync auto-upgrades.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#management GkeHubFeatureMembership#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_controller(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipConfigmanagementPolicyController"]:
        '''policy_controller block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_controller GkeHubFeatureMembership#policy_controller}
        '''
        result = self._values.get("policy_controller")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipConfigmanagementPolicyController"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Optional. Version of ACM to install. Defaults to the latest version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#version GkeHubFeatureMembership#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipConfigmanagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementBinauthz",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GkeHubFeatureMembershipConfigmanagementBinauthz:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether binauthz is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enabled GkeHubFeatureMembership#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__689b97183b28ffbb7fb03f78337b508eef556d80fbbfb22222e1c0492433ab0d)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether binauthz is enabled in this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enabled GkeHubFeatureMembership#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipConfigmanagementBinauthz(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipConfigmanagementBinauthzOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementBinauthzOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ffabfe355074ab4fd0964eb551b45e5660ba91ef904d5e7645bee5e1e648e6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa9a151294c51b24b5ab5f2f0c45f9df0a55797c8720ac6761b5bf0d1c6a7317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagementBinauthz]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagementBinauthz], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipConfigmanagementBinauthz],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d730595ca48e2913c9178174ab2734366d091e93e275236303edb3d0cb09932d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementConfigSync",
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
class GkeHubFeatureMembershipConfigmanagementConfigSync:
    def __init__(
        self,
        *,
        deployment_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        git: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagementConfigSyncGit", typing.Dict[builtins.str, typing.Any]]] = None,
        metrics_gcp_service_account_email: typing.Optional[builtins.str] = None,
        oci: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagementConfigSyncOci", typing.Dict[builtins.str, typing.Any]]] = None,
        prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_format: typing.Optional[builtins.str] = None,
        stop_syncing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param deployment_overrides: deployment_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#deployment_overrides GkeHubFeatureMembership#deployment_overrides}
        :param enabled: Enables the installation of ConfigSync. If set to true, ConfigSync resources will be created and the other ConfigSync fields will be applied if exist. If set to false, all other ConfigSync fields will be ignored, ConfigSync resources will be deleted. If omitted, ConfigSync resources will be managed depends on the presence of the git or oci field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enabled GkeHubFeatureMembership#enabled}
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#git GkeHubFeatureMembership#git}
        :param metrics_gcp_service_account_email: Deprecated: If Workload Identity Federation for GKE is enabled, Google Cloud Service Account is no longer needed for exporting Config Sync metrics: https://cloud.google.com/kubernetes-engine/enterprise/config-sync/docs/how-to/monitor-config-sync-cloud-monitoring#custom-monitoring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#metrics_gcp_service_account_email GkeHubFeatureMembership#metrics_gcp_service_account_email}
        :param oci: oci block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#oci GkeHubFeatureMembership#oci}
        :param prevent_drift: Set to true to enable the Config Sync admission webhook to prevent drifts. If set to ``false``, disables the Config Sync admission webhook and does not prevent drifts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#prevent_drift GkeHubFeatureMembership#prevent_drift}
        :param source_format: Specifies whether the Config Sync Repo is in "hierarchical" or "unstructured" mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#source_format GkeHubFeatureMembership#source_format}
        :param stop_syncing: Set to true to stop syncing configs for a single cluster. Default: false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#stop_syncing GkeHubFeatureMembership#stop_syncing}
        '''
        if isinstance(git, dict):
            git = GkeHubFeatureMembershipConfigmanagementConfigSyncGit(**git)
        if isinstance(oci, dict):
            oci = GkeHubFeatureMembershipConfigmanagementConfigSyncOci(**oci)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea17a61ff333b604f5f609632beb36f5d2f6c8c7aecdcfbf77f58e0610a1c858)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides"]]]:
        '''deployment_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#deployment_overrides GkeHubFeatureMembership#deployment_overrides}
        '''
        result = self._values.get("deployment_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides"]]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the installation of ConfigSync.

        If set to true, ConfigSync resources will be created and the other ConfigSync fields will be applied if exist. If set to false, all other ConfigSync fields will be ignored, ConfigSync resources will be deleted. If omitted, ConfigSync resources will be managed depends on the presence of the git or oci field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enabled GkeHubFeatureMembership#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def git(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipConfigmanagementConfigSyncGit"]:
        '''git block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#git GkeHubFeatureMembership#git}
        '''
        result = self._values.get("git")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipConfigmanagementConfigSyncGit"], result)

    @builtins.property
    def metrics_gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''Deprecated: If Workload Identity Federation for GKE is enabled, Google Cloud Service Account is no longer needed for exporting Config Sync metrics: https://cloud.google.com/kubernetes-engine/enterprise/config-sync/docs/how-to/monitor-config-sync-cloud-monitoring#custom-monitoring.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#metrics_gcp_service_account_email GkeHubFeatureMembership#metrics_gcp_service_account_email}
        '''
        result = self._values.get("metrics_gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oci(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipConfigmanagementConfigSyncOci"]:
        '''oci block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#oci GkeHubFeatureMembership#oci}
        '''
        result = self._values.get("oci")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipConfigmanagementConfigSyncOci"], result)

    @builtins.property
    def prevent_drift(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to enable the Config Sync admission webhook to prevent drifts.

        If set to ``false``, disables the Config Sync admission webhook and does not prevent drifts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#prevent_drift GkeHubFeatureMembership#prevent_drift}
        '''
        result = self._values.get("prevent_drift")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_format(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the Config Sync Repo is in "hierarchical" or "unstructured" mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#source_format GkeHubFeatureMembership#source_format}
        '''
        result = self._values.get("source_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stop_syncing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to stop syncing configs for a single cluster. Default: false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#stop_syncing GkeHubFeatureMembership#stop_syncing}
        '''
        result = self._values.get("stop_syncing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipConfigmanagementConfigSync(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "containers": "containers",
        "deployment_name": "deploymentName",
        "deployment_namespace": "deploymentNamespace",
    },
)
class GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides:
    def __init__(
        self,
        *,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        deployment_name: typing.Optional[builtins.str] = None,
        deployment_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#containers GkeHubFeatureMembership#containers}
        :param deployment_name: The name of the Deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#deployment_name GkeHubFeatureMembership#deployment_name}
        :param deployment_namespace: The namespace of the Deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#deployment_namespace GkeHubFeatureMembership#deployment_namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c04067944061820c85ab30c1b72604238f12f3131f4008fc7b1220bdedf6811)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers"]]]:
        '''containers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#containers GkeHubFeatureMembership#containers}
        '''
        result = self._values.get("containers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers"]]], result)

    @builtins.property
    def deployment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Deployment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#deployment_name GkeHubFeatureMembership#deployment_name}
        '''
        result = self._values.get("deployment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the Deployment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#deployment_namespace GkeHubFeatureMembership#deployment_namespace}
        '''
        result = self._values.get("deployment_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers",
    jsii_struct_bases=[],
    name_mapping={
        "container_name": "containerName",
        "cpu_limit": "cpuLimit",
        "cpu_request": "cpuRequest",
        "memory_limit": "memoryLimit",
        "memory_request": "memoryRequest",
    },
)
class GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers:
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
        :param container_name: The name of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#container_name GkeHubFeatureMembership#container_name}
        :param cpu_limit: The CPU limit of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#cpu_limit GkeHubFeatureMembership#cpu_limit}
        :param cpu_request: The CPU request of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#cpu_request GkeHubFeatureMembership#cpu_request}
        :param memory_limit: The memory limit of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#memory_limit GkeHubFeatureMembership#memory_limit}
        :param memory_request: The memory request of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#memory_request GkeHubFeatureMembership#memory_request}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5268a4b6a8740eb13de188830ce9a5cc2ffe86cbbcd76fa13821cf2e603f90da)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#container_name GkeHubFeatureMembership#container_name}
        '''
        result = self._values.get("container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_limit(self) -> typing.Optional[builtins.str]:
        '''The CPU limit of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#cpu_limit GkeHubFeatureMembership#cpu_limit}
        '''
        result = self._values.get("cpu_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_request(self) -> typing.Optional[builtins.str]:
        '''The CPU request of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#cpu_request GkeHubFeatureMembership#cpu_request}
        '''
        result = self._values.get("cpu_request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory_limit(self) -> typing.Optional[builtins.str]:
        '''The memory limit of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#memory_limit GkeHubFeatureMembership#memory_limit}
        '''
        result = self._values.get("memory_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory_request(self) -> typing.Optional[builtins.str]:
        '''The memory request of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#memory_request GkeHubFeatureMembership#memory_request}
        '''
        result = self._values.get("memory_request")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__139c81dcc34046cf5d4eef978fabc83653ddfabdb7d86b70bf79e12cb038c954)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f5e1881514f82496a4555707157c633fac0605a8ab95c0fe545d3c9c7ac967)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89cb6d16963d80f22248c06e0a0a44831d68d154f75418f334a7be1388c3281c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8543803e3d1c6f22375c0a58e76d215c72478696a4784d2617e07649fc7382a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20148e72fba502c0a3c066e314965c190f02a4d5a69719989c1c70be32a7d90d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e06c8ddc5390e81dfc0d52029194e745b504dc0ff2fce7fa0259c0b3ceb23d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5162205821fe5e6d9ba597a66fb946d50bd135e3f95be89d55e87aa7df14acaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c79595257b1ee838f8dc15310e61d69c10202241e07b44dc1d6e5300cd4b979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuLimit")
    def cpu_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuLimit"))

    @cpu_limit.setter
    def cpu_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62df76314f67904fad370d1289d310f6b82f222f0fd84f681b9f03e3061e3c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuRequest")
    def cpu_request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuRequest"))

    @cpu_request.setter
    def cpu_request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf24858006777e307a8534817930d3e6b9467a76fb9d63594456d342e7e9f2c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryLimit")
    def memory_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memoryLimit"))

    @memory_limit.setter
    def memory_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca2529ad622160d116d10dd6905933ae929366a23e165b114069b5cdb4e0b1d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryRequest")
    def memory_request(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memoryRequest"))

    @memory_request.setter
    def memory_request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7872fa5127bd5f65af50d252415e95ccad5b23ab2f979d66fb73b5415bb3d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c497098a75d221fb13b73de60b4c845de7b8a5e1dbcdf187466d9ec4ebba96a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82ea8302569d5b5882204c4e674a4b9d6acc9e8b13bbbfc6f1b1b4b1175bb0a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f81251799d1c453aecfba0dced6802886c5f0527657193e8be5202e0bf3bc0c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60d96f925f0b61456f4966ae86a6263021f66bf29b658b09ef385962bf468e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be776327837dcffc6a9619cc9ab40f51f2406f24f739af99cfd6cf7be1537528)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9694e7b44ee234981aa8fba2fc748211ec344dd00a71083a14e93aa125d7d178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c53f501ea5fa90e9d3ffb29b67baa920611bf994d6f49cfd42a1224d4eab02ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5e06f89403f613905ed357aa571d2362643d7b2c83a6d4981729b04dc531035)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putContainers")
    def put_containers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32c027454f41438a4f644a93dd78bbdea613bdca2a9f6d8a029352d6f3a42726)
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
    ) -> GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersList:
        return typing.cast(GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersList, jsii.get(self, "containers"))

    @builtins.property
    @jsii.member(jsii_name="containersInput")
    def containers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]], jsii.get(self, "containersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cf96694e294acbbdfad57f25a5f9cd5bcbfd89b7c21362a7fe932d88a318baac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentNamespace")
    def deployment_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentNamespace"))

    @deployment_namespace.setter
    def deployment_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33def2f6aa92a4671fd0530ef52b5f512693311ac5a31b3b795823cd44b9e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5099c169fa0f4015ca05b255badcd5d765de6844a5b19f619f697053c51e01c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementConfigSyncGit",
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
class GkeHubFeatureMembershipConfigmanagementConfigSyncGit:
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
        :param gcp_service_account_email: The GCP Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#gcp_service_account_email GkeHubFeatureMembership#gcp_service_account_email}
        :param https_proxy: URL for the HTTPS proxy to be used when communicating with the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#https_proxy GkeHubFeatureMembership#https_proxy}
        :param policy_dir: The path within the Git repository that represents the top level of the repo to sync. Default: the root directory of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_dir GkeHubFeatureMembership#policy_dir}
        :param secret_type: Type of secret configured for access to the Git repo. Must be one of ssh, cookiefile, gcenode, token, gcpserviceaccount or none. The validation of this is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#secret_type GkeHubFeatureMembership#secret_type}
        :param sync_branch: The branch of the repository to sync from. Default: master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_branch GkeHubFeatureMembership#sync_branch}
        :param sync_repo: The URL of the Git repository to use as the source of truth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_repo GkeHubFeatureMembership#sync_repo}
        :param sync_rev: Git revision (tag or hash) to check out. Default HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_rev GkeHubFeatureMembership#sync_rev}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_wait_secs GkeHubFeatureMembership#sync_wait_secs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45fcde1907aceadc36931f91434e43b71ed5f724a3f29099dd2f2132b1418d5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#gcp_service_account_email GkeHubFeatureMembership#gcp_service_account_email}
        '''
        result = self._values.get("gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_proxy(self) -> typing.Optional[builtins.str]:
        '''URL for the HTTPS proxy to be used when communicating with the Git repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#https_proxy GkeHubFeatureMembership#https_proxy}
        '''
        result = self._values.get("https_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_dir(self) -> typing.Optional[builtins.str]:
        '''The path within the Git repository that represents the top level of the repo to sync.

        Default: the root directory of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_dir GkeHubFeatureMembership#policy_dir}
        '''
        result = self._values.get("policy_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_type(self) -> typing.Optional[builtins.str]:
        '''Type of secret configured for access to the Git repo.

        Must be one of ssh, cookiefile, gcenode, token, gcpserviceaccount or none. The validation of this is case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#secret_type GkeHubFeatureMembership#secret_type}
        '''
        result = self._values.get("secret_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_branch(self) -> typing.Optional[builtins.str]:
        '''The branch of the repository to sync from. Default: master.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_branch GkeHubFeatureMembership#sync_branch}
        '''
        result = self._values.get("sync_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_repo(self) -> typing.Optional[builtins.str]:
        '''The URL of the Git repository to use as the source of truth.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_repo GkeHubFeatureMembership#sync_repo}
        '''
        result = self._values.get("sync_repo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_rev(self) -> typing.Optional[builtins.str]:
        '''Git revision (tag or hash) to check out. Default HEAD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_rev GkeHubFeatureMembership#sync_rev}
        '''
        result = self._values.get("sync_rev")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_wait_secs(self) -> typing.Optional[builtins.str]:
        '''Period in seconds between consecutive syncs. Default: 15.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_wait_secs GkeHubFeatureMembership#sync_wait_secs}
        '''
        result = self._values.get("sync_wait_secs")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipConfigmanagementConfigSyncGit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e93a801795bed8ba89a93c8a19f037c5743c6656dd953896050a00fe3020870)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cc3f0ae9a2c702e07f80195b70cff72184ee9fe14ada17778d72bf53d842de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsProxy")
    def https_proxy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsProxy"))

    @https_proxy.setter
    def https_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df9cded1b65cd7b6d920490ef51cb9b8b4a62cc4b402cfb5ae0ccfc78eb7184a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyDir")
    def policy_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDir"))

    @policy_dir.setter
    def policy_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c68ce06c5116f35dfb61e335b6167043dea872c8f4e2d2cc5e509d1ab1230f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretType")
    def secret_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretType"))

    @secret_type.setter
    def secret_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0402df681a8de8573980907dd7566ec3153b7bed068a140fadb8c3f3c9f0224d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncBranch")
    def sync_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncBranch"))

    @sync_branch.setter
    def sync_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1335247b25e09f81a6480add0043453b38a1b35b0f54a88bc6485ba67850413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncRepo")
    def sync_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRepo"))

    @sync_repo.setter
    def sync_repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb963cbb5aa96b67316ce1a32901d8d9a828c20429a750aa17e7b5192ccb9c6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRepo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncRev")
    def sync_rev(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRev"))

    @sync_rev.setter
    def sync_rev(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__111edf2594439a71b500a467fefbca4c92ea4ae86780cad012b7fb2fca6d4faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRev", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecs")
    def sync_wait_secs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncWaitSecs"))

    @sync_wait_secs.setter
    def sync_wait_secs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5d42e87d53885d085e9780b47f2db7a4a24dc9424b3aaafb5454c79ba335641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncWaitSecs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSyncGit]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSyncGit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSyncGit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efb53f3e0cb6d2e6a0546124a020d522e3e5bd6237fcb712cc5d73f14cf814d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementConfigSyncOci",
    jsii_struct_bases=[],
    name_mapping={
        "gcp_service_account_email": "gcpServiceAccountEmail",
        "policy_dir": "policyDir",
        "secret_type": "secretType",
        "sync_repo": "syncRepo",
        "sync_wait_secs": "syncWaitSecs",
    },
)
class GkeHubFeatureMembershipConfigmanagementConfigSyncOci:
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
        :param gcp_service_account_email: The GCP Service Account Email used for auth when secret_type is gcpserviceaccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#gcp_service_account_email GkeHubFeatureMembership#gcp_service_account_email}
        :param policy_dir: The absolute path of the directory that contains the local resources. Default: the root directory of the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_dir GkeHubFeatureMembership#policy_dir}
        :param secret_type: Type of secret configured for access to the OCI Image. Must be one of gcenode, gcpserviceaccount or none. The validation of this is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#secret_type GkeHubFeatureMembership#secret_type}
        :param sync_repo: The OCI image repository URL for the package to sync from. e.g. LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME/PACKAGE_NAME. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_repo GkeHubFeatureMembership#sync_repo}
        :param sync_wait_secs: Period in seconds(int64 format) between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_wait_secs GkeHubFeatureMembership#sync_wait_secs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3a4a7b3c959733254173fd799a6d4898dcf72e3ed3deb45b10377120e97af6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#gcp_service_account_email GkeHubFeatureMembership#gcp_service_account_email}
        '''
        result = self._values.get("gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_dir(self) -> typing.Optional[builtins.str]:
        '''The absolute path of the directory that contains the local resources. Default: the root directory of the image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_dir GkeHubFeatureMembership#policy_dir}
        '''
        result = self._values.get("policy_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_type(self) -> typing.Optional[builtins.str]:
        '''Type of secret configured for access to the OCI Image.

        Must be one of gcenode, gcpserviceaccount or none. The validation of this is case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#secret_type GkeHubFeatureMembership#secret_type}
        '''
        result = self._values.get("secret_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_repo(self) -> typing.Optional[builtins.str]:
        '''The OCI image repository URL for the package to sync from. e.g. LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME/PACKAGE_NAME.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_repo GkeHubFeatureMembership#sync_repo}
        '''
        result = self._values.get("sync_repo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_wait_secs(self) -> typing.Optional[builtins.str]:
        '''Period in seconds(int64 format) between consecutive syncs. Default: 15.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_wait_secs GkeHubFeatureMembership#sync_wait_secs}
        '''
        result = self._values.get("sync_wait_secs")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipConfigmanagementConfigSyncOci(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__583e97dd6f32df3dd86d903ee55a2f2300ae23a548eb941e57a199531b44a028)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84c8adfa87b14c2bb460dea53373c89f99c0bf7cfa0b2d4b381919c110e71480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyDir")
    def policy_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDir"))

    @policy_dir.setter
    def policy_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7492a570319296913acaa5c282dd866c6ba5c62ad92eabcd8196923ca59bb924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretType")
    def secret_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretType"))

    @secret_type.setter
    def secret_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e941cb3530a43f09dc77ab8586e7eabd3f49d24778ce8893e7f4933f8211cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncRepo")
    def sync_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRepo"))

    @sync_repo.setter
    def sync_repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46211483ada232d63ca3e383f9a9d5b1c0bd56c86bdacca68c5e809a70e63930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRepo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecs")
    def sync_wait_secs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncWaitSecs"))

    @sync_wait_secs.setter
    def sync_wait_secs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d92a2d6f8366a34ca958f54327ad0217853e3b26a7777de439b7e9eb693bea16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncWaitSecs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSyncOci]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSyncOci], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSyncOci],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c05b5c02ccf4b105d0aba002933aba4b6a6ec69becb8145ea6c6caec96aa296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10d1b9d883554c60deb9b39b296097ebf3f339d9f5d7197cb8102cba424bc4ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeploymentOverrides")
    def put_deployment_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eaa012bff14c047901a8be007b1d305761b387fe0e77451d4ac04738fb24572)
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
        :param gcp_service_account_email: The GCP Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#gcp_service_account_email GkeHubFeatureMembership#gcp_service_account_email}
        :param https_proxy: URL for the HTTPS proxy to be used when communicating with the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#https_proxy GkeHubFeatureMembership#https_proxy}
        :param policy_dir: The path within the Git repository that represents the top level of the repo to sync. Default: the root directory of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_dir GkeHubFeatureMembership#policy_dir}
        :param secret_type: Type of secret configured for access to the Git repo. Must be one of ssh, cookiefile, gcenode, token, gcpserviceaccount or none. The validation of this is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#secret_type GkeHubFeatureMembership#secret_type}
        :param sync_branch: The branch of the repository to sync from. Default: master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_branch GkeHubFeatureMembership#sync_branch}
        :param sync_repo: The URL of the Git repository to use as the source of truth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_repo GkeHubFeatureMembership#sync_repo}
        :param sync_rev: Git revision (tag or hash) to check out. Default HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_rev GkeHubFeatureMembership#sync_rev}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_wait_secs GkeHubFeatureMembership#sync_wait_secs}
        '''
        value = GkeHubFeatureMembershipConfigmanagementConfigSyncGit(
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
        :param gcp_service_account_email: The GCP Service Account Email used for auth when secret_type is gcpserviceaccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#gcp_service_account_email GkeHubFeatureMembership#gcp_service_account_email}
        :param policy_dir: The absolute path of the directory that contains the local resources. Default: the root directory of the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_dir GkeHubFeatureMembership#policy_dir}
        :param secret_type: Type of secret configured for access to the OCI Image. Must be one of gcenode, gcpserviceaccount or none. The validation of this is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#secret_type GkeHubFeatureMembership#secret_type}
        :param sync_repo: The OCI image repository URL for the package to sync from. e.g. LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME/PACKAGE_NAME. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_repo GkeHubFeatureMembership#sync_repo}
        :param sync_wait_secs: Period in seconds(int64 format) between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#sync_wait_secs GkeHubFeatureMembership#sync_wait_secs}
        '''
        value = GkeHubFeatureMembershipConfigmanagementConfigSyncOci(
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
    ) -> GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesList:
        return typing.cast(GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesList, jsii.get(self, "deploymentOverrides"))

    @builtins.property
    @jsii.member(jsii_name="git")
    def git(
        self,
    ) -> GkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference:
        return typing.cast(GkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference, jsii.get(self, "git"))

    @builtins.property
    @jsii.member(jsii_name="oci")
    def oci(
        self,
    ) -> GkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference:
        return typing.cast(GkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference, jsii.get(self, "oci"))

    @builtins.property
    @jsii.member(jsii_name="deploymentOverridesInput")
    def deployment_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]], jsii.get(self, "deploymentOverridesInput"))

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
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSyncGit]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSyncGit], jsii.get(self, "gitInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsGcpServiceAccountEmailInput")
    def metrics_gcp_service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricsGcpServiceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="ociInput")
    def oci_input(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSyncOci]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSyncOci], jsii.get(self, "ociInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bf5a8e9bb58a37fc888e7c09624d26009e0f7cf6a226669e09bb2556b2c035c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsGcpServiceAccountEmail")
    def metrics_gcp_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricsGcpServiceAccountEmail"))

    @metrics_gcp_service_account_email.setter
    def metrics_gcp_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fb35a93dc2e90379b9eb9800a2f8bf78a18953ee034dbc59f476e04f2fee52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c5340bd24ecdb1631cbbb6422e4b2f2cca97cd2f7d6f700b444e90c54595fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventDrift", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFormat")
    def source_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFormat"))

    @source_format.setter
    def source_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fced9d9e9938e63c04e200b8289e225b7e22a6abc07b78ad2f80fcd40112b4ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb01f869006d2339b8c5441d1c832eba6ef3d739d385ac209e10164ddb8ea17c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopSyncing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSync]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSync], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSync],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c19425030df5fa09300a88138b169316edf4e9ea283576a41f878fda720714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementHierarchyController",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "enable_hierarchical_resource_quota": "enableHierarchicalResourceQuota",
        "enable_pod_tree_labels": "enablePodTreeLabels",
    },
)
class GkeHubFeatureMembershipConfigmanagementHierarchyController:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_hierarchical_resource_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_pod_tree_labels: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: **DEPRECATED** Configuring Hierarchy Controller through the configmanagement feature is no longer recommended. Use https://github.com/kubernetes-sigs/hierarchical-namespaces instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enabled GkeHubFeatureMembership#enabled}
        :param enable_hierarchical_resource_quota: Whether hierarchical resource quota is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enable_hierarchical_resource_quota GkeHubFeatureMembership#enable_hierarchical_resource_quota}
        :param enable_pod_tree_labels: Whether pod tree labels are enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enable_pod_tree_labels GkeHubFeatureMembership#enable_pod_tree_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e017568bbfcb14c15d2a4d678567346be6949b382cd6209db10faed33c564233)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enabled GkeHubFeatureMembership#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_hierarchical_resource_quota(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether hierarchical resource quota is enabled in this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enable_hierarchical_resource_quota GkeHubFeatureMembership#enable_hierarchical_resource_quota}
        '''
        result = self._values.get("enable_hierarchical_resource_quota")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_pod_tree_labels(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether pod tree labels are enabled in this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enable_pod_tree_labels GkeHubFeatureMembership#enable_pod_tree_labels}
        '''
        result = self._values.get("enable_pod_tree_labels")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipConfigmanagementHierarchyController(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c7ef1fa692b4e23e259f01627f10821dc065e87c38d07bc7382fa01fff2838)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d2d3e7741072bec9b9aef10a52039aab814479c34661144c95fb490be296acc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cbb48e3669dfd3b33906f0fa9c25af14cfde63ede5406afb4206d6caad057a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49365cba62adce206d95a8c06c208885be13a69b315f1724837b8db3a43af2ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePodTreeLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagementHierarchyController]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagementHierarchyController], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipConfigmanagementHierarchyController],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e81d2f26840fdae46158abbc0760a45bc1c3c5d20b9ff5fdc660b5fd7b2aa792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureMembershipConfigmanagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411225477c06591609eac2c06362e51f89640f2a71ad3455ccdca4ed3e7ed9f3)
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
        :param enabled: Whether binauthz is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enabled GkeHubFeatureMembership#enabled}
        '''
        value = GkeHubFeatureMembershipConfigmanagementBinauthz(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putBinauthz", [value]))

    @jsii.member(jsii_name="putConfigSync")
    def put_config_sync(
        self,
        *,
        deployment_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        git: typing.Optional[typing.Union[GkeHubFeatureMembershipConfigmanagementConfigSyncGit, typing.Dict[builtins.str, typing.Any]]] = None,
        metrics_gcp_service_account_email: typing.Optional[builtins.str] = None,
        oci: typing.Optional[typing.Union[GkeHubFeatureMembershipConfigmanagementConfigSyncOci, typing.Dict[builtins.str, typing.Any]]] = None,
        prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_format: typing.Optional[builtins.str] = None,
        stop_syncing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param deployment_overrides: deployment_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#deployment_overrides GkeHubFeatureMembership#deployment_overrides}
        :param enabled: Enables the installation of ConfigSync. If set to true, ConfigSync resources will be created and the other ConfigSync fields will be applied if exist. If set to false, all other ConfigSync fields will be ignored, ConfigSync resources will be deleted. If omitted, ConfigSync resources will be managed depends on the presence of the git or oci field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enabled GkeHubFeatureMembership#enabled}
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#git GkeHubFeatureMembership#git}
        :param metrics_gcp_service_account_email: Deprecated: If Workload Identity Federation for GKE is enabled, Google Cloud Service Account is no longer needed for exporting Config Sync metrics: https://cloud.google.com/kubernetes-engine/enterprise/config-sync/docs/how-to/monitor-config-sync-cloud-monitoring#custom-monitoring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#metrics_gcp_service_account_email GkeHubFeatureMembership#metrics_gcp_service_account_email}
        :param oci: oci block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#oci GkeHubFeatureMembership#oci}
        :param prevent_drift: Set to true to enable the Config Sync admission webhook to prevent drifts. If set to ``false``, disables the Config Sync admission webhook and does not prevent drifts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#prevent_drift GkeHubFeatureMembership#prevent_drift}
        :param source_format: Specifies whether the Config Sync Repo is in "hierarchical" or "unstructured" mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#source_format GkeHubFeatureMembership#source_format}
        :param stop_syncing: Set to true to stop syncing configs for a single cluster. Default: false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#stop_syncing GkeHubFeatureMembership#stop_syncing}
        '''
        value = GkeHubFeatureMembershipConfigmanagementConfigSync(
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
        :param enabled: **DEPRECATED** Configuring Hierarchy Controller through the configmanagement feature is no longer recommended. Use https://github.com/kubernetes-sigs/hierarchical-namespaces instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enabled GkeHubFeatureMembership#enabled}
        :param enable_hierarchical_resource_quota: Whether hierarchical resource quota is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enable_hierarchical_resource_quota GkeHubFeatureMembership#enable_hierarchical_resource_quota}
        :param enable_pod_tree_labels: Whether pod tree labels are enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enable_pod_tree_labels GkeHubFeatureMembership#enable_pod_tree_labels}
        '''
        value = GkeHubFeatureMembershipConfigmanagementHierarchyController(
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
        monitoring: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        template_library_installed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param audit_interval_seconds: Sets the interval for Policy Controller Audit Scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#audit_interval_seconds GkeHubFeatureMembership#audit_interval_seconds}
        :param enabled: Enables the installation of Policy Controller. If false, the rest of PolicyController fields take no effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enabled GkeHubFeatureMembership#enabled}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#exemptable_namespaces GkeHubFeatureMembership#exemptable_namespaces}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#log_denies_enabled GkeHubFeatureMembership#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#monitoring GkeHubFeatureMembership#monitoring}
        :param mutation_enabled: Enable or disable mutation in policy controller. If true, mutation CRDs, webhook and controller deployment will be deployed to the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#mutation_enabled GkeHubFeatureMembership#mutation_enabled}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#referential_rules_enabled GkeHubFeatureMembership#referential_rules_enabled}
        :param template_library_installed: Installs the default template library along with Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#template_library_installed GkeHubFeatureMembership#template_library_installed}
        '''
        value = GkeHubFeatureMembershipConfigmanagementPolicyController(
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
    ) -> GkeHubFeatureMembershipConfigmanagementBinauthzOutputReference:
        return typing.cast(GkeHubFeatureMembershipConfigmanagementBinauthzOutputReference, jsii.get(self, "binauthz"))

    @builtins.property
    @jsii.member(jsii_name="configSync")
    def config_sync(
        self,
    ) -> GkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference:
        return typing.cast(GkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference, jsii.get(self, "configSync"))

    @builtins.property
    @jsii.member(jsii_name="hierarchyController")
    def hierarchy_controller(
        self,
    ) -> GkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference:
        return typing.cast(GkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference, jsii.get(self, "hierarchyController"))

    @builtins.property
    @jsii.member(jsii_name="policyController")
    def policy_controller(
        self,
    ) -> "GkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference":
        return typing.cast("GkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference", jsii.get(self, "policyController"))

    @builtins.property
    @jsii.member(jsii_name="binauthzInput")
    def binauthz_input(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagementBinauthz]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagementBinauthz], jsii.get(self, "binauthzInput"))

    @builtins.property
    @jsii.member(jsii_name="configSyncInput")
    def config_sync_input(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSync]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSync], jsii.get(self, "configSyncInput"))

    @builtins.property
    @jsii.member(jsii_name="hierarchyControllerInput")
    def hierarchy_controller_input(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagementHierarchyController]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagementHierarchyController], jsii.get(self, "hierarchyControllerInput"))

    @builtins.property
    @jsii.member(jsii_name="managementInput")
    def management_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managementInput"))

    @builtins.property
    @jsii.member(jsii_name="policyControllerInput")
    def policy_controller_input(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipConfigmanagementPolicyController"]:
        return typing.cast(typing.Optional["GkeHubFeatureMembershipConfigmanagementPolicyController"], jsii.get(self, "policyControllerInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__47f22505e4b779beba5463877980447c9ae81b1b1ee4f23c5cbc67d7e87f0e7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "management", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a94d69d37fb6a1ff75c7abd0e72d41ab5fede2085aa383a94b25c6bfba4de204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagement]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipConfigmanagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe114025004a573e4f8fc0c89205fb586bdd689d4751076ebb603f31fce17a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementPolicyController",
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
class GkeHubFeatureMembershipConfigmanagementPolicyController:
    def __init__(
        self,
        *,
        audit_interval_seconds: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring: typing.Optional[typing.Union["GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        template_library_installed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param audit_interval_seconds: Sets the interval for Policy Controller Audit Scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#audit_interval_seconds GkeHubFeatureMembership#audit_interval_seconds}
        :param enabled: Enables the installation of Policy Controller. If false, the rest of PolicyController fields take no effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enabled GkeHubFeatureMembership#enabled}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#exemptable_namespaces GkeHubFeatureMembership#exemptable_namespaces}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#log_denies_enabled GkeHubFeatureMembership#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#monitoring GkeHubFeatureMembership#monitoring}
        :param mutation_enabled: Enable or disable mutation in policy controller. If true, mutation CRDs, webhook and controller deployment will be deployed to the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#mutation_enabled GkeHubFeatureMembership#mutation_enabled}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#referential_rules_enabled GkeHubFeatureMembership#referential_rules_enabled}
        :param template_library_installed: Installs the default template library along with Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#template_library_installed GkeHubFeatureMembership#template_library_installed}
        '''
        if isinstance(monitoring, dict):
            monitoring = GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring(**monitoring)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c85fe288cb946331d7fe57019d71fe333ab5e5510c1397dcef4afbf1a44b8e4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#audit_interval_seconds GkeHubFeatureMembership#audit_interval_seconds}
        '''
        result = self._values.get("audit_interval_seconds")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the installation of Policy Controller. If false, the rest of PolicyController fields take no effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#enabled GkeHubFeatureMembership#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exemptable_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of namespaces that are excluded from Policy Controller checks.

        Namespaces do not need to currently exist on the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#exemptable_namespaces GkeHubFeatureMembership#exemptable_namespaces}
        '''
        result = self._values.get("exemptable_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def log_denies_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Logs all denies and dry run failures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#log_denies_enabled GkeHubFeatureMembership#log_denies_enabled}
        '''
        result = self._values.get("log_denies_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monitoring(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring"]:
        '''monitoring block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#monitoring GkeHubFeatureMembership#monitoring}
        '''
        result = self._values.get("monitoring")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring"], result)

    @builtins.property
    def mutation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable mutation in policy controller.

        If true, mutation CRDs, webhook and controller deployment will be deployed to the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#mutation_enabled GkeHubFeatureMembership#mutation_enabled}
        '''
        result = self._values.get("mutation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def referential_rules_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#referential_rules_enabled GkeHubFeatureMembership#referential_rules_enabled}
        '''
        result = self._values.get("referential_rules_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def template_library_installed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Installs the default template library along with Policy Controller.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#template_library_installed GkeHubFeatureMembership#template_library_installed}
        '''
        result = self._values.get("template_library_installed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipConfigmanagementPolicyController(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring",
    jsii_struct_bases=[],
    name_mapping={"backends": "backends"},
)
class GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring:
    def __init__(
        self,
        *,
        backends: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param backends: Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#backends GkeHubFeatureMembership#backends}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ed4a3b277ad27d138e317f8e697da34fac9fccb4dbf5fbd75678555be48212)
            check_type(argname="argument backends", value=backends, expected_type=type_hints["backends"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backends is not None:
            self._values["backends"] = backends

    @builtins.property
    def backends(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#backends GkeHubFeatureMembership#backends}
        '''
        result = self._values.get("backends")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2353e6d5db09eeb5175116895be93b26f4e8a7c4a17be6c1f437c111434e109)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64cc9d2e11175975480dc38401b3d99cedc549edba0e3b0d8ced9ed34100068e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backends", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e032c30be726a8f335a54fdb988b113133e5583fec57388a0a1b5d553c90f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0994bdf7529627bc0302556765ff7217bed8d5dbcf92d91b398ce8dbe94b44b4)
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
        :param backends: Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#backends GkeHubFeatureMembership#backends}
        '''
        value = GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring(
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
    ) -> GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference:
        return typing.cast(GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference, jsii.get(self, "monitoring"))

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
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring], jsii.get(self, "monitoringInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ec4e493026b3cb63c0f3e909c339299c8dc7b323ac7258734df2a2002b7a9935)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8e480722073829cec525fcb1178c1425081fbb898cfd0d277153cd90979de03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exemptableNamespaces")
    def exemptable_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exemptableNamespaces"))

    @exemptable_namespaces.setter
    def exemptable_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3ef7712ef12d5212a4c2da0adccb20d7d51769125cfd8092d25e35ac4fd7a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c494aae757905f71dfdc16af86c720ccdc625b34406c1c39bc3d2ec2db90f41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8b532a9253fd62f1854180f32ac3156b113183f3410cc1d4dbe54c7fff08224)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e6272c93e23a15c18b31f0fd1de63459c305b251dab04b1acd342890e898511)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db8632b8bb218768eacd7de2580996d53642e424627c4bba42ac4cfa51ba2488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateLibraryInstalled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipConfigmanagementPolicyController]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipConfigmanagementPolicyController], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipConfigmanagementPolicyController],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf1bad03fb85c544a0d9600facc1a7af3f2d84e6af1c231ba4b17e2ac0106320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipMesh",
    jsii_struct_bases=[],
    name_mapping={"control_plane": "controlPlane", "management": "management"},
)
class GkeHubFeatureMembershipMesh:
    def __init__(
        self,
        *,
        control_plane: typing.Optional[builtins.str] = None,
        management: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control_plane: **DEPRECATED** Whether to automatically manage Service Mesh control planes. Possible values: CONTROL_PLANE_MANAGEMENT_UNSPECIFIED, AUTOMATIC, MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#control_plane GkeHubFeatureMembership#control_plane}
        :param management: Whether to automatically manage Service Mesh. Possible values: MANAGEMENT_UNSPECIFIED, MANAGEMENT_AUTOMATIC, MANAGEMENT_MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#management GkeHubFeatureMembership#management}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5051e131e93d2f7f068ab1c2749afd37fa309d15a4264035a7949be180c0a19c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#control_plane GkeHubFeatureMembership#control_plane}
        '''
        result = self._values.get("control_plane")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def management(self) -> typing.Optional[builtins.str]:
        '''Whether to automatically manage Service Mesh. Possible values: MANAGEMENT_UNSPECIFIED, MANAGEMENT_AUTOMATIC, MANAGEMENT_MANUAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#management GkeHubFeatureMembership#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipMesh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipMeshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipMeshOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2114e1c47c0be25e1304ad402280a8eb65ebf8b7b8c9896c3ebd693ef432d3e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27526b41379459e32152af6d36d78c99278b77406f9b56ee27851d23a5df02bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlane", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "management"))

    @management.setter
    def management(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__508d4422b37e89b891ce3eae26b61d911a4b0af2025b4096400d74dd27c7da3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "management", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubFeatureMembershipMesh]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipMesh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipMesh],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6c2ab3c1bd8318805cf2bc3ac1f471612142a0a36ebca43ca88ba4f251efe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontroller",
    jsii_struct_bases=[],
    name_mapping={
        "policy_controller_hub_config": "policyControllerHubConfig",
        "version": "version",
    },
)
class GkeHubFeatureMembershipPolicycontroller:
    def __init__(
        self,
        *,
        policy_controller_hub_config: typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig", typing.Dict[builtins.str, typing.Any]],
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param policy_controller_hub_config: policy_controller_hub_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_controller_hub_config GkeHubFeatureMembership#policy_controller_hub_config}
        :param version: Optional. Version of Policy Controller to install. Defaults to the latest version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#version GkeHubFeatureMembership#version}
        '''
        if isinstance(policy_controller_hub_config, dict):
            policy_controller_hub_config = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig(**policy_controller_hub_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea909d4447fa7ac17367510054bb5fe0b3c33f36085dfc09773653d07cc29e3)
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
    ) -> "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig":
        '''policy_controller_hub_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_controller_hub_config GkeHubFeatureMembership#policy_controller_hub_config}
        '''
        result = self._values.get("policy_controller_hub_config")
        assert result is not None, "Required property 'policy_controller_hub_config' is missing"
        return typing.cast("GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig", result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Optional. Version of Policy Controller to install. Defaults to the latest version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#version GkeHubFeatureMembership#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipPolicycontroller(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipPolicycontrollerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673d6051e01b667f7c733d38526d4e22b9aa9473e144b1ab480a4cee4749f38c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPolicyControllerHubConfig")
    def put_policy_controller_hub_config(
        self,
        *,
        audit_interval_seconds: typing.Optional[jsii.Number] = None,
        constraint_violation_limit: typing.Optional[jsii.Number] = None,
        deployment_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        install_spec: typing.Optional[builtins.str] = None,
        log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring: typing.Optional[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_content: typing.Optional[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent", typing.Dict[builtins.str, typing.Any]]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param audit_interval_seconds: Sets the interval for Policy Controller Audit Scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#audit_interval_seconds GkeHubFeatureMembership#audit_interval_seconds}
        :param constraint_violation_limit: The maximum number of audit violations to be stored in a constraint. If not set, the internal default of 20 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#constraint_violation_limit GkeHubFeatureMembership#constraint_violation_limit}
        :param deployment_configs: deployment_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#deployment_configs GkeHubFeatureMembership#deployment_configs}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#exemptable_namespaces GkeHubFeatureMembership#exemptable_namespaces}
        :param install_spec: Configures the mode of the Policy Controller installation. Possible values: INSTALL_SPEC_UNSPECIFIED, INSTALL_SPEC_NOT_INSTALLED, INSTALL_SPEC_ENABLED, INSTALL_SPEC_SUSPENDED, INSTALL_SPEC_DETACHED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#install_spec GkeHubFeatureMembership#install_spec}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#log_denies_enabled GkeHubFeatureMembership#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#monitoring GkeHubFeatureMembership#monitoring}
        :param mutation_enabled: Enables the ability to mutate resources using Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#mutation_enabled GkeHubFeatureMembership#mutation_enabled}
        :param policy_content: policy_content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_content GkeHubFeatureMembership#policy_content}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#referential_rules_enabled GkeHubFeatureMembership#referential_rules_enabled}
        '''
        value = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig(
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
    ) -> "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigOutputReference":
        return typing.cast("GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigOutputReference", jsii.get(self, "policyControllerHubConfig"))

    @builtins.property
    @jsii.member(jsii_name="policyControllerHubConfigInput")
    def policy_controller_hub_config_input(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig"]:
        return typing.cast(typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig"], jsii.get(self, "policyControllerHubConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2a84382a18daa34defee08a67d45113fd36cba4b93e835e730b0d4995ed51359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipPolicycontroller]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipPolicycontroller], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipPolicycontroller],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a9b2d44ea845aeb64f7b21e1622e720da9ab89c1f59746b537ccf725abb7f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig",
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
class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig:
    def __init__(
        self,
        *,
        audit_interval_seconds: typing.Optional[jsii.Number] = None,
        constraint_violation_limit: typing.Optional[jsii.Number] = None,
        deployment_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        install_spec: typing.Optional[builtins.str] = None,
        log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring: typing.Optional[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_content: typing.Optional[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent", typing.Dict[builtins.str, typing.Any]]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param audit_interval_seconds: Sets the interval for Policy Controller Audit Scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#audit_interval_seconds GkeHubFeatureMembership#audit_interval_seconds}
        :param constraint_violation_limit: The maximum number of audit violations to be stored in a constraint. If not set, the internal default of 20 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#constraint_violation_limit GkeHubFeatureMembership#constraint_violation_limit}
        :param deployment_configs: deployment_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#deployment_configs GkeHubFeatureMembership#deployment_configs}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#exemptable_namespaces GkeHubFeatureMembership#exemptable_namespaces}
        :param install_spec: Configures the mode of the Policy Controller installation. Possible values: INSTALL_SPEC_UNSPECIFIED, INSTALL_SPEC_NOT_INSTALLED, INSTALL_SPEC_ENABLED, INSTALL_SPEC_SUSPENDED, INSTALL_SPEC_DETACHED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#install_spec GkeHubFeatureMembership#install_spec}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#log_denies_enabled GkeHubFeatureMembership#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#monitoring GkeHubFeatureMembership#monitoring}
        :param mutation_enabled: Enables the ability to mutate resources using Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#mutation_enabled GkeHubFeatureMembership#mutation_enabled}
        :param policy_content: policy_content block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_content GkeHubFeatureMembership#policy_content}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#referential_rules_enabled GkeHubFeatureMembership#referential_rules_enabled}
        '''
        if isinstance(monitoring, dict):
            monitoring = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring(**monitoring)
        if isinstance(policy_content, dict):
            policy_content = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent(**policy_content)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea5e5019762de17ea1154d06f206e096daa782376a20abf456cdcd78cc746d0e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#audit_interval_seconds GkeHubFeatureMembership#audit_interval_seconds}
        '''
        result = self._values.get("audit_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def constraint_violation_limit(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of audit violations to be stored in a constraint.

        If not set, the internal default of 20 will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#constraint_violation_limit GkeHubFeatureMembership#constraint_violation_limit}
        '''
        result = self._values.get("constraint_violation_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def deployment_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs"]]]:
        '''deployment_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#deployment_configs GkeHubFeatureMembership#deployment_configs}
        '''
        result = self._values.get("deployment_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs"]]], result)

    @builtins.property
    def exemptable_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of namespaces that are excluded from Policy Controller checks.

        Namespaces do not need to currently exist on the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#exemptable_namespaces GkeHubFeatureMembership#exemptable_namespaces}
        '''
        result = self._values.get("exemptable_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def install_spec(self) -> typing.Optional[builtins.str]:
        '''Configures the mode of the Policy Controller installation. Possible values: INSTALL_SPEC_UNSPECIFIED, INSTALL_SPEC_NOT_INSTALLED, INSTALL_SPEC_ENABLED, INSTALL_SPEC_SUSPENDED, INSTALL_SPEC_DETACHED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#install_spec GkeHubFeatureMembership#install_spec}
        '''
        result = self._values.get("install_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_denies_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Logs all denies and dry run failures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#log_denies_enabled GkeHubFeatureMembership#log_denies_enabled}
        '''
        result = self._values.get("log_denies_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monitoring(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring"]:
        '''monitoring block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#monitoring GkeHubFeatureMembership#monitoring}
        '''
        result = self._values.get("monitoring")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring"], result)

    @builtins.property
    def mutation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the ability to mutate resources using Policy Controller.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#mutation_enabled GkeHubFeatureMembership#mutation_enabled}
        '''
        result = self._values.get("mutation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def policy_content(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent"]:
        '''policy_content block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#policy_content GkeHubFeatureMembership#policy_content}
        '''
        result = self._values.get("policy_content")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent"], result)

    @builtins.property
    def referential_rules_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#referential_rules_enabled GkeHubFeatureMembership#referential_rules_enabled}
        '''
        result = self._values.get("referential_rules_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "component_name": "componentName",
        "container_resources": "containerResources",
        "pod_affinity": "podAffinity",
        "pod_tolerations": "podTolerations",
        "replica_count": "replicaCount",
    },
)
class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs:
    def __init__(
        self,
        *,
        component_name: builtins.str,
        container_resources: typing.Optional[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources", typing.Dict[builtins.str, typing.Any]]] = None,
        pod_affinity: typing.Optional[builtins.str] = None,
        pod_tolerations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param component_name: The name for the key in the map for which this object is mapped to in the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#component_name GkeHubFeatureMembership#component_name}
        :param container_resources: container_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#container_resources GkeHubFeatureMembership#container_resources}
        :param pod_affinity: Pod affinity configuration. Possible values: AFFINITY_UNSPECIFIED, NO_AFFINITY, ANTI_AFFINITY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#pod_affinity GkeHubFeatureMembership#pod_affinity}
        :param pod_tolerations: pod_tolerations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#pod_tolerations GkeHubFeatureMembership#pod_tolerations}
        :param replica_count: Pod replica count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#replica_count GkeHubFeatureMembership#replica_count}
        '''
        if isinstance(container_resources, dict):
            container_resources = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources(**container_resources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fdb49653da5e28442cf36d4ccfb96fb170013d408fef50eeb9086e3a7c21868)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#component_name GkeHubFeatureMembership#component_name}
        '''
        result = self._values.get("component_name")
        assert result is not None, "Required property 'component_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_resources(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources"]:
        '''container_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#container_resources GkeHubFeatureMembership#container_resources}
        '''
        result = self._values.get("container_resources")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources"], result)

    @builtins.property
    def pod_affinity(self) -> typing.Optional[builtins.str]:
        '''Pod affinity configuration. Possible values: AFFINITY_UNSPECIFIED, NO_AFFINITY, ANTI_AFFINITY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#pod_affinity GkeHubFeatureMembership#pod_affinity}
        '''
        result = self._values.get("pod_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_tolerations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations"]]]:
        '''pod_tolerations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#pod_tolerations GkeHubFeatureMembership#pod_tolerations}
        '''
        result = self._values.get("pod_tolerations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations"]]], result)

    @builtins.property
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''Pod replica count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#replica_count GkeHubFeatureMembership#replica_count}
        '''
        result = self._values.get("replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources",
    jsii_struct_bases=[],
    name_mapping={"limits": "limits", "requests": "requests"},
)
class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources:
    def __init__(
        self,
        *,
        limits: typing.Optional[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        requests: typing.Optional[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#limits GkeHubFeatureMembership#limits}
        :param requests: requests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#requests GkeHubFeatureMembership#requests}
        '''
        if isinstance(limits, dict):
            limits = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits(**limits)
        if isinstance(requests, dict):
            requests = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests(**requests)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed56e8c17f1521748e47b9ebee7c6567599ba01f0b8ee7fae08b5447bf12d9e)
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
    ) -> typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits"]:
        '''limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#limits GkeHubFeatureMembership#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits"], result)

    @builtins.property
    def requests(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"]:
        '''requests block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#requests GkeHubFeatureMembership#requests}
        '''
        result = self._values.get("requests")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory"},
)
class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#cpu GkeHubFeatureMembership#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#memory GkeHubFeatureMembership#memory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__926103cc22eb01ea27f193b61db333ace7e2c7f3b300fb41b8f330ade9911fe4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#cpu GkeHubFeatureMembership#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Memory requirement expressed in Kubernetes resource units.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#memory GkeHubFeatureMembership#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6c878bcef6d22dff5f234432da6e1599056513eaa4088494d16d4ea9750a534)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3361c0357f8638b0f700a5975fb9f692b56f2f19be61c4639203322ead96c5b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa01045f9852cca0f3c2d5012479f2785ee0fbb68ad6e9bd25bdd79c0a64cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce82cf039385b70c21add717272684679b7200c74234cf431d06de7d5765bbaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b97a2a245b0061d8752686ee629d07ea482b4aff0d857acb9329e2710831470)
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
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#cpu GkeHubFeatureMembership#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#memory GkeHubFeatureMembership#memory}
        '''
        value = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits(
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
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#cpu GkeHubFeatureMembership#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#memory GkeHubFeatureMembership#memory}
        '''
        value = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests(
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
    ) -> GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference:
        return typing.cast(GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference, jsii.get(self, "limits"))

    @builtins.property
    @jsii.member(jsii_name="requests")
    def requests(
        self,
    ) -> "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference":
        return typing.cast("GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference", jsii.get(self, "requests"))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="requestsInput")
    def requests_input(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"]:
        return typing.cast(typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests"], jsii.get(self, "requestsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b4dfc21cf740107c61149126b39651ca068aabca4ffaa1c1e6a8a64612df2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory"},
)
class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#cpu GkeHubFeatureMembership#cpu}
        :param memory: Memory requirement expressed in Kubernetes resource units. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#memory GkeHubFeatureMembership#memory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb902df6760889258910364e588414c9d4e04f557fb444d8804c242cbcdb183f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#cpu GkeHubFeatureMembership#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Memory requirement expressed in Kubernetes resource units.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#memory GkeHubFeatureMembership#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24dd0c0e46c46c941060fdd63282d6b6705618d2ce9f31b0244a106ba5c26e09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89f160ec404dace35181e7da745d0f4fdc81fd13b9e467cd49806118854eca15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb6a5d8f224c41e1120501be538c06b6f9dad44777704543473ec2d28c2b306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd42bdbe3c1bd05653bc5cb219b134803e1baabe10d5d5b99358e6c2d8a7995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af71e59600e297598663196b9db79f55d11380cac63d750777d00a07f727a4a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbc1afe1a92966fb4fe13ea8b5ae7031dd929eb9ad4f57088141a497f0a960f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf730a6aefd78af66ab55d4e5a5d820c83014dddcd7ac1a56af5feed978aad4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__582ec97c4d2c4644f6a53a481d609c10b10c64e6bb58ed50805fb858893d6642)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a4e517d09e38224dbcd3ca87410dc03f38a89e866c008990dc76443e44be664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4a69128f61d315b54d1191196acb8136d486c1e06103443a8bf12de7c76928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f37b68965467cccaf5a014b2737ad1e41734aafcf8257f2aee44c6b2570d538b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putContainerResources")
    def put_container_resources(
        self,
        *,
        limits: typing.Optional[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits, typing.Dict[builtins.str, typing.Any]]] = None,
        requests: typing.Optional[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#limits GkeHubFeatureMembership#limits}
        :param requests: requests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#requests GkeHubFeatureMembership#requests}
        '''
        value = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources(
            limits=limits, requests=requests
        )

        return typing.cast(None, jsii.invoke(self, "putContainerResources", [value]))

    @jsii.member(jsii_name="putPodTolerations")
    def put_pod_tolerations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10827d3df57dd0038588dc45d43abbbc14b2188e0e39e270ebfa1e1cb82398a8)
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
    ) -> GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference:
        return typing.cast(GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference, jsii.get(self, "containerResources"))

    @builtins.property
    @jsii.member(jsii_name="podTolerations")
    def pod_tolerations(
        self,
    ) -> "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsList":
        return typing.cast("GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsList", jsii.get(self, "podTolerations"))

    @builtins.property
    @jsii.member(jsii_name="componentNameInput")
    def component_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "componentNameInput"))

    @builtins.property
    @jsii.member(jsii_name="containerResourcesInput")
    def container_resources_input(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources], jsii.get(self, "containerResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="podAffinityInput")
    def pod_affinity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="podTolerationsInput")
    def pod_tolerations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations"]]], jsii.get(self, "podTolerationsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7fff8acabe36d0fd672acf7878370ce08a3424d073cf771654e0c44e71f344bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podAffinity")
    def pod_affinity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podAffinity"))

    @pod_affinity.setter
    def pod_affinity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f95a1a23a4bbd29cd18afe09ee5fa39ee935ae8e317ea48f563d1932213594e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaCount")
    def replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCount"))

    @replica_count.setter
    def replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f185812cc6e2e85fab435806cb67c2d6c326362ab859258fd913355624a8230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab5eec5366781648f057a2f8bf8a8f8b5672c0072fe11b89c65ab2fb8104978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations",
    jsii_struct_bases=[],
    name_mapping={
        "effect": "effect",
        "key": "key",
        "operator": "operator",
        "value": "value",
    },
)
class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations:
    def __init__(
        self,
        *,
        effect: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Matches a taint effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#effect GkeHubFeatureMembership#effect}
        :param key: Matches a taint key (not necessarily unique). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#key GkeHubFeatureMembership#key}
        :param operator: Matches a taint operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#operator GkeHubFeatureMembership#operator}
        :param value: Matches a taint value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#value GkeHubFeatureMembership#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea24440d000353baee7176bea9aea7126d9da479a0dbe6e3ddba086a1bce832)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#effect GkeHubFeatureMembership#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Matches a taint key (not necessarily unique).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#key GkeHubFeatureMembership#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Matches a taint operator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#operator GkeHubFeatureMembership#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Matches a taint value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#value GkeHubFeatureMembership#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd01e5c44e18fbb445cd0fff7fc0775a54606a534cffc3d912b2d75ff800a53b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a066b0138152ee6bb4b56b0d5a67678b9bf678ed3f5452b9b958f79bdeafa1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316b35a63fc1a661762c8c679d21a46c6eb8ef55525fb6403e460543a4308de2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5215c7d6217e3776db042c618cb81299203eae60c4860af5df000883b2751822)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32d7c494dda194cafaef263b754749f46d51576f4e8010008bd2268916473188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350ce72563a1386ea72b598e7f67e466ebd2b294f38f76ea3ffa063e842befc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b437976eed12b2b483a36a1c3b3c62cded512b3a58771a8fe6c667a607582cf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afa165162b3c48043eba90dd2e8d60fd29b6ca91568cdf64ecf5f409c8c10d2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3c68f723acea91b1b3de78dd6276e353c7edc5e1251788dac303394ea01640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744023ad0cc8d3888df82484399967f68903b70e7980b6817d37deb5df473002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1306231f6751caa33006804c21d58b133b102091f6bbffe1c5bfb51d369c656e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d56449134de040eb9ef9a27a7ebaebfc2321c4dea8d22c457edf053e734b3dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring",
    jsii_struct_bases=[],
    name_mapping={"backends": "backends"},
)
class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring:
    def __init__(
        self,
        *,
        backends: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param backends: Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#backends GkeHubFeatureMembership#backends}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e11044695fdae240dcd6806c6d6b59a317a92b67d7140fbd349f0f57301331)
            check_type(argname="argument backends", value=backends, expected_type=type_hints["backends"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backends is not None:
            self._values["backends"] = backends

    @builtins.property
    def backends(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#backends GkeHubFeatureMembership#backends}
        '''
        result = self._values.get("backends")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9a96a2547249af0ad31383fa61da4f0d21616f9942c89470a32d7be5239e2c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a01511d9d5205bddf3098a55f3d703d724bdea06229bf790588b4aa909e5bfac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backends", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63e6034a42110e137977bda7d536c381e4b258a52331276a86d9aae11d740c62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc93a4c667ded1ebba91efd8b87f5313f56d59c57b4591c23b9faa1a7b0a6c36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeploymentConfigs")
    def put_deployment_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58fe581eb44ed32ed5bd562587da86b5ff91d3afd493638f636dd5a61947242b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeploymentConfigs", [value]))

    @jsii.member(jsii_name="putMonitoring")
    def put_monitoring(
        self,
        *,
        backends: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param backends: Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#backends GkeHubFeatureMembership#backends}
        '''
        value = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring(
            backends=backends
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoring", [value]))

    @jsii.member(jsii_name="putPolicyContent")
    def put_policy_content(
        self,
        *,
        bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        template_library: typing.Optional[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bundles: bundles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#bundles GkeHubFeatureMembership#bundles}
        :param template_library: template_library block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#template_library GkeHubFeatureMembership#template_library}
        '''
        value = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent(
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
    ) -> GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList:
        return typing.cast(GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList, jsii.get(self, "deploymentConfigs"))

    @builtins.property
    @jsii.member(jsii_name="monitoring")
    def monitoring(
        self,
    ) -> GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference:
        return typing.cast(GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference, jsii.get(self, "monitoring"))

    @builtins.property
    @jsii.member(jsii_name="policyContent")
    def policy_content(
        self,
    ) -> "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference":
        return typing.cast("GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference", jsii.get(self, "policyContent"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]], jsii.get(self, "deploymentConfigsInput"))

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
    ) -> typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring], jsii.get(self, "monitoringInput"))

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
    ) -> typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent"]:
        return typing.cast(typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent"], jsii.get(self, "policyContentInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0a46dc4fa6d0d3055ceefc523abb70fe22e670798ce5d17863668ba21ef8e74b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auditIntervalSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="constraintViolationLimit")
    def constraint_violation_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "constraintViolationLimit"))

    @constraint_violation_limit.setter
    def constraint_violation_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc4fd0e37db1fb4bd22c5bcbfe7946760f30e1910aca41907e660c6a38dd871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constraintViolationLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exemptableNamespaces")
    def exemptable_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exemptableNamespaces"))

    @exemptable_namespaces.setter
    def exemptable_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6592ec8355a4cf0dffb33a50b70efb732c2477821f596dd91cbc472d64b28f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exemptableNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="installSpec")
    def install_spec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "installSpec"))

    @install_spec.setter
    def install_spec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397829d5351842ba74ef21b0848ec966e1e3a8b2e608605aa87287b23a9cca58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61093ca67a4069fc4e4d62d4b71978992203075b76deabd2e73fb1ccd4ca93d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dda3a467e685deaeccd4b4ca564ffb841d7d7d5216a777f205c555a6f5d6a3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee87d78c3c6c6a157e0d61d4a1d92d7abd4fc84b4130ff2065b0241d541397be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referentialRulesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234910481b9737dc66868b9917b1866c94d0230209871df618d77fe06d47bc53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent",
    jsii_struct_bases=[],
    name_mapping={"bundles": "bundles", "template_library": "templateLibrary"},
)
class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent:
    def __init__(
        self,
        *,
        bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        template_library: typing.Optional[typing.Union["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bundles: bundles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#bundles GkeHubFeatureMembership#bundles}
        :param template_library: template_library block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#template_library GkeHubFeatureMembership#template_library}
        '''
        if isinstance(template_library, dict):
            template_library = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary(**template_library)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f75357582cffe19f130bbd8c3d7ea68e470a5e0592bd608e5fe24d34be9b7e0)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles"]]]:
        '''bundles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#bundles GkeHubFeatureMembership#bundles}
        '''
        result = self._values.get("bundles")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles"]]], result)

    @builtins.property
    def template_library(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"]:
        '''template_library block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#template_library GkeHubFeatureMembership#template_library}
        '''
        result = self._values.get("template_library")
        return typing.cast(typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles",
    jsii_struct_bases=[],
    name_mapping={
        "bundle_name": "bundleName",
        "exempted_namespaces": "exemptedNamespaces",
    },
)
class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles:
    def __init__(
        self,
        *,
        bundle_name: builtins.str,
        exempted_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bundle_name: The name for the key in the map for which this object is mapped to in the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#bundle_name GkeHubFeatureMembership#bundle_name}
        :param exempted_namespaces: The set of namespaces to be exempted from the bundle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#exempted_namespaces GkeHubFeatureMembership#exempted_namespaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a2071453de13044f37cc04c71ae4c6fd107004fc1ccd44588d8add1e82719b7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#bundle_name GkeHubFeatureMembership#bundle_name}
        '''
        result = self._values.get("bundle_name")
        assert result is not None, "Required property 'bundle_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exempted_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of namespaces to be exempted from the bundle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#exempted_namespaces GkeHubFeatureMembership#exempted_namespaces}
        '''
        result = self._values.get("exempted_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72569a72a66a0355b793c0d01fda21f8f0cd803859fd4841d2d26bef530b71e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d325bb21e0e76de66a5db01176218b0c8009d0b2efe0b1391f2ef1dc90f28985)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fca3772d7668042a80b1a5a3f76f3cec66122d38785cdbbd3f8565727a4e4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c445998b077e2094ba5fe2767e4301789093b3da8007e0e342478f3feb211bb6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__baf44b7201cbbe3d20bd323ecab0c96701444b3e7ca1745228c571e0c463ee57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c42918f38d4b297d52d6ea423f5b6c34b8b1fdd79be1ecfbd6c7e5590545781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20e1975859b3c7dae0995bdb86063ce8bbe17e93241520e0fb5add9955f3cf7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4919229535fdd19e0dafa52d46ec5cc8cb9735cd071e68865e0db6fdc0e5fa7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exemptedNamespaces")
    def exempted_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exemptedNamespaces"))

    @exempted_namespaces.setter
    def exempted_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d2fa891b3a77b4fadae990ee9c228a1730ca99738faa73097032cdd760ab290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exemptedNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556375aedcc2007b9f290d79eaac039bd296035a80c9ef94ecc678d1b5e927fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d55b196970860ca81217885c1b76db2ef76aa0e226187e04e4ebd90bc56cda2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBundles")
    def put_bundles(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bfb9737800a2cfe163257847947a76f001c80adc8d5c9329e059561d282f940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBundles", [value]))

    @jsii.member(jsii_name="putTemplateLibrary")
    def put_template_library(
        self,
        *,
        installation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param installation: Configures the manner in which the template library is installed on the cluster. Possible values: INSTALLATION_UNSPECIFIED, NOT_INSTALLED, ALL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#installation GkeHubFeatureMembership#installation}
        '''
        value = GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary(
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
    ) -> GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList:
        return typing.cast(GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList, jsii.get(self, "bundles"))

    @builtins.property
    @jsii.member(jsii_name="templateLibrary")
    def template_library(
        self,
    ) -> "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference":
        return typing.cast("GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference", jsii.get(self, "templateLibrary"))

    @builtins.property
    @jsii.member(jsii_name="bundlesInput")
    def bundles_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]], jsii.get(self, "bundlesInput"))

    @builtins.property
    @jsii.member(jsii_name="templateLibraryInput")
    def template_library_input(
        self,
    ) -> typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"]:
        return typing.cast(typing.Optional["GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary"], jsii.get(self, "templateLibraryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21aed3e61fabbd02d140215ad7bdb6ed2c792d0ded9086c6b04d4a75d24af346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary",
    jsii_struct_bases=[],
    name_mapping={"installation": "installation"},
)
class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary:
    def __init__(self, *, installation: typing.Optional[builtins.str] = None) -> None:
        '''
        :param installation: Configures the manner in which the template library is installed on the cluster. Possible values: INSTALLATION_UNSPECIFIED, NOT_INSTALLED, ALL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#installation GkeHubFeatureMembership#installation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e0e5a5ad1322caaa0ca2557c0d28abccfefa7d0c1ba2a54d0280d6883bcea1)
            check_type(argname="argument installation", value=installation, expected_type=type_hints["installation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if installation is not None:
            self._values["installation"] = installation

    @builtins.property
    def installation(self) -> typing.Optional[builtins.str]:
        '''Configures the manner in which the template library is installed on the cluster. Possible values: INSTALLATION_UNSPECIFIED, NOT_INSTALLED, ALL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#installation GkeHubFeatureMembership#installation}
        '''
        result = self._values.get("installation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69afc6b4526bf2a516ee238ebb141c7aed7dee1e9bd08386b96ff1925c66e9ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__247bef8e0a2010341b16e7d581393a42b28a62ea4faf917d50ebc03cd34db62b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "installation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary]:
        return typing.cast(typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a98a741053e6b03ee91840afceab136a00e5ab00ebe00ad44b8bc169d08103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeHubFeatureMembershipTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#create GkeHubFeatureMembership#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#delete GkeHubFeatureMembership#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#update GkeHubFeatureMembership#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f88e210ddb5b2cfd696f243768fbc79e9e02661f9ee1cfb0fb45ac11e76669d1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#create GkeHubFeatureMembership#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#delete GkeHubFeatureMembership#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_feature_membership#update GkeHubFeatureMembership#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubFeatureMembershipTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubFeatureMembershipTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubFeatureMembership.GkeHubFeatureMembershipTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f14dbccf86469c150c3c5fad6d165a598a01298a4daf8239bdc0a9ed1701e73e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d214e166c6a9928b4828447c6b354a35458f9d1689a05a6f23f25e1ccce8b592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1aa7bdf945622531f07642fdd3d27a9589f9ec90a34750d63a4548d9461cb58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bdb16f0c8f75c83be9eca93b9167ed2a1deb8711b46b24c5e80a2707fa4759b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02188ca687120d5c6d373e88cc377b78a32a1ff82f429a09e0d1d51a16b5afc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GkeHubFeatureMembership",
    "GkeHubFeatureMembershipConfig",
    "GkeHubFeatureMembershipConfigmanagement",
    "GkeHubFeatureMembershipConfigmanagementBinauthz",
    "GkeHubFeatureMembershipConfigmanagementBinauthzOutputReference",
    "GkeHubFeatureMembershipConfigmanagementConfigSync",
    "GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides",
    "GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers",
    "GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersList",
    "GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainersOutputReference",
    "GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesList",
    "GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesOutputReference",
    "GkeHubFeatureMembershipConfigmanagementConfigSyncGit",
    "GkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference",
    "GkeHubFeatureMembershipConfigmanagementConfigSyncOci",
    "GkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference",
    "GkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference",
    "GkeHubFeatureMembershipConfigmanagementHierarchyController",
    "GkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference",
    "GkeHubFeatureMembershipConfigmanagementOutputReference",
    "GkeHubFeatureMembershipConfigmanagementPolicyController",
    "GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring",
    "GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference",
    "GkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference",
    "GkeHubFeatureMembershipMesh",
    "GkeHubFeatureMembershipMeshOutputReference",
    "GkeHubFeatureMembershipPolicycontroller",
    "GkeHubFeatureMembershipPolicycontrollerOutputReference",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimitsOutputReference",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesOutputReference",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequestsOutputReference",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsList",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsOutputReference",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsList",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerationsOutputReference",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoringOutputReference",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigOutputReference",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesList",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundlesOutputReference",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentOutputReference",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary",
    "GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibraryOutputReference",
    "GkeHubFeatureMembershipTimeouts",
    "GkeHubFeatureMembershipTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0a96870167bc32cdbfdcac336a73c454273cb1475d43f37aa777572ec248fe2b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    feature: builtins.str,
    location: builtins.str,
    membership: builtins.str,
    configmanagement: typing.Optional[typing.Union[GkeHubFeatureMembershipConfigmanagement, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    membership_location: typing.Optional[builtins.str] = None,
    mesh: typing.Optional[typing.Union[GkeHubFeatureMembershipMesh, typing.Dict[builtins.str, typing.Any]]] = None,
    policycontroller: typing.Optional[typing.Union[GkeHubFeatureMembershipPolicycontroller, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeHubFeatureMembershipTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f2aee590de1843789c8ef1dea10a2768edb3a48fee230631a1789a29505465e9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3512006e65eab1a04198554dcdfc7196f0a342cfaef0f6c6eb6fbcf93d00a44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54665bf3a6d4aac656975ceaeabc90ae7c54b56d5bc87779704ed754f305f1b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf1ded7253a545b531d5a3d11c9bfd3b06f0ee6705499a2b777c5ccf549907b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d1532736e4c16b290c3dc87d4e5ac1e2223ac2e9dc329efce725c8789cb8dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23fed7629d4b6fff80f0b47acb25749d4ccc87e5aaf8106f2d0d47126e1c5b46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00a47c92acacc4bbf6a29ebed750df6dba1e9fe1e1af9054edde70a9a4abebd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1011a9208bab4a587190961eecb477d69b286a0c9e569ed8a407abb498efcd7d(
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
    configmanagement: typing.Optional[typing.Union[GkeHubFeatureMembershipConfigmanagement, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    membership_location: typing.Optional[builtins.str] = None,
    mesh: typing.Optional[typing.Union[GkeHubFeatureMembershipMesh, typing.Dict[builtins.str, typing.Any]]] = None,
    policycontroller: typing.Optional[typing.Union[GkeHubFeatureMembershipPolicycontroller, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeHubFeatureMembershipTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1726b90741e6331d8b802a147dacd909f44fc57506ef5c7b888888f5c988c88a(
    *,
    binauthz: typing.Optional[typing.Union[GkeHubFeatureMembershipConfigmanagementBinauthz, typing.Dict[builtins.str, typing.Any]]] = None,
    config_sync: typing.Optional[typing.Union[GkeHubFeatureMembershipConfigmanagementConfigSync, typing.Dict[builtins.str, typing.Any]]] = None,
    hierarchy_controller: typing.Optional[typing.Union[GkeHubFeatureMembershipConfigmanagementHierarchyController, typing.Dict[builtins.str, typing.Any]]] = None,
    management: typing.Optional[builtins.str] = None,
    policy_controller: typing.Optional[typing.Union[GkeHubFeatureMembershipConfigmanagementPolicyController, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689b97183b28ffbb7fb03f78337b508eef556d80fbbfb22222e1c0492433ab0d(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ffabfe355074ab4fd0964eb551b45e5660ba91ef904d5e7645bee5e1e648e6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9a151294c51b24b5ab5f2f0c45f9df0a55797c8720ac6761b5bf0d1c6a7317(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d730595ca48e2913c9178174ab2734366d091e93e275236303edb3d0cb09932d(
    value: typing.Optional[GkeHubFeatureMembershipConfigmanagementBinauthz],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea17a61ff333b604f5f609632beb36f5d2f6c8c7aecdcfbf77f58e0610a1c858(
    *,
    deployment_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    git: typing.Optional[typing.Union[GkeHubFeatureMembershipConfigmanagementConfigSyncGit, typing.Dict[builtins.str, typing.Any]]] = None,
    metrics_gcp_service_account_email: typing.Optional[builtins.str] = None,
    oci: typing.Optional[typing.Union[GkeHubFeatureMembershipConfigmanagementConfigSyncOci, typing.Dict[builtins.str, typing.Any]]] = None,
    prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_format: typing.Optional[builtins.str] = None,
    stop_syncing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c04067944061820c85ab30c1b72604238f12f3131f4008fc7b1220bdedf6811(
    *,
    containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deployment_name: typing.Optional[builtins.str] = None,
    deployment_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5268a4b6a8740eb13de188830ce9a5cc2ffe86cbbcd76fa13821cf2e603f90da(
    *,
    container_name: typing.Optional[builtins.str] = None,
    cpu_limit: typing.Optional[builtins.str] = None,
    cpu_request: typing.Optional[builtins.str] = None,
    memory_limit: typing.Optional[builtins.str] = None,
    memory_request: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139c81dcc34046cf5d4eef978fabc83653ddfabdb7d86b70bf79e12cb038c954(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f5e1881514f82496a4555707157c633fac0605a8ab95c0fe545d3c9c7ac967(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89cb6d16963d80f22248c06e0a0a44831d68d154f75418f334a7be1388c3281c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8543803e3d1c6f22375c0a58e76d215c72478696a4784d2617e07649fc7382a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20148e72fba502c0a3c066e314965c190f02a4d5a69719989c1c70be32a7d90d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e06c8ddc5390e81dfc0d52029194e745b504dc0ff2fce7fa0259c0b3ceb23d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5162205821fe5e6d9ba597a66fb946d50bd135e3f95be89d55e87aa7df14acaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c79595257b1ee838f8dc15310e61d69c10202241e07b44dc1d6e5300cd4b979(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62df76314f67904fad370d1289d310f6b82f222f0fd84f681b9f03e3061e3c8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf24858006777e307a8534817930d3e6b9467a76fb9d63594456d342e7e9f2c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2529ad622160d116d10dd6905933ae929366a23e165b114069b5cdb4e0b1d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7872fa5127bd5f65af50d252415e95ccad5b23ab2f979d66fb73b5415bb3d0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c497098a75d221fb13b73de60b4c845de7b8a5e1dbcdf187466d9ec4ebba96a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ea8302569d5b5882204c4e674a4b9d6acc9e8b13bbbfc6f1b1b4b1175bb0a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f81251799d1c453aecfba0dced6802886c5f0527657193e8be5202e0bf3bc0c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60d96f925f0b61456f4966ae86a6263021f66bf29b658b09ef385962bf468e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be776327837dcffc6a9619cc9ab40f51f2406f24f739af99cfd6cf7be1537528(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9694e7b44ee234981aa8fba2fc748211ec344dd00a71083a14e93aa125d7d178(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53f501ea5fa90e9d3ffb29b67baa920611bf994d6f49cfd42a1224d4eab02ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e06f89403f613905ed357aa571d2362643d7b2c83a6d4981729b04dc531035(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c027454f41438a4f644a93dd78bbdea613bdca2a9f6d8a029352d6f3a42726(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverridesContainers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf96694e294acbbdfad57f25a5f9cd5bcbfd89b7c21362a7fe932d88a318baac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33def2f6aa92a4671fd0530ef52b5f512693311ac5a31b3b795823cd44b9e14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5099c169fa0f4015ca05b255badcd5d765de6844a5b19f619f697053c51e01c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45fcde1907aceadc36931f91434e43b71ed5f724a3f29099dd2f2132b1418d5(
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

def _typecheckingstub__4e93a801795bed8ba89a93c8a19f037c5743c6656dd953896050a00fe3020870(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc3f0ae9a2c702e07f80195b70cff72184ee9fe14ada17778d72bf53d842de9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9cded1b65cd7b6d920490ef51cb9b8b4a62cc4b402cfb5ae0ccfc78eb7184a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c68ce06c5116f35dfb61e335b6167043dea872c8f4e2d2cc5e509d1ab1230f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0402df681a8de8573980907dd7566ec3153b7bed068a140fadb8c3f3c9f0224d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1335247b25e09f81a6480add0043453b38a1b35b0f54a88bc6485ba67850413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb963cbb5aa96b67316ce1a32901d8d9a828c20429a750aa17e7b5192ccb9c6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111edf2594439a71b500a467fefbca4c92ea4ae86780cad012b7fb2fca6d4faf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5d42e87d53885d085e9780b47f2db7a4a24dc9424b3aaafb5454c79ba335641(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb53f3e0cb6d2e6a0546124a020d522e3e5bd6237fcb712cc5d73f14cf814d6(
    value: typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSyncGit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3a4a7b3c959733254173fd799a6d4898dcf72e3ed3deb45b10377120e97af6(
    *,
    gcp_service_account_email: typing.Optional[builtins.str] = None,
    policy_dir: typing.Optional[builtins.str] = None,
    secret_type: typing.Optional[builtins.str] = None,
    sync_repo: typing.Optional[builtins.str] = None,
    sync_wait_secs: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583e97dd6f32df3dd86d903ee55a2f2300ae23a548eb941e57a199531b44a028(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c8adfa87b14c2bb460dea53373c89f99c0bf7cfa0b2d4b381919c110e71480(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7492a570319296913acaa5c282dd866c6ba5c62ad92eabcd8196923ca59bb924(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e941cb3530a43f09dc77ab8586e7eabd3f49d24778ce8893e7f4933f8211cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46211483ada232d63ca3e383f9a9d5b1c0bd56c86bdacca68c5e809a70e63930(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d92a2d6f8366a34ca958f54327ad0217853e3b26a7777de439b7e9eb693bea16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c05b5c02ccf4b105d0aba002933aba4b6a6ec69becb8145ea6c6caec96aa296(
    value: typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSyncOci],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d1b9d883554c60deb9b39b296097ebf3f339d9f5d7197cb8102cba424bc4ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eaa012bff14c047901a8be007b1d305761b387fe0e77451d4ac04738fb24572(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipConfigmanagementConfigSyncDeploymentOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf5a8e9bb58a37fc888e7c09624d26009e0f7cf6a226669e09bb2556b2c035c4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fb35a93dc2e90379b9eb9800a2f8bf78a18953ee034dbc59f476e04f2fee52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5340bd24ecdb1631cbbb6422e4b2f2cca97cd2f7d6f700b444e90c54595fc8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fced9d9e9938e63c04e200b8289e225b7e22a6abc07b78ad2f80fcd40112b4ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb01f869006d2339b8c5441d1c832eba6ef3d739d385ac209e10164ddb8ea17c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c19425030df5fa09300a88138b169316edf4e9ea283576a41f878fda720714(
    value: typing.Optional[GkeHubFeatureMembershipConfigmanagementConfigSync],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e017568bbfcb14c15d2a4d678567346be6949b382cd6209db10faed33c564233(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_hierarchical_resource_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_pod_tree_labels: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c7ef1fa692b4e23e259f01627f10821dc065e87c38d07bc7382fa01fff2838(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2d3e7741072bec9b9aef10a52039aab814479c34661144c95fb490be296acc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbb48e3669dfd3b33906f0fa9c25af14cfde63ede5406afb4206d6caad057a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49365cba62adce206d95a8c06c208885be13a69b315f1724837b8db3a43af2ae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81d2f26840fdae46158abbc0760a45bc1c3c5d20b9ff5fdc660b5fd7b2aa792(
    value: typing.Optional[GkeHubFeatureMembershipConfigmanagementHierarchyController],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411225477c06591609eac2c06362e51f89640f2a71ad3455ccdca4ed3e7ed9f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f22505e4b779beba5463877980447c9ae81b1b1ee4f23c5cbc67d7e87f0e7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94d69d37fb6a1ff75c7abd0e72d41ab5fede2085aa383a94b25c6bfba4de204(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe114025004a573e4f8fc0c89205fb586bdd689d4751076ebb603f31fce17a78(
    value: typing.Optional[GkeHubFeatureMembershipConfigmanagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c85fe288cb946331d7fe57019d71fe333ab5e5510c1397dcef4afbf1a44b8e4(
    *,
    audit_interval_seconds: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitoring: typing.Optional[typing.Union[GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring, typing.Dict[builtins.str, typing.Any]]] = None,
    mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    template_library_installed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ed4a3b277ad27d138e317f8e697da34fac9fccb4dbf5fbd75678555be48212(
    *,
    backends: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2353e6d5db09eeb5175116895be93b26f4e8a7c4a17be6c1f437c111434e109(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64cc9d2e11175975480dc38401b3d99cedc549edba0e3b0d8ced9ed34100068e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e032c30be726a8f335a54fdb988b113133e5583fec57388a0a1b5d553c90f9(
    value: typing.Optional[GkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0994bdf7529627bc0302556765ff7217bed8d5dbcf92d91b398ce8dbe94b44b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4e493026b3cb63c0f3e909c339299c8dc7b323ac7258734df2a2002b7a9935(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e480722073829cec525fcb1178c1425081fbb898cfd0d277153cd90979de03(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3ef7712ef12d5212a4c2da0adccb20d7d51769125cfd8092d25e35ac4fd7a9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c494aae757905f71dfdc16af86c720ccdc625b34406c1c39bc3d2ec2db90f41(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b532a9253fd62f1854180f32ac3156b113183f3410cc1d4dbe54c7fff08224(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6272c93e23a15c18b31f0fd1de63459c305b251dab04b1acd342890e898511(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db8632b8bb218768eacd7de2580996d53642e424627c4bba42ac4cfa51ba2488(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1bad03fb85c544a0d9600facc1a7af3f2d84e6af1c231ba4b17e2ac0106320(
    value: typing.Optional[GkeHubFeatureMembershipConfigmanagementPolicyController],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5051e131e93d2f7f068ab1c2749afd37fa309d15a4264035a7949be180c0a19c(
    *,
    control_plane: typing.Optional[builtins.str] = None,
    management: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2114e1c47c0be25e1304ad402280a8eb65ebf8b7b8c9896c3ebd693ef432d3e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27526b41379459e32152af6d36d78c99278b77406f9b56ee27851d23a5df02bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__508d4422b37e89b891ce3eae26b61d911a4b0af2025b4096400d74dd27c7da3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6c2ab3c1bd8318805cf2bc3ac1f471612142a0a36ebca43ca88ba4f251efe2(
    value: typing.Optional[GkeHubFeatureMembershipMesh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea909d4447fa7ac17367510054bb5fe0b3c33f36085dfc09773653d07cc29e3(
    *,
    policy_controller_hub_config: typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig, typing.Dict[builtins.str, typing.Any]],
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673d6051e01b667f7c733d38526d4e22b9aa9473e144b1ab480a4cee4749f38c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a84382a18daa34defee08a67d45113fd36cba4b93e835e730b0d4995ed51359(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a9b2d44ea845aeb64f7b21e1622e720da9ab89c1f59746b537ccf725abb7f7(
    value: typing.Optional[GkeHubFeatureMembershipPolicycontroller],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5e5019762de17ea1154d06f206e096daa782376a20abf456cdcd78cc746d0e(
    *,
    audit_interval_seconds: typing.Optional[jsii.Number] = None,
    constraint_violation_limit: typing.Optional[jsii.Number] = None,
    deployment_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    install_spec: typing.Optional[builtins.str] = None,
    log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitoring: typing.Optional[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring, typing.Dict[builtins.str, typing.Any]]] = None,
    mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policy_content: typing.Optional[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent, typing.Dict[builtins.str, typing.Any]]] = None,
    referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fdb49653da5e28442cf36d4ccfb96fb170013d408fef50eeb9086e3a7c21868(
    *,
    component_name: builtins.str,
    container_resources: typing.Optional[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources, typing.Dict[builtins.str, typing.Any]]] = None,
    pod_affinity: typing.Optional[builtins.str] = None,
    pod_tolerations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    replica_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed56e8c17f1521748e47b9ebee7c6567599ba01f0b8ee7fae08b5447bf12d9e(
    *,
    limits: typing.Optional[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    requests: typing.Optional[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926103cc22eb01ea27f193b61db333ace7e2c7f3b300fb41b8f330ade9911fe4(
    *,
    cpu: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c878bcef6d22dff5f234432da6e1599056513eaa4088494d16d4ea9750a534(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3361c0357f8638b0f700a5975fb9f692b56f2f19be61c4639203322ead96c5b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa01045f9852cca0f3c2d5012479f2785ee0fbb68ad6e9bd25bdd79c0a64cfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce82cf039385b70c21add717272684679b7200c74234cf431d06de7d5765bbaa(
    value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b97a2a245b0061d8752686ee629d07ea482b4aff0d857acb9329e2710831470(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b4dfc21cf740107c61149126b39651ca068aabca4ffaa1c1e6a8a64612df2c(
    value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb902df6760889258910364e588414c9d4e04f557fb444d8804c242cbcdb183f(
    *,
    cpu: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24dd0c0e46c46c941060fdd63282d6b6705618d2ce9f31b0244a106ba5c26e09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f160ec404dace35181e7da745d0f4fdc81fd13b9e467cd49806118854eca15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb6a5d8f224c41e1120501be538c06b6f9dad44777704543473ec2d28c2b306(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd42bdbe3c1bd05653bc5cb219b134803e1baabe10d5d5b99358e6c2d8a7995(
    value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsContainerResourcesRequests],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af71e59600e297598663196b9db79f55d11380cac63d750777d00a07f727a4a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc1afe1a92966fb4fe13ea8b5ae7031dd929eb9ad4f57088141a497f0a960f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf730a6aefd78af66ab55d4e5a5d820c83014dddcd7ac1a56af5feed978aad4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__582ec97c4d2c4644f6a53a481d609c10b10c64e6bb58ed50805fb858893d6642(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4e517d09e38224dbcd3ca87410dc03f38a89e866c008990dc76443e44be664(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4a69128f61d315b54d1191196acb8136d486c1e06103443a8bf12de7c76928(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37b68965467cccaf5a014b2737ad1e41734aafcf8257f2aee44c6b2570d538b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10827d3df57dd0038588dc45d43abbbc14b2188e0e39e270ebfa1e1cb82398a8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fff8acabe36d0fd672acf7878370ce08a3424d073cf771654e0c44e71f344bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f95a1a23a4bbd29cd18afe09ee5fa39ee935ae8e317ea48f563d1932213594e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f185812cc6e2e85fab435806cb67c2d6c326362ab859258fd913355624a8230(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab5eec5366781648f057a2f8bf8a8f8b5672c0072fe11b89c65ab2fb8104978(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea24440d000353baee7176bea9aea7126d9da479a0dbe6e3ddba086a1bce832(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd01e5c44e18fbb445cd0fff7fc0775a54606a534cffc3d912b2d75ff800a53b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a066b0138152ee6bb4b56b0d5a67678b9bf678ed3f5452b9b958f79bdeafa1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316b35a63fc1a661762c8c679d21a46c6eb8ef55525fb6403e460543a4308de2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5215c7d6217e3776db042c618cb81299203eae60c4860af5df000883b2751822(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d7c494dda194cafaef263b754749f46d51576f4e8010008bd2268916473188(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350ce72563a1386ea72b598e7f67e466ebd2b294f38f76ea3ffa063e842befc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b437976eed12b2b483a36a1c3b3c62cded512b3a58771a8fe6c667a607582cf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa165162b3c48043eba90dd2e8d60fd29b6ca91568cdf64ecf5f409c8c10d2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3c68f723acea91b1b3de78dd6276e353c7edc5e1251788dac303394ea01640(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744023ad0cc8d3888df82484399967f68903b70e7980b6817d37deb5df473002(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1306231f6751caa33006804c21d58b133b102091f6bbffe1c5bfb51d369c656e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d56449134de040eb9ef9a27a7ebaebfc2321c4dea8d22c457edf053e734b3dd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigsPodTolerations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e11044695fdae240dcd6806c6d6b59a317a92b67d7140fbd349f0f57301331(
    *,
    backends: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a96a2547249af0ad31383fa61da4f0d21616f9942c89470a32d7be5239e2c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01511d9d5205bddf3098a55f3d703d724bdea06229bf790588b4aa909e5bfac(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e6034a42110e137977bda7d536c381e4b258a52331276a86d9aae11d740c62(
    value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigMonitoring],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc93a4c667ded1ebba91efd8b87f5313f56d59c57b4591c23b9faa1a7b0a6c36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58fe581eb44ed32ed5bd562587da86b5ff91d3afd493638f636dd5a61947242b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigDeploymentConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a46dc4fa6d0d3055ceefc523abb70fe22e670798ce5d17863668ba21ef8e74b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc4fd0e37db1fb4bd22c5bcbfe7946760f30e1910aca41907e660c6a38dd871(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6592ec8355a4cf0dffb33a50b70efb732c2477821f596dd91cbc472d64b28f20(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397829d5351842ba74ef21b0848ec966e1e3a8b2e608605aa87287b23a9cca58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61093ca67a4069fc4e4d62d4b71978992203075b76deabd2e73fb1ccd4ca93d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dda3a467e685deaeccd4b4ca564ffb841d7d7d5216a777f205c555a6f5d6a3c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee87d78c3c6c6a157e0d61d4a1d92d7abd4fc84b4130ff2065b0241d541397be(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234910481b9737dc66868b9917b1866c94d0230209871df618d77fe06d47bc53(
    value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f75357582cffe19f130bbd8c3d7ea68e470a5e0592bd608e5fe24d34be9b7e0(
    *,
    bundles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles, typing.Dict[builtins.str, typing.Any]]]]] = None,
    template_library: typing.Optional[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2071453de13044f37cc04c71ae4c6fd107004fc1ccd44588d8add1e82719b7(
    *,
    bundle_name: builtins.str,
    exempted_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72569a72a66a0355b793c0d01fda21f8f0cd803859fd4841d2d26bef530b71e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d325bb21e0e76de66a5db01176218b0c8009d0b2efe0b1391f2ef1dc90f28985(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fca3772d7668042a80b1a5a3f76f3cec66122d38785cdbbd3f8565727a4e4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c445998b077e2094ba5fe2767e4301789093b3da8007e0e342478f3feb211bb6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf44b7201cbbe3d20bd323ecab0c96701444b3e7ca1745228c571e0c463ee57(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c42918f38d4b297d52d6ea423f5b6c34b8b1fdd79be1ecfbd6c7e5590545781(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e1975859b3c7dae0995bdb86063ce8bbe17e93241520e0fb5add9955f3cf7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4919229535fdd19e0dafa52d46ec5cc8cb9735cd071e68865e0db6fdc0e5fa7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2fa891b3a77b4fadae990ee9c228a1730ca99738faa73097032cdd760ab290(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556375aedcc2007b9f290d79eaac039bd296035a80c9ef94ecc678d1b5e927fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d55b196970860ca81217885c1b76db2ef76aa0e226187e04e4ebd90bc56cda2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bfb9737800a2cfe163257847947a76f001c80adc8d5c9329e059561d282f940(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentBundles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21aed3e61fabbd02d140215ad7bdb6ed2c792d0ded9086c6b04d4a75d24af346(
    value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e0e5a5ad1322caaa0ca2557c0d28abccfefa7d0c1ba2a54d0280d6883bcea1(
    *,
    installation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69afc6b4526bf2a516ee238ebb141c7aed7dee1e9bd08386b96ff1925c66e9ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247bef8e0a2010341b16e7d581393a42b28a62ea4faf917d50ebc03cd34db62b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a98a741053e6b03ee91840afceab136a00e5ab00ebe00ad44b8bc169d08103(
    value: typing.Optional[GkeHubFeatureMembershipPolicycontrollerPolicyControllerHubConfigPolicyContentTemplateLibrary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88e210ddb5b2cfd696f243768fbc79e9e02661f9ee1cfb0fb45ac11e76669d1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f14dbccf86469c150c3c5fad6d165a598a01298a4daf8239bdc0a9ed1701e73e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d214e166c6a9928b4828447c6b354a35458f9d1689a05a6f23f25e1ccce8b592(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1aa7bdf945622531f07642fdd3d27a9589f9ec90a34750d63a4548d9461cb58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bdb16f0c8f75c83be9eca93b9167ed2a1deb8711b46b24c5e80a2707fa4759b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02188ca687120d5c6d373e88cc377b78a32a1ff82f429a09e0d1d51a16b5afc6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubFeatureMembershipTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
