r'''
# `google_gke_hub_membership`

Refer to the Terraform Registry for docs: [`google_gke_hub_membership`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership).
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


class GkeHubMembership(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubMembership.GkeHubMembership",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership google_gke_hub_membership}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        membership_id: builtins.str,
        authority: typing.Optional[typing.Union["GkeHubMembershipAuthority", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint: typing.Optional[typing.Union["GkeHubMembershipEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeHubMembershipTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership google_gke_hub_membership} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param membership_id: The client-provided identifier of the membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#membership_id GkeHubMembership#membership_id}
        :param authority: authority block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#authority GkeHubMembership#authority}
        :param endpoint: endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#endpoint GkeHubMembership#endpoint}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#id GkeHubMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels to apply to this membership. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#labels GkeHubMembership#labels}
        :param location: Location of the membership. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#location GkeHubMembership#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#project GkeHubMembership#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#timeouts GkeHubMembership#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff48f11d1d879c98fff5396ed571d491219dcd4a6248b9bebdc846ae6beae10)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GkeHubMembershipConfig(
            membership_id=membership_id,
            authority=authority,
            endpoint=endpoint,
            id=id,
            labels=labels,
            location=location,
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
        '''Generates CDKTF code for importing a GkeHubMembership resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeHubMembership to import.
        :param import_from_id: The id of the existing GkeHubMembership that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeHubMembership to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d7aac6f87c91f608820593468649e3950485d131a21bc9cc967149ee371bbe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthority")
    def put_authority(self, *, issuer: builtins.str) -> None:
        '''
        :param issuer: A JSON Web Token (JWT) issuer URI. 'issuer' must start with 'https://' and // be a valid with length <2000 characters. For example: 'https://container.googleapis.com/v1/projects/my-project/locations/us-west1/clusters/my-cluster'. If the cluster is provisioned with Terraform, this is '"https://container.googleapis.com/v1/${google_container_cluster.my-cluster.id}"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#issuer GkeHubMembership#issuer}
        '''
        value = GkeHubMembershipAuthority(issuer=issuer)

        return typing.cast(None, jsii.invoke(self, "putAuthority", [value]))

    @jsii.member(jsii_name="putEndpoint")
    def put_endpoint(
        self,
        *,
        gke_cluster: typing.Optional[typing.Union["GkeHubMembershipEndpointGkeCluster", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gke_cluster: gke_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#gke_cluster GkeHubMembership#gke_cluster}
        '''
        value = GkeHubMembershipEndpoint(gke_cluster=gke_cluster)

        return typing.cast(None, jsii.invoke(self, "putEndpoint", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#create GkeHubMembership#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#delete GkeHubMembership#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#update GkeHubMembership#update}.
        '''
        value = GkeHubMembershipTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAuthority")
    def reset_authority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthority", []))

    @jsii.member(jsii_name="resetEndpoint")
    def reset_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpoint", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

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
    @jsii.member(jsii_name="authority")
    def authority(self) -> "GkeHubMembershipAuthorityOutputReference":
        return typing.cast("GkeHubMembershipAuthorityOutputReference", jsii.get(self, "authority"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> "GkeHubMembershipEndpointOutputReference":
        return typing.cast("GkeHubMembershipEndpointOutputReference", jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GkeHubMembershipTimeoutsOutputReference":
        return typing.cast("GkeHubMembershipTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="authorityInput")
    def authority_input(self) -> typing.Optional["GkeHubMembershipAuthority"]:
        return typing.cast(typing.Optional["GkeHubMembershipAuthority"], jsii.get(self, "authorityInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional["GkeHubMembershipEndpoint"]:
        return typing.cast(typing.Optional["GkeHubMembershipEndpoint"], jsii.get(self, "endpointInput"))

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
    @jsii.member(jsii_name="membershipIdInput")
    def membership_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "membershipIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeHubMembershipTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeHubMembershipTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5551e13de782ec79beaaa544faf155d58361a11492e386f7c516299bdf35ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__154f993bcedfee4511de8b637ade76f621a0938a7f5e22b8f574ed5914054fad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e363f7fe009a5043a4ae1b4db95165c7d58609b3da84a5bfbf471ce0bdd9f040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="membershipId")
    def membership_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "membershipId"))

    @membership_id.setter
    def membership_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a65b258face7db57cca1ec6141d7d459faf0322ac4b27b444cf68ac4b36dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membershipId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__695b8e64c43b0215384946994e2b7228403bea797c4de99df6f326c9ac1eeae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubMembership.GkeHubMembershipAuthority",
    jsii_struct_bases=[],
    name_mapping={"issuer": "issuer"},
)
class GkeHubMembershipAuthority:
    def __init__(self, *, issuer: builtins.str) -> None:
        '''
        :param issuer: A JSON Web Token (JWT) issuer URI. 'issuer' must start with 'https://' and // be a valid with length <2000 characters. For example: 'https://container.googleapis.com/v1/projects/my-project/locations/us-west1/clusters/my-cluster'. If the cluster is provisioned with Terraform, this is '"https://container.googleapis.com/v1/${google_container_cluster.my-cluster.id}"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#issuer GkeHubMembership#issuer}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052f55a228f03c21ff6ec3e793450f8f9dbc2a9ddf3d83d94ad9e877af83e0bf)
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "issuer": issuer,
        }

    @builtins.property
    def issuer(self) -> builtins.str:
        '''A JSON Web Token (JWT) issuer URI.

        'issuer' must start with 'https://' and // be a valid
        with length <2000 characters. For example: 'https://container.googleapis.com/v1/projects/my-project/locations/us-west1/clusters/my-cluster'. If the cluster is provisioned with Terraform, this is '"https://container.googleapis.com/v1/${google_container_cluster.my-cluster.id}"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#issuer GkeHubMembership#issuer}
        '''
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubMembershipAuthority(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubMembershipAuthorityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubMembership.GkeHubMembershipAuthorityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36406406d04a7b1372e60403651673334c0fab23a4f78d6e445a4c36410e0fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2342b612289e5d2b2d09860e8a7586caf8805be2a55985512a6d56c683fd0ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubMembershipAuthority]:
        return typing.cast(typing.Optional[GkeHubMembershipAuthority], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GkeHubMembershipAuthority]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada4547da959ea258fa78b9add0dace42baa8cb5b8e0806d1e09085ab000ca75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubMembership.GkeHubMembershipConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "membership_id": "membershipId",
        "authority": "authority",
        "endpoint": "endpoint",
        "id": "id",
        "labels": "labels",
        "location": "location",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GkeHubMembershipConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        membership_id: builtins.str,
        authority: typing.Optional[typing.Union[GkeHubMembershipAuthority, typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint: typing.Optional[typing.Union["GkeHubMembershipEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeHubMembershipTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param membership_id: The client-provided identifier of the membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#membership_id GkeHubMembership#membership_id}
        :param authority: authority block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#authority GkeHubMembership#authority}
        :param endpoint: endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#endpoint GkeHubMembership#endpoint}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#id GkeHubMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels to apply to this membership. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#labels GkeHubMembership#labels}
        :param location: Location of the membership. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#location GkeHubMembership#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#project GkeHubMembership#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#timeouts GkeHubMembership#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(authority, dict):
            authority = GkeHubMembershipAuthority(**authority)
        if isinstance(endpoint, dict):
            endpoint = GkeHubMembershipEndpoint(**endpoint)
        if isinstance(timeouts, dict):
            timeouts = GkeHubMembershipTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f990520ce66637ca54dc9d1affb3979206597d3afbe6e83697cc261393e259)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument membership_id", value=membership_id, expected_type=type_hints["membership_id"])
            check_type(argname="argument authority", value=authority, expected_type=type_hints["authority"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "membership_id": membership_id,
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
        if authority is not None:
            self._values["authority"] = authority
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
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
    def membership_id(self) -> builtins.str:
        '''The client-provided identifier of the membership.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#membership_id GkeHubMembership#membership_id}
        '''
        result = self._values.get("membership_id")
        assert result is not None, "Required property 'membership_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authority(self) -> typing.Optional[GkeHubMembershipAuthority]:
        '''authority block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#authority GkeHubMembership#authority}
        '''
        result = self._values.get("authority")
        return typing.cast(typing.Optional[GkeHubMembershipAuthority], result)

    @builtins.property
    def endpoint(self) -> typing.Optional["GkeHubMembershipEndpoint"]:
        '''endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#endpoint GkeHubMembership#endpoint}
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional["GkeHubMembershipEndpoint"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#id GkeHubMembership#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to this membership.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#labels GkeHubMembership#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Location of the membership. The default value is 'global'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#location GkeHubMembership#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#project GkeHubMembership#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeHubMembershipTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#timeouts GkeHubMembership#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeHubMembershipTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubMembershipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubMembership.GkeHubMembershipEndpoint",
    jsii_struct_bases=[],
    name_mapping={"gke_cluster": "gkeCluster"},
)
class GkeHubMembershipEndpoint:
    def __init__(
        self,
        *,
        gke_cluster: typing.Optional[typing.Union["GkeHubMembershipEndpointGkeCluster", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gke_cluster: gke_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#gke_cluster GkeHubMembership#gke_cluster}
        '''
        if isinstance(gke_cluster, dict):
            gke_cluster = GkeHubMembershipEndpointGkeCluster(**gke_cluster)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da794a3175e7f252522e72e5affbea1e5c8a0a03dedc341872da5efa3e58f033)
            check_type(argname="argument gke_cluster", value=gke_cluster, expected_type=type_hints["gke_cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gke_cluster is not None:
            self._values["gke_cluster"] = gke_cluster

    @builtins.property
    def gke_cluster(self) -> typing.Optional["GkeHubMembershipEndpointGkeCluster"]:
        '''gke_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#gke_cluster GkeHubMembership#gke_cluster}
        '''
        result = self._values.get("gke_cluster")
        return typing.cast(typing.Optional["GkeHubMembershipEndpointGkeCluster"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubMembershipEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubMembership.GkeHubMembershipEndpointGkeCluster",
    jsii_struct_bases=[],
    name_mapping={"resource_link": "resourceLink"},
)
class GkeHubMembershipEndpointGkeCluster:
    def __init__(self, *, resource_link: builtins.str) -> None:
        '''
        :param resource_link: Self-link of the GCP resource for the GKE cluster. For example: '//container.googleapis.com/projects/my-project/locations/us-west1-a/clusters/my-cluster'. It can be at the most 1000 characters in length. If the cluster is provisioned with Terraform, this can be '"//container.googleapis.com/${google_container_cluster.my-cluster.id}"' or 'google_container_cluster.my-cluster.id'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#resource_link GkeHubMembership#resource_link}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d9a9a2040189ffb27b909b5ee19ae3accdba93160b5b51c844760e9c3e2005)
            check_type(argname="argument resource_link", value=resource_link, expected_type=type_hints["resource_link"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_link": resource_link,
        }

    @builtins.property
    def resource_link(self) -> builtins.str:
        '''Self-link of the GCP resource for the GKE cluster.

        For example: '//container.googleapis.com/projects/my-project/locations/us-west1-a/clusters/my-cluster'.
        It can be at the most 1000 characters in length. If the cluster is provisioned with Terraform,
        this can be '"//container.googleapis.com/${google_container_cluster.my-cluster.id}"' or
        'google_container_cluster.my-cluster.id'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#resource_link GkeHubMembership#resource_link}
        '''
        result = self._values.get("resource_link")
        assert result is not None, "Required property 'resource_link' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubMembershipEndpointGkeCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubMembershipEndpointGkeClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubMembership.GkeHubMembershipEndpointGkeClusterOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46903349733614e1033affa85a052e3498e2c2572bdc4ae420c7939bbebdb40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceLinkInput")
    def resource_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceLink")
    def resource_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceLink"))

    @resource_link.setter
    def resource_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d382c38b040ab4c1da977a8801d7fab85a09f9dfc806fbff303817436a6fec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubMembershipEndpointGkeCluster]:
        return typing.cast(typing.Optional[GkeHubMembershipEndpointGkeCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeHubMembershipEndpointGkeCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0673d3dc446040668f1cb2dd10eb37d6739fad1681a173369425ef8aed2da97c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeHubMembershipEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubMembership.GkeHubMembershipEndpointOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3afe013829f24e43d54518be7e6ffdaddabe18489f9638b0b3be0600437235b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGkeCluster")
    def put_gke_cluster(self, *, resource_link: builtins.str) -> None:
        '''
        :param resource_link: Self-link of the GCP resource for the GKE cluster. For example: '//container.googleapis.com/projects/my-project/locations/us-west1-a/clusters/my-cluster'. It can be at the most 1000 characters in length. If the cluster is provisioned with Terraform, this can be '"//container.googleapis.com/${google_container_cluster.my-cluster.id}"' or 'google_container_cluster.my-cluster.id'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#resource_link GkeHubMembership#resource_link}
        '''
        value = GkeHubMembershipEndpointGkeCluster(resource_link=resource_link)

        return typing.cast(None, jsii.invoke(self, "putGkeCluster", [value]))

    @jsii.member(jsii_name="resetGkeCluster")
    def reset_gke_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGkeCluster", []))

    @builtins.property
    @jsii.member(jsii_name="gkeCluster")
    def gke_cluster(self) -> GkeHubMembershipEndpointGkeClusterOutputReference:
        return typing.cast(GkeHubMembershipEndpointGkeClusterOutputReference, jsii.get(self, "gkeCluster"))

    @builtins.property
    @jsii.member(jsii_name="gkeClusterInput")
    def gke_cluster_input(self) -> typing.Optional[GkeHubMembershipEndpointGkeCluster]:
        return typing.cast(typing.Optional[GkeHubMembershipEndpointGkeCluster], jsii.get(self, "gkeClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeHubMembershipEndpoint]:
        return typing.cast(typing.Optional[GkeHubMembershipEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GkeHubMembershipEndpoint]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5181f878f7dff7e647f393612a61ed26f27d9a45cba9bf4466444241ac49e62d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeHubMembership.GkeHubMembershipTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeHubMembershipTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#create GkeHubMembership#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#delete GkeHubMembership#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#update GkeHubMembership#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963684599b21f59bb1d2780acabddd67ca76232459d383690285cc4431b1a758)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#create GkeHubMembership#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#delete GkeHubMembership#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_hub_membership#update GkeHubMembership#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeHubMembershipTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeHubMembershipTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeHubMembership.GkeHubMembershipTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4099018dd92884ba6a95738f7f81ae24f79196bef2efeb5f910384f415ba866)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68cb1a7a0f799c7557db1a430d86b61a3a8f61c99b0dc426a18e6417f1896cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baaaba49205b4946ca532581c430b68bbe60a95a3f6180f5b3cb590714267d53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a32fa37740cd32c8252f63b2ce702c607475a70f83730b9b620faf94b2b4afd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubMembershipTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubMembershipTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubMembershipTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__800d375473a4fe6f9212374f1bbe7bb7df6f421d062b60606e965fa8d367a107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GkeHubMembership",
    "GkeHubMembershipAuthority",
    "GkeHubMembershipAuthorityOutputReference",
    "GkeHubMembershipConfig",
    "GkeHubMembershipEndpoint",
    "GkeHubMembershipEndpointGkeCluster",
    "GkeHubMembershipEndpointGkeClusterOutputReference",
    "GkeHubMembershipEndpointOutputReference",
    "GkeHubMembershipTimeouts",
    "GkeHubMembershipTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__cff48f11d1d879c98fff5396ed571d491219dcd4a6248b9bebdc846ae6beae10(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    membership_id: builtins.str,
    authority: typing.Optional[typing.Union[GkeHubMembershipAuthority, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint: typing.Optional[typing.Union[GkeHubMembershipEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeHubMembershipTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__81d7aac6f87c91f608820593468649e3950485d131a21bc9cc967149ee371bbe(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5551e13de782ec79beaaa544faf155d58361a11492e386f7c516299bdf35ca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154f993bcedfee4511de8b637ade76f621a0938a7f5e22b8f574ed5914054fad(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e363f7fe009a5043a4ae1b4db95165c7d58609b3da84a5bfbf471ce0bdd9f040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a65b258face7db57cca1ec6141d7d459faf0322ac4b27b444cf68ac4b36dc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__695b8e64c43b0215384946994e2b7228403bea797c4de99df6f326c9ac1eeae9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052f55a228f03c21ff6ec3e793450f8f9dbc2a9ddf3d83d94ad9e877af83e0bf(
    *,
    issuer: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36406406d04a7b1372e60403651673334c0fab23a4f78d6e445a4c36410e0fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2342b612289e5d2b2d09860e8a7586caf8805be2a55985512a6d56c683fd0ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada4547da959ea258fa78b9add0dace42baa8cb5b8e0806d1e09085ab000ca75(
    value: typing.Optional[GkeHubMembershipAuthority],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f990520ce66637ca54dc9d1affb3979206597d3afbe6e83697cc261393e259(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    membership_id: builtins.str,
    authority: typing.Optional[typing.Union[GkeHubMembershipAuthority, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint: typing.Optional[typing.Union[GkeHubMembershipEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeHubMembershipTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da794a3175e7f252522e72e5affbea1e5c8a0a03dedc341872da5efa3e58f033(
    *,
    gke_cluster: typing.Optional[typing.Union[GkeHubMembershipEndpointGkeCluster, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d9a9a2040189ffb27b909b5ee19ae3accdba93160b5b51c844760e9c3e2005(
    *,
    resource_link: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46903349733614e1033affa85a052e3498e2c2572bdc4ae420c7939bbebdb40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d382c38b040ab4c1da977a8801d7fab85a09f9dfc806fbff303817436a6fec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0673d3dc446040668f1cb2dd10eb37d6739fad1681a173369425ef8aed2da97c(
    value: typing.Optional[GkeHubMembershipEndpointGkeCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3afe013829f24e43d54518be7e6ffdaddabe18489f9638b0b3be0600437235b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5181f878f7dff7e647f393612a61ed26f27d9a45cba9bf4466444241ac49e62d(
    value: typing.Optional[GkeHubMembershipEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963684599b21f59bb1d2780acabddd67ca76232459d383690285cc4431b1a758(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4099018dd92884ba6a95738f7f81ae24f79196bef2efeb5f910384f415ba866(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68cb1a7a0f799c7557db1a430d86b61a3a8f61c99b0dc426a18e6417f1896cd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baaaba49205b4946ca532581c430b68bbe60a95a3f6180f5b3cb590714267d53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a32fa37740cd32c8252f63b2ce702c607475a70f83730b9b620faf94b2b4afd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800d375473a4fe6f9212374f1bbe7bb7df6f421d062b60606e965fa8d367a107(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeHubMembershipTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
