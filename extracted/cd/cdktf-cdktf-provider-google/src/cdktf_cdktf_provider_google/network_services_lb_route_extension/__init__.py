r'''
# `google_network_services_lb_route_extension`

Refer to the Terraform Registry for docs: [`google_network_services_lb_route_extension`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension).
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


class NetworkServicesLbRouteExtension(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbRouteExtension.NetworkServicesLbRouteExtension",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension google_network_services_lb_route_extension}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        extension_chains: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesLbRouteExtensionExtensionChains", typing.Dict[builtins.str, typing.Any]]]],
        forwarding_rules: typing.Sequence[builtins.str],
        load_balancing_scheme: builtins.str,
        location: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesLbRouteExtensionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension google_network_services_lb_route_extension} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param extension_chains: extension_chains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#extension_chains NetworkServicesLbRouteExtension#extension_chains}
        :param forwarding_rules: A list of references to the forwarding rules to which this service extension is attached to. At least one forwarding rule is required. There can be only one LbRouteExtension resource per forwarding rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#forwarding_rules NetworkServicesLbRouteExtension#forwarding_rules}
        :param load_balancing_scheme: All backend services and forwarding rules referenced by this extension must share the same load balancing scheme. For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_ and `Supported application load balancers <https://cloud.google.com/service-extensions/docs/callouts-overview#supported-lbs>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#load_balancing_scheme NetworkServicesLbRouteExtension#load_balancing_scheme}
        :param location: The location of the route extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#location NetworkServicesLbRouteExtension#location}
        :param name: Name of the LbRouteExtension resource in the following format: projects/{project}/locations/{location}/lbRouteExtensions/{lbRouteExtension}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#name NetworkServicesLbRouteExtension#name}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#description NetworkServicesLbRouteExtension#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#id NetworkServicesLbRouteExtension#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the LbRouteExtension resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#labels NetworkServicesLbRouteExtension#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#project NetworkServicesLbRouteExtension#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#timeouts NetworkServicesLbRouteExtension#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96e7dc6db33f67c5ff3dd949adba606cc53ef713670c0b65bb07e2d3bea38ca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkServicesLbRouteExtensionConfig(
            extension_chains=extension_chains,
            forwarding_rules=forwarding_rules,
            load_balancing_scheme=load_balancing_scheme,
            location=location,
            name=name,
            description=description,
            id=id,
            labels=labels,
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
        '''Generates CDKTF code for importing a NetworkServicesLbRouteExtension resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkServicesLbRouteExtension to import.
        :param import_from_id: The id of the existing NetworkServicesLbRouteExtension that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkServicesLbRouteExtension to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2996ad5413810527e2afd9276d7eb2cec28a1c139d8cef7ecf041d229d5e0db6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExtensionChains")
    def put_extension_chains(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesLbRouteExtensionExtensionChains", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b66b16bc56f5e780e319701e96e815b49adf1f6998b157af42c6f0d55e214e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtensionChains", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#create NetworkServicesLbRouteExtension#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#delete NetworkServicesLbRouteExtension#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#update NetworkServicesLbRouteExtension#update}.
        '''
        value = NetworkServicesLbRouteExtensionTimeouts(
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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="extensionChains")
    def extension_chains(self) -> "NetworkServicesLbRouteExtensionExtensionChainsList":
        return typing.cast("NetworkServicesLbRouteExtensionExtensionChainsList", jsii.get(self, "extensionChains"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkServicesLbRouteExtensionTimeoutsOutputReference":
        return typing.cast("NetworkServicesLbRouteExtensionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionChainsInput")
    def extension_chains_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesLbRouteExtensionExtensionChains"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesLbRouteExtensionExtensionChains"]]], jsii.get(self, "extensionChainsInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardingRulesInput")
    def forwarding_rules_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "forwardingRulesInput"))

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
    @jsii.member(jsii_name="loadBalancingSchemeInput")
    def load_balancing_scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancingSchemeInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesLbRouteExtensionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesLbRouteExtensionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a0ec95a91d554dead6637435fb5147666d13999523d78b4142a59a831d3408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardingRules")
    def forwarding_rules(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "forwardingRules"))

    @forwarding_rules.setter
    def forwarding_rules(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33e459ae7013ee6e8d25c04841560c7ddc35318327bcdd6d25e8d91e7b580be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardingRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f701bf30bbe09bf3d554292f90dbd16f3c381c0b6ed87a77d78dcdc45828d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78ec63f4962bd4c224328775b93d8fab4d69245d0c3afab93cd713218742b87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d20ed61c56ee1f19c28eca35631212bae33555e4fcffb4f128dd156d41478265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec82c8a03283a4ef9b61b2dcdb3d9a1a9f20beb65b4cd863fe330826881bd77c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eda6da4b0a3f821d2b5ab1e548f2a0b63e70060f292cfd9ee185d3ec86eec8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba71bf37472d80d5b63aaa6bf79884e3a44f9d5245525ebd34c49e99a30f6d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesLbRouteExtension.NetworkServicesLbRouteExtensionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "extension_chains": "extensionChains",
        "forwarding_rules": "forwardingRules",
        "load_balancing_scheme": "loadBalancingScheme",
        "location": "location",
        "name": "name",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class NetworkServicesLbRouteExtensionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        extension_chains: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesLbRouteExtensionExtensionChains", typing.Dict[builtins.str, typing.Any]]]],
        forwarding_rules: typing.Sequence[builtins.str],
        load_balancing_scheme: builtins.str,
        location: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesLbRouteExtensionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param extension_chains: extension_chains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#extension_chains NetworkServicesLbRouteExtension#extension_chains}
        :param forwarding_rules: A list of references to the forwarding rules to which this service extension is attached to. At least one forwarding rule is required. There can be only one LbRouteExtension resource per forwarding rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#forwarding_rules NetworkServicesLbRouteExtension#forwarding_rules}
        :param load_balancing_scheme: All backend services and forwarding rules referenced by this extension must share the same load balancing scheme. For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_ and `Supported application load balancers <https://cloud.google.com/service-extensions/docs/callouts-overview#supported-lbs>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#load_balancing_scheme NetworkServicesLbRouteExtension#load_balancing_scheme}
        :param location: The location of the route extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#location NetworkServicesLbRouteExtension#location}
        :param name: Name of the LbRouteExtension resource in the following format: projects/{project}/locations/{location}/lbRouteExtensions/{lbRouteExtension}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#name NetworkServicesLbRouteExtension#name}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#description NetworkServicesLbRouteExtension#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#id NetworkServicesLbRouteExtension#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the LbRouteExtension resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#labels NetworkServicesLbRouteExtension#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#project NetworkServicesLbRouteExtension#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#timeouts NetworkServicesLbRouteExtension#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = NetworkServicesLbRouteExtensionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e052feb5a7538305beb5e39440ab18362b1ed43de5a61cb450f1249de476837)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument extension_chains", value=extension_chains, expected_type=type_hints["extension_chains"])
            check_type(argname="argument forwarding_rules", value=forwarding_rules, expected_type=type_hints["forwarding_rules"])
            check_type(argname="argument load_balancing_scheme", value=load_balancing_scheme, expected_type=type_hints["load_balancing_scheme"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "extension_chains": extension_chains,
            "forwarding_rules": forwarding_rules,
            "load_balancing_scheme": load_balancing_scheme,
            "location": location,
            "name": name,
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
    def extension_chains(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesLbRouteExtensionExtensionChains"]]:
        '''extension_chains block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#extension_chains NetworkServicesLbRouteExtension#extension_chains}
        '''
        result = self._values.get("extension_chains")
        assert result is not None, "Required property 'extension_chains' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesLbRouteExtensionExtensionChains"]], result)

    @builtins.property
    def forwarding_rules(self) -> typing.List[builtins.str]:
        '''A list of references to the forwarding rules to which this service extension is attached to.

        At least one forwarding rule is required. There can be only one LbRouteExtension resource per forwarding rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#forwarding_rules NetworkServicesLbRouteExtension#forwarding_rules}
        '''
        result = self._values.get("forwarding_rules")
        assert result is not None, "Required property 'forwarding_rules' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def load_balancing_scheme(self) -> builtins.str:
        '''All backend services and forwarding rules referenced by this extension must share the same load balancing scheme.

        For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_ and
        `Supported application load balancers <https://cloud.google.com/service-extensions/docs/callouts-overview#supported-lbs>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#load_balancing_scheme NetworkServicesLbRouteExtension#load_balancing_scheme}
        '''
        result = self._values.get("load_balancing_scheme")
        assert result is not None, "Required property 'load_balancing_scheme' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the route extension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#location NetworkServicesLbRouteExtension#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the LbRouteExtension resource in the following format: projects/{project}/locations/{location}/lbRouteExtensions/{lbRouteExtension}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#name NetworkServicesLbRouteExtension#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#description NetworkServicesLbRouteExtension#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#id NetworkServicesLbRouteExtension#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of labels associated with the LbRouteExtension resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#labels NetworkServicesLbRouteExtension#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#project NetworkServicesLbRouteExtension#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkServicesLbRouteExtensionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#timeouts NetworkServicesLbRouteExtension#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkServicesLbRouteExtensionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesLbRouteExtensionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesLbRouteExtension.NetworkServicesLbRouteExtensionExtensionChains",
    jsii_struct_bases=[],
    name_mapping={
        "extensions": "extensions",
        "match_condition": "matchCondition",
        "name": "name",
    },
)
class NetworkServicesLbRouteExtensionExtensionChains:
    def __init__(
        self,
        *,
        extensions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesLbRouteExtensionExtensionChainsExtensions", typing.Dict[builtins.str, typing.Any]]]],
        match_condition: typing.Union["NetworkServicesLbRouteExtensionExtensionChainsMatchCondition", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param extensions: extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#extensions NetworkServicesLbRouteExtension#extensions}
        :param match_condition: match_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#match_condition NetworkServicesLbRouteExtension#match_condition}
        :param name: The name for this extension chain. The name is logged as part of the HTTP request logs. The name must conform with RFC-1034, is restricted to lower-cased letters, numbers and hyphens, and can have a maximum length of 63 characters. Additionally, the first character must be a letter and the last character must be a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#name NetworkServicesLbRouteExtension#name}
        '''
        if isinstance(match_condition, dict):
            match_condition = NetworkServicesLbRouteExtensionExtensionChainsMatchCondition(**match_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff06c678ed2ac5096c426e478ec66d799b096325bb854d15d17eb16d1e01237)
            check_type(argname="argument extensions", value=extensions, expected_type=type_hints["extensions"])
            check_type(argname="argument match_condition", value=match_condition, expected_type=type_hints["match_condition"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "extensions": extensions,
            "match_condition": match_condition,
            "name": name,
        }

    @builtins.property
    def extensions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesLbRouteExtensionExtensionChainsExtensions"]]:
        '''extensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#extensions NetworkServicesLbRouteExtension#extensions}
        '''
        result = self._values.get("extensions")
        assert result is not None, "Required property 'extensions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesLbRouteExtensionExtensionChainsExtensions"]], result)

    @builtins.property
    def match_condition(
        self,
    ) -> "NetworkServicesLbRouteExtensionExtensionChainsMatchCondition":
        '''match_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#match_condition NetworkServicesLbRouteExtension#match_condition}
        '''
        result = self._values.get("match_condition")
        assert result is not None, "Required property 'match_condition' is missing"
        return typing.cast("NetworkServicesLbRouteExtensionExtensionChainsMatchCondition", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for this extension chain.

        The name is logged as part of the HTTP request logs.
        The name must conform with RFC-1034, is restricted to lower-cased letters, numbers and hyphens,
        and can have a maximum length of 63 characters. Additionally, the first character must be a letter
        and the last character must be a letter or a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#name NetworkServicesLbRouteExtension#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesLbRouteExtensionExtensionChains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesLbRouteExtension.NetworkServicesLbRouteExtensionExtensionChainsExtensions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "service": "service",
        "authority": "authority",
        "fail_open": "failOpen",
        "forward_headers": "forwardHeaders",
        "timeout": "timeout",
    },
)
class NetworkServicesLbRouteExtensionExtensionChainsExtensions:
    def __init__(
        self,
        *,
        name: builtins.str,
        service: builtins.str,
        authority: typing.Optional[builtins.str] = None,
        fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name for this extension. The name is logged as part of the HTTP request logs. The name must conform with RFC-1034, is restricted to lower-cased letters, numbers and hyphens, and can have a maximum length of 63 characters. Additionally, the first character must be a letter and the last a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#name NetworkServicesLbRouteExtension#name}
        :param service: The reference to the service that runs the extension. Must be a reference to a backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#service NetworkServicesLbRouteExtension#service}
        :param authority: The :authority header in the gRPC request sent from Envoy to the extension service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#authority NetworkServicesLbRouteExtension#authority}
        :param fail_open: Determines how the proxy behaves if the call to the extension fails or times out. When set to TRUE, request or response processing continues without error. Any subsequent extensions in the extension chain are also executed. When set to FALSE: * If response headers have not been delivered to the downstream client, a generic 500 error is returned to the client. The error response can be tailored by configuring a custom error response in the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#fail_open NetworkServicesLbRouteExtension#fail_open}
        :param forward_headers: List of the HTTP headers to forward to the extension (from the client or backend). If omitted, all headers are sent. Each element is a string indicating the header name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#forward_headers NetworkServicesLbRouteExtension#forward_headers}
        :param timeout: Specifies the timeout for each individual message on the stream. The timeout must be between 10-1000 milliseconds. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#timeout NetworkServicesLbRouteExtension#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6248e245b0101a8282b711615c73555e00dad4e52465856080612c3af667b3e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument authority", value=authority, expected_type=type_hints["authority"])
            check_type(argname="argument fail_open", value=fail_open, expected_type=type_hints["fail_open"])
            check_type(argname="argument forward_headers", value=forward_headers, expected_type=type_hints["forward_headers"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "service": service,
        }
        if authority is not None:
            self._values["authority"] = authority
        if fail_open is not None:
            self._values["fail_open"] = fail_open
        if forward_headers is not None:
            self._values["forward_headers"] = forward_headers
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for this extension.

        The name is logged as part of the HTTP request logs.
        The name must conform with RFC-1034, is restricted to lower-cased letters, numbers and hyphens,
        and can have a maximum length of 63 characters. Additionally, the first character must be a letter
        and the last a letter or a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#name NetworkServicesLbRouteExtension#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''The reference to the service that runs the extension. Must be a reference to a backend service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#service NetworkServicesLbRouteExtension#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authority(self) -> typing.Optional[builtins.str]:
        '''The :authority header in the gRPC request sent from Envoy to the extension service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#authority NetworkServicesLbRouteExtension#authority}
        '''
        result = self._values.get("authority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_open(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines how the proxy behaves if the call to the extension fails or times out.

        When set to TRUE, request or response processing continues without error.
        Any subsequent extensions in the extension chain are also executed.
        When set to FALSE: * If response headers have not been delivered to the downstream client,
        a generic 500 error is returned to the client. The error response can be tailored by
        configuring a custom error response in the load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#fail_open NetworkServicesLbRouteExtension#fail_open}
        '''
        result = self._values.get("fail_open")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forward_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of the HTTP headers to forward to the extension (from the client or backend).

        If omitted, all headers are sent. Each element is a string indicating the header name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#forward_headers NetworkServicesLbRouteExtension#forward_headers}
        '''
        result = self._values.get("forward_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Specifies the timeout for each individual message on the stream.

        The timeout must be between 10-1000 milliseconds.
        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#timeout NetworkServicesLbRouteExtension#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesLbRouteExtensionExtensionChainsExtensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesLbRouteExtensionExtensionChainsExtensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbRouteExtension.NetworkServicesLbRouteExtensionExtensionChainsExtensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bda665b9b74cfefc2e599eb9dc256c1dd537ceade7c3a4fc3424343d6e46dfad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesLbRouteExtensionExtensionChainsExtensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8d4b14ec639529f7245238aacbb8dd123d95fdb0243ce29f20ef1be9ec6c6c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesLbRouteExtensionExtensionChainsExtensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82e03020084c86b805fd5b889fdb5a75e071c6fb3d3498d733c329a4b75b27f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__131851728e98de6003b29d717ca12502545ffff33e05c6028b90c026ed908f7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cfa337c3ad5a24406213eb2459372ed83b2667e9c74bcb311931ff8a0893016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbRouteExtensionExtensionChainsExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbRouteExtensionExtensionChainsExtensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbRouteExtensionExtensionChainsExtensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da7c2aa1cfeecb95a151aef799a786ea8695a2a5737fdce96df7494d1ed22901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesLbRouteExtensionExtensionChainsExtensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbRouteExtension.NetworkServicesLbRouteExtensionExtensionChainsExtensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ae9e7a5169a28ec09bf6f7ac00dedda13b2eb7c59c540c42729da38930901dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAuthority")
    def reset_authority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthority", []))

    @jsii.member(jsii_name="resetFailOpen")
    def reset_fail_open(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOpen", []))

    @jsii.member(jsii_name="resetForwardHeaders")
    def reset_forward_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardHeaders", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="authorityInput")
    def authority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorityInput"))

    @builtins.property
    @jsii.member(jsii_name="failOpenInput")
    def fail_open_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOpenInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardHeadersInput")
    def forward_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "forwardHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="authority")
    def authority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authority"))

    @authority.setter
    def authority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1edbd503d2afffab7bfc5c668ab7c7abff9bf51c5d30b36ef145b046d647e104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOpen")
    def fail_open(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOpen"))

    @fail_open.setter
    def fail_open(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55737280fd310fc2aafea986eff01336b8c75cd192ea0932b160561d99915e67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOpen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardHeaders")
    def forward_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "forwardHeaders"))

    @forward_headers.setter
    def forward_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d2262658303971b5b1199987099aa447059694e98704edb70e39e5ce90865cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb688b452ff6bd13561fe6ad1b3b4059ce2fb698584898ef8f5637496b31b12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e91bf83122fa0206646698e7b0a4cd2b1d7b61f0537328cb0eb748ddbae282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e4a8102fb39095c472bf1d4c55f0423ff53e23f931b47265fa3dfdee3766fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbRouteExtensionExtensionChainsExtensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbRouteExtensionExtensionChainsExtensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbRouteExtensionExtensionChainsExtensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75db423032e9b82b904b729739abd795f2fd71d504075d054f01704f156d42ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesLbRouteExtensionExtensionChainsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbRouteExtension.NetworkServicesLbRouteExtensionExtensionChainsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b3e0fc77aea854040a1052290f451a7defeb341c79118d990f1c17dde983ef0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesLbRouteExtensionExtensionChainsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498ce05d5e54b949f248c0942fbaa0eabdfbbf2a7d470f2246220886bdcc921d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesLbRouteExtensionExtensionChainsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd4275013cdd8e0d16f8c03b2c2855f375cbf88adf52b9b5b2b4d081b584e9a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69734e1dec9b7d15c6bf58662bf75e59dd9877137f7f44da6fe6ac45654f36b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__073a749575f3e0a690eef9acacd82ee3af96aec6a911c95adc7c1de326ee4606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbRouteExtensionExtensionChains]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbRouteExtensionExtensionChains]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbRouteExtensionExtensionChains]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32934c8f7ce5b3f6e4a787a9c71dae7e21bc035c13c3f981822aed7567296afe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesLbRouteExtension.NetworkServicesLbRouteExtensionExtensionChainsMatchCondition",
    jsii_struct_bases=[],
    name_mapping={"cel_expression": "celExpression"},
)
class NetworkServicesLbRouteExtensionExtensionChainsMatchCondition:
    def __init__(self, *, cel_expression: builtins.str) -> None:
        '''
        :param cel_expression: A Common Expression Language (CEL) expression that is used to match requests for which the extension chain is executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#cel_expression NetworkServicesLbRouteExtension#cel_expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3e3ef6db81a5247632d725a82777dad00e55c79212571a3d293449d7421790)
            check_type(argname="argument cel_expression", value=cel_expression, expected_type=type_hints["cel_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cel_expression": cel_expression,
        }

    @builtins.property
    def cel_expression(self) -> builtins.str:
        '''A Common Expression Language (CEL) expression that is used to match requests for which the extension chain is executed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#cel_expression NetworkServicesLbRouteExtension#cel_expression}
        '''
        result = self._values.get("cel_expression")
        assert result is not None, "Required property 'cel_expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesLbRouteExtensionExtensionChainsMatchCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesLbRouteExtensionExtensionChainsMatchConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbRouteExtension.NetworkServicesLbRouteExtensionExtensionChainsMatchConditionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__753fb0da266ce6bc84fdaa42370055387ba0cd5d75bd413bf8d36ca26126da33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="celExpressionInput")
    def cel_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "celExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="celExpression")
    def cel_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "celExpression"))

    @cel_expression.setter
    def cel_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a24278ac3b6f3575e44c51b8dd871c2290ee28d610a75e8214a1288a9077d1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "celExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesLbRouteExtensionExtensionChainsMatchCondition]:
        return typing.cast(typing.Optional[NetworkServicesLbRouteExtensionExtensionChainsMatchCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesLbRouteExtensionExtensionChainsMatchCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87ce95b6dcd8bef8a9ac863d18b53dadbe14f603131889d4e480af558bc8c4e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesLbRouteExtensionExtensionChainsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbRouteExtension.NetworkServicesLbRouteExtensionExtensionChainsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8658219f62bc7a091bce10d9d0f39fef38f722e9c7a71026b0d1f9f9a3068578)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExtensions")
    def put_extensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesLbRouteExtensionExtensionChainsExtensions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9ee38121bac35f28aa4144d71a430fc5d19871b58a289f60f2b8f63f572d2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtensions", [value]))

    @jsii.member(jsii_name="putMatchCondition")
    def put_match_condition(self, *, cel_expression: builtins.str) -> None:
        '''
        :param cel_expression: A Common Expression Language (CEL) expression that is used to match requests for which the extension chain is executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#cel_expression NetworkServicesLbRouteExtension#cel_expression}
        '''
        value = NetworkServicesLbRouteExtensionExtensionChainsMatchCondition(
            cel_expression=cel_expression
        )

        return typing.cast(None, jsii.invoke(self, "putMatchCondition", [value]))

    @builtins.property
    @jsii.member(jsii_name="extensions")
    def extensions(
        self,
    ) -> NetworkServicesLbRouteExtensionExtensionChainsExtensionsList:
        return typing.cast(NetworkServicesLbRouteExtensionExtensionChainsExtensionsList, jsii.get(self, "extensions"))

    @builtins.property
    @jsii.member(jsii_name="matchCondition")
    def match_condition(
        self,
    ) -> NetworkServicesLbRouteExtensionExtensionChainsMatchConditionOutputReference:
        return typing.cast(NetworkServicesLbRouteExtensionExtensionChainsMatchConditionOutputReference, jsii.get(self, "matchCondition"))

    @builtins.property
    @jsii.member(jsii_name="extensionsInput")
    def extensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbRouteExtensionExtensionChainsExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbRouteExtensionExtensionChainsExtensions]]], jsii.get(self, "extensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchConditionInput")
    def match_condition_input(
        self,
    ) -> typing.Optional[NetworkServicesLbRouteExtensionExtensionChainsMatchCondition]:
        return typing.cast(typing.Optional[NetworkServicesLbRouteExtensionExtensionChainsMatchCondition], jsii.get(self, "matchConditionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f445bf4105bd99add222603703625e11b440fa3b77cd4d0d00db949b728129e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbRouteExtensionExtensionChains]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbRouteExtensionExtensionChains]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbRouteExtensionExtensionChains]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e57ea079928ae1594bffe95ad60f14c3bb39e0cf5d3259efa50ba9fcb21ead02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesLbRouteExtension.NetworkServicesLbRouteExtensionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkServicesLbRouteExtensionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#create NetworkServicesLbRouteExtension#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#delete NetworkServicesLbRouteExtension#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#update NetworkServicesLbRouteExtension#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5daa806347645f6e8a22baa4eec278bed7144e656b43617c5ad1397b0c061d09)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#create NetworkServicesLbRouteExtension#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#delete NetworkServicesLbRouteExtension#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_route_extension#update NetworkServicesLbRouteExtension#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesLbRouteExtensionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesLbRouteExtensionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbRouteExtension.NetworkServicesLbRouteExtensionTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29dde2d5ae7af4b40bb00a77a67e1bda5d3a455f4112302ace09a4e63522a0ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7662feb86b6081e80d23470e7e626b776f34dba9f5cd10f109b4609f5c6d8bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f37ed0cdb828578f4895c66e308b4696ccc6c128d4b02d4680f381022e86a70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c4eb9aca7cae08429b3b8428ba12a01a08e6184c4df8fd69bb7ff06a3ab04c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbRouteExtensionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbRouteExtensionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbRouteExtensionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e189475a93a986832529fc144b0d9bfa0be30a06f67dc09e880658246b266c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkServicesLbRouteExtension",
    "NetworkServicesLbRouteExtensionConfig",
    "NetworkServicesLbRouteExtensionExtensionChains",
    "NetworkServicesLbRouteExtensionExtensionChainsExtensions",
    "NetworkServicesLbRouteExtensionExtensionChainsExtensionsList",
    "NetworkServicesLbRouteExtensionExtensionChainsExtensionsOutputReference",
    "NetworkServicesLbRouteExtensionExtensionChainsList",
    "NetworkServicesLbRouteExtensionExtensionChainsMatchCondition",
    "NetworkServicesLbRouteExtensionExtensionChainsMatchConditionOutputReference",
    "NetworkServicesLbRouteExtensionExtensionChainsOutputReference",
    "NetworkServicesLbRouteExtensionTimeouts",
    "NetworkServicesLbRouteExtensionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d96e7dc6db33f67c5ff3dd949adba606cc53ef713670c0b65bb07e2d3bea38ca(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    extension_chains: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesLbRouteExtensionExtensionChains, typing.Dict[builtins.str, typing.Any]]]],
    forwarding_rules: typing.Sequence[builtins.str],
    load_balancing_scheme: builtins.str,
    location: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesLbRouteExtensionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2996ad5413810527e2afd9276d7eb2cec28a1c139d8cef7ecf041d229d5e0db6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b66b16bc56f5e780e319701e96e815b49adf1f6998b157af42c6f0d55e214e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesLbRouteExtensionExtensionChains, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a0ec95a91d554dead6637435fb5147666d13999523d78b4142a59a831d3408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33e459ae7013ee6e8d25c04841560c7ddc35318327bcdd6d25e8d91e7b580be(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f701bf30bbe09bf3d554292f90dbd16f3c381c0b6ed87a77d78dcdc45828d1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78ec63f4962bd4c224328775b93d8fab4d69245d0c3afab93cd713218742b87(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20ed61c56ee1f19c28eca35631212bae33555e4fcffb4f128dd156d41478265(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec82c8a03283a4ef9b61b2dcdb3d9a1a9f20beb65b4cd863fe330826881bd77c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eda6da4b0a3f821d2b5ab1e548f2a0b63e70060f292cfd9ee185d3ec86eec8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba71bf37472d80d5b63aaa6bf79884e3a44f9d5245525ebd34c49e99a30f6d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e052feb5a7538305beb5e39440ab18362b1ed43de5a61cb450f1249de476837(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    extension_chains: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesLbRouteExtensionExtensionChains, typing.Dict[builtins.str, typing.Any]]]],
    forwarding_rules: typing.Sequence[builtins.str],
    load_balancing_scheme: builtins.str,
    location: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesLbRouteExtensionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff06c678ed2ac5096c426e478ec66d799b096325bb854d15d17eb16d1e01237(
    *,
    extensions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesLbRouteExtensionExtensionChainsExtensions, typing.Dict[builtins.str, typing.Any]]]],
    match_condition: typing.Union[NetworkServicesLbRouteExtensionExtensionChainsMatchCondition, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6248e245b0101a8282b711615c73555e00dad4e52465856080612c3af667b3e(
    *,
    name: builtins.str,
    service: builtins.str,
    authority: typing.Optional[builtins.str] = None,
    fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forward_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda665b9b74cfefc2e599eb9dc256c1dd537ceade7c3a4fc3424343d6e46dfad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8d4b14ec639529f7245238aacbb8dd123d95fdb0243ce29f20ef1be9ec6c6c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82e03020084c86b805fd5b889fdb5a75e071c6fb3d3498d733c329a4b75b27f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131851728e98de6003b29d717ca12502545ffff33e05c6028b90c026ed908f7a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cfa337c3ad5a24406213eb2459372ed83b2667e9c74bcb311931ff8a0893016(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7c2aa1cfeecb95a151aef799a786ea8695a2a5737fdce96df7494d1ed22901(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbRouteExtensionExtensionChainsExtensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae9e7a5169a28ec09bf6f7ac00dedda13b2eb7c59c540c42729da38930901dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edbd503d2afffab7bfc5c668ab7c7abff9bf51c5d30b36ef145b046d647e104(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55737280fd310fc2aafea986eff01336b8c75cd192ea0932b160561d99915e67(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2262658303971b5b1199987099aa447059694e98704edb70e39e5ce90865cf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb688b452ff6bd13561fe6ad1b3b4059ce2fb698584898ef8f5637496b31b12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e91bf83122fa0206646698e7b0a4cd2b1d7b61f0537328cb0eb748ddbae282(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e4a8102fb39095c472bf1d4c55f0423ff53e23f931b47265fa3dfdee3766fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75db423032e9b82b904b729739abd795f2fd71d504075d054f01704f156d42ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbRouteExtensionExtensionChainsExtensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3e0fc77aea854040a1052290f451a7defeb341c79118d990f1c17dde983ef0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498ce05d5e54b949f248c0942fbaa0eabdfbbf2a7d470f2246220886bdcc921d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4275013cdd8e0d16f8c03b2c2855f375cbf88adf52b9b5b2b4d081b584e9a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69734e1dec9b7d15c6bf58662bf75e59dd9877137f7f44da6fe6ac45654f36b3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073a749575f3e0a690eef9acacd82ee3af96aec6a911c95adc7c1de326ee4606(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32934c8f7ce5b3f6e4a787a9c71dae7e21bc035c13c3f981822aed7567296afe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbRouteExtensionExtensionChains]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3e3ef6db81a5247632d725a82777dad00e55c79212571a3d293449d7421790(
    *,
    cel_expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753fb0da266ce6bc84fdaa42370055387ba0cd5d75bd413bf8d36ca26126da33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a24278ac3b6f3575e44c51b8dd871c2290ee28d610a75e8214a1288a9077d1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ce95b6dcd8bef8a9ac863d18b53dadbe14f603131889d4e480af558bc8c4e4(
    value: typing.Optional[NetworkServicesLbRouteExtensionExtensionChainsMatchCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8658219f62bc7a091bce10d9d0f39fef38f722e9c7a71026b0d1f9f9a3068578(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9ee38121bac35f28aa4144d71a430fc5d19871b58a289f60f2b8f63f572d2f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesLbRouteExtensionExtensionChainsExtensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f445bf4105bd99add222603703625e11b440fa3b77cd4d0d00db949b728129e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57ea079928ae1594bffe95ad60f14c3bb39e0cf5d3259efa50ba9fcb21ead02(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbRouteExtensionExtensionChains]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5daa806347645f6e8a22baa4eec278bed7144e656b43617c5ad1397b0c061d09(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29dde2d5ae7af4b40bb00a77a67e1bda5d3a455f4112302ace09a4e63522a0ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7662feb86b6081e80d23470e7e626b776f34dba9f5cd10f109b4609f5c6d8bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f37ed0cdb828578f4895c66e308b4696ccc6c128d4b02d4680f381022e86a70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4eb9aca7cae08429b3b8428ba12a01a08e6184c4df8fd69bb7ff06a3ab04c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e189475a93a986832529fc144b0d9bfa0be30a06f67dc09e880658246b266c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbRouteExtensionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
