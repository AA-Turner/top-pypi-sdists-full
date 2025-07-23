r'''
# `google_network_services_lb_traffic_extension`

Refer to the Terraform Registry for docs: [`google_network_services_lb_traffic_extension`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension).
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


class NetworkServicesLbTrafficExtension(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbTrafficExtension.NetworkServicesLbTrafficExtension",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension google_network_services_lb_traffic_extension}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        extension_chains: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesLbTrafficExtensionExtensionChains", typing.Dict[builtins.str, typing.Any]]]],
        forwarding_rules: typing.Sequence[builtins.str],
        location: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesLbTrafficExtensionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension google_network_services_lb_traffic_extension} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param extension_chains: extension_chains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#extension_chains NetworkServicesLbTrafficExtension#extension_chains}
        :param forwarding_rules: A list of references to the forwarding rules to which this service extension is attached to. At least one forwarding rule is required. There can be only one LBTrafficExtension resource per forwarding rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#forwarding_rules NetworkServicesLbTrafficExtension#forwarding_rules}
        :param location: The location of the traffic extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#location NetworkServicesLbTrafficExtension#location}
        :param name: Name of the LbTrafficExtension resource in the following format: projects/{project}/locations/{location}/lbTrafficExtensions/{lbTrafficExtension}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#name NetworkServicesLbTrafficExtension#name}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#description NetworkServicesLbTrafficExtension#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#id NetworkServicesLbTrafficExtension#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the LbTrafficExtension resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#labels NetworkServicesLbTrafficExtension#labels}
        :param load_balancing_scheme: All backend services and forwarding rules referenced by this extension must share the same load balancing scheme. For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_ and `Supported application load balancers <https://cloud.google.com/service-extensions/docs/callouts-overview#supported-lbs>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#load_balancing_scheme NetworkServicesLbTrafficExtension#load_balancing_scheme}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#project NetworkServicesLbTrafficExtension#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#timeouts NetworkServicesLbTrafficExtension#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd4d233ff08ea64ba403631d0ee20f7505e5cf95ca1a37f5483c5abbe3788a1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkServicesLbTrafficExtensionConfig(
            extension_chains=extension_chains,
            forwarding_rules=forwarding_rules,
            location=location,
            name=name,
            description=description,
            id=id,
            labels=labels,
            load_balancing_scheme=load_balancing_scheme,
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
        '''Generates CDKTF code for importing a NetworkServicesLbTrafficExtension resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkServicesLbTrafficExtension to import.
        :param import_from_id: The id of the existing NetworkServicesLbTrafficExtension that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkServicesLbTrafficExtension to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f9cc86dc5d91b6b0df70626aff73515fcad88858b993f65e3d560c39947f5e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExtensionChains")
    def put_extension_chains(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesLbTrafficExtensionExtensionChains", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c781256f1ee90de875f19125a49e89b5e180c770d03cf26d3959f83ea0835f)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#create NetworkServicesLbTrafficExtension#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#delete NetworkServicesLbTrafficExtension#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#update NetworkServicesLbTrafficExtension#update}.
        '''
        value = NetworkServicesLbTrafficExtensionTimeouts(
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

    @jsii.member(jsii_name="resetLoadBalancingScheme")
    def reset_load_balancing_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancingScheme", []))

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
    def extension_chains(
        self,
    ) -> "NetworkServicesLbTrafficExtensionExtensionChainsList":
        return typing.cast("NetworkServicesLbTrafficExtensionExtensionChainsList", jsii.get(self, "extensionChains"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkServicesLbTrafficExtensionTimeoutsOutputReference":
        return typing.cast("NetworkServicesLbTrafficExtensionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionChainsInput")
    def extension_chains_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesLbTrafficExtensionExtensionChains"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesLbTrafficExtensionExtensionChains"]]], jsii.get(self, "extensionChainsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesLbTrafficExtensionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesLbTrafficExtensionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f36c0e901af456a4f7eb814f9cb7d160fe63f8482ff28160418201866e9a8d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardingRules")
    def forwarding_rules(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "forwardingRules"))

    @forwarding_rules.setter
    def forwarding_rules(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826dafcecb965ab34a6977616f47645d53192fb9f31a8315790c735e63a68666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardingRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae9bf8ce21223de686b762bc34bf58001eb16e5f54344ad7753e8b12aa63c67a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a7f10c77aff4c0830416495be84a26b90f2355cf78ed666dececc1d7241d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27f7b9d43afb4d2b0e32d71efb4e15f3d921317f4473877bc7bd4a9fd51f518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d619c90dc8198e06a1905ab48680151a0411c4bb2689a365207aa53e10ef8059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4988e451a4143b72003cae494c039c147382a627dad7463e0336d25eea944d71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3195c06fb3d6935eafb18dc352478d7f352ed5a17b060ee3f8f65c14f01d3539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesLbTrafficExtension.NetworkServicesLbTrafficExtensionConfig",
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
        "location": "location",
        "name": "name",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "load_balancing_scheme": "loadBalancingScheme",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class NetworkServicesLbTrafficExtensionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        extension_chains: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesLbTrafficExtensionExtensionChains", typing.Dict[builtins.str, typing.Any]]]],
        forwarding_rules: typing.Sequence[builtins.str],
        location: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesLbTrafficExtensionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param extension_chains: extension_chains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#extension_chains NetworkServicesLbTrafficExtension#extension_chains}
        :param forwarding_rules: A list of references to the forwarding rules to which this service extension is attached to. At least one forwarding rule is required. There can be only one LBTrafficExtension resource per forwarding rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#forwarding_rules NetworkServicesLbTrafficExtension#forwarding_rules}
        :param location: The location of the traffic extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#location NetworkServicesLbTrafficExtension#location}
        :param name: Name of the LbTrafficExtension resource in the following format: projects/{project}/locations/{location}/lbTrafficExtensions/{lbTrafficExtension}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#name NetworkServicesLbTrafficExtension#name}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#description NetworkServicesLbTrafficExtension#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#id NetworkServicesLbTrafficExtension#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the LbTrafficExtension resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#labels NetworkServicesLbTrafficExtension#labels}
        :param load_balancing_scheme: All backend services and forwarding rules referenced by this extension must share the same load balancing scheme. For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_ and `Supported application load balancers <https://cloud.google.com/service-extensions/docs/callouts-overview#supported-lbs>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#load_balancing_scheme NetworkServicesLbTrafficExtension#load_balancing_scheme}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#project NetworkServicesLbTrafficExtension#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#timeouts NetworkServicesLbTrafficExtension#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = NetworkServicesLbTrafficExtensionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4438ebebddac59e064eeee87d75ff8631e7d09a7396d5010e1fb7d00a18004)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument extension_chains", value=extension_chains, expected_type=type_hints["extension_chains"])
            check_type(argname="argument forwarding_rules", value=forwarding_rules, expected_type=type_hints["forwarding_rules"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument load_balancing_scheme", value=load_balancing_scheme, expected_type=type_hints["load_balancing_scheme"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "extension_chains": extension_chains,
            "forwarding_rules": forwarding_rules,
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
        if load_balancing_scheme is not None:
            self._values["load_balancing_scheme"] = load_balancing_scheme
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesLbTrafficExtensionExtensionChains"]]:
        '''extension_chains block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#extension_chains NetworkServicesLbTrafficExtension#extension_chains}
        '''
        result = self._values.get("extension_chains")
        assert result is not None, "Required property 'extension_chains' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesLbTrafficExtensionExtensionChains"]], result)

    @builtins.property
    def forwarding_rules(self) -> typing.List[builtins.str]:
        '''A list of references to the forwarding rules to which this service extension is attached to.

        At least one forwarding rule is required. There can be only one LBTrafficExtension resource per forwarding rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#forwarding_rules NetworkServicesLbTrafficExtension#forwarding_rules}
        '''
        result = self._values.get("forwarding_rules")
        assert result is not None, "Required property 'forwarding_rules' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the traffic extension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#location NetworkServicesLbTrafficExtension#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the LbTrafficExtension resource in the following format: projects/{project}/locations/{location}/lbTrafficExtensions/{lbTrafficExtension}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#name NetworkServicesLbTrafficExtension#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#description NetworkServicesLbTrafficExtension#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#id NetworkServicesLbTrafficExtension#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of labels associated with the LbTrafficExtension resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#labels NetworkServicesLbTrafficExtension#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def load_balancing_scheme(self) -> typing.Optional[builtins.str]:
        '''All backend services and forwarding rules referenced by this extension must share the same load balancing scheme.

        For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_ and
        `Supported application load balancers <https://cloud.google.com/service-extensions/docs/callouts-overview#supported-lbs>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#load_balancing_scheme NetworkServicesLbTrafficExtension#load_balancing_scheme}
        '''
        result = self._values.get("load_balancing_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#project NetworkServicesLbTrafficExtension#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkServicesLbTrafficExtensionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#timeouts NetworkServicesLbTrafficExtension#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkServicesLbTrafficExtensionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesLbTrafficExtensionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesLbTrafficExtension.NetworkServicesLbTrafficExtensionExtensionChains",
    jsii_struct_bases=[],
    name_mapping={
        "extensions": "extensions",
        "match_condition": "matchCondition",
        "name": "name",
    },
)
class NetworkServicesLbTrafficExtensionExtensionChains:
    def __init__(
        self,
        *,
        extensions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesLbTrafficExtensionExtensionChainsExtensions", typing.Dict[builtins.str, typing.Any]]]],
        match_condition: typing.Union["NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param extensions: extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#extensions NetworkServicesLbTrafficExtension#extensions}
        :param match_condition: match_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#match_condition NetworkServicesLbTrafficExtension#match_condition}
        :param name: The name for this extension chain. The name is logged as part of the HTTP request logs. The name must conform with RFC-1034, is restricted to lower-cased letters, numbers and hyphens, and can have a maximum length of 63 characters. Additionally, the first character must be a letter and the last a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#name NetworkServicesLbTrafficExtension#name}
        '''
        if isinstance(match_condition, dict):
            match_condition = NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition(**match_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ac4c01a0db85ea03d504a4bd904deaba3112dcd905b6283f1535ccb02db89e)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesLbTrafficExtensionExtensionChainsExtensions"]]:
        '''extensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#extensions NetworkServicesLbTrafficExtension#extensions}
        '''
        result = self._values.get("extensions")
        assert result is not None, "Required property 'extensions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesLbTrafficExtensionExtensionChainsExtensions"]], result)

    @builtins.property
    def match_condition(
        self,
    ) -> "NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition":
        '''match_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#match_condition NetworkServicesLbTrafficExtension#match_condition}
        '''
        result = self._values.get("match_condition")
        assert result is not None, "Required property 'match_condition' is missing"
        return typing.cast("NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for this extension chain.

        The name is logged as part of the HTTP request logs.
        The name must conform with RFC-1034, is restricted to lower-cased letters, numbers and hyphens,
        and can have a maximum length of 63 characters. Additionally, the first character must be a letter
        and the last a letter or a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#name NetworkServicesLbTrafficExtension#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesLbTrafficExtensionExtensionChains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesLbTrafficExtension.NetworkServicesLbTrafficExtensionExtensionChainsExtensions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "service": "service",
        "authority": "authority",
        "fail_open": "failOpen",
        "forward_headers": "forwardHeaders",
        "metadata": "metadata",
        "supported_events": "supportedEvents",
        "timeout": "timeout",
    },
)
class NetworkServicesLbTrafficExtensionExtensionChainsExtensions:
    def __init__(
        self,
        *,
        name: builtins.str,
        service: builtins.str,
        authority: typing.Optional[builtins.str] = None,
        fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        supported_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name for this extension. The name is logged as part of the HTTP request logs. The name must conform with RFC-1034, is restricted to lower-cased letters, numbers and hyphens, and can have a maximum length of 63 characters. Additionally, the first character must be a letter and the last a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#name NetworkServicesLbTrafficExtension#name}
        :param service: The reference to the service that runs the extension. Must be a reference to a backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#service NetworkServicesLbTrafficExtension#service}
        :param authority: The :authority header in the gRPC request sent from Envoy to the extension service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#authority NetworkServicesLbTrafficExtension#authority}
        :param fail_open: Determines how the proxy behaves if the call to the extension fails or times out. When set to TRUE, request or response processing continues without error. Any subsequent extensions in the extension chain are also executed. When set to FALSE: * If response headers have not been delivered to the downstream client, a generic 500 error is returned to the client. The error response can be tailored by configuring a custom error response in the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#fail_open NetworkServicesLbTrafficExtension#fail_open}
        :param forward_headers: List of the HTTP headers to forward to the extension (from the client or backend). If omitted, all headers are sent. Each element is a string indicating the header name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#forward_headers NetworkServicesLbTrafficExtension#forward_headers}
        :param metadata: Metadata associated with the extension. This field is used to pass metadata to the extension service. You can set up key value pairs for metadata as you like and need. f.e. {"key": "value", "key2": "value2"}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#metadata NetworkServicesLbTrafficExtension#metadata}
        :param supported_events: A set of events during request or response processing for which this extension is called. This field is required for the LbTrafficExtension resource. It's not relevant for the LbRouteExtension resource. Possible values:'EVENT_TYPE_UNSPECIFIED', 'REQUEST_HEADERS', 'REQUEST_BODY', 'RESPONSE_HEADERS', 'RESPONSE_BODY', 'RESPONSE_BODY' and 'RESPONSE_BODY'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#supported_events NetworkServicesLbTrafficExtension#supported_events}
        :param timeout: Specifies the timeout for each individual message on the stream. The timeout must be between 10-1000 milliseconds. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#timeout NetworkServicesLbTrafficExtension#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c78c3bcc98112bd915290d0234dd89380fad107712d149e628df89783e25098)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument authority", value=authority, expected_type=type_hints["authority"])
            check_type(argname="argument fail_open", value=fail_open, expected_type=type_hints["fail_open"])
            check_type(argname="argument forward_headers", value=forward_headers, expected_type=type_hints["forward_headers"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument supported_events", value=supported_events, expected_type=type_hints["supported_events"])
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
        if metadata is not None:
            self._values["metadata"] = metadata
        if supported_events is not None:
            self._values["supported_events"] = supported_events
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for this extension.

        The name is logged as part of the HTTP request logs.
        The name must conform with RFC-1034, is restricted to lower-cased letters, numbers and hyphens,
        and can have a maximum length of 63 characters. Additionally, the first character must be a letter
        and the last a letter or a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#name NetworkServicesLbTrafficExtension#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''The reference to the service that runs the extension. Must be a reference to a backend service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#service NetworkServicesLbTrafficExtension#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authority(self) -> typing.Optional[builtins.str]:
        '''The :authority header in the gRPC request sent from Envoy to the extension service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#authority NetworkServicesLbTrafficExtension#authority}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#fail_open NetworkServicesLbTrafficExtension#fail_open}
        '''
        result = self._values.get("fail_open")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forward_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of the HTTP headers to forward to the extension (from the client or backend).

        If omitted, all headers are sent. Each element is a string indicating the header name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#forward_headers NetworkServicesLbTrafficExtension#forward_headers}
        '''
        result = self._values.get("forward_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata associated with the extension.

        This field is used to pass metadata to the extension service.
        You can set up key value pairs for metadata as you like and need.
        f.e. {"key": "value", "key2": "value2"}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#metadata NetworkServicesLbTrafficExtension#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def supported_events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of events during request or response processing for which this extension is called.

        This field is required for the LbTrafficExtension resource. It's not relevant for the LbRouteExtension
        resource. Possible values:'EVENT_TYPE_UNSPECIFIED', 'REQUEST_HEADERS', 'REQUEST_BODY', 'RESPONSE_HEADERS',
        'RESPONSE_BODY', 'RESPONSE_BODY' and 'RESPONSE_BODY'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#supported_events NetworkServicesLbTrafficExtension#supported_events}
        '''
        result = self._values.get("supported_events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Specifies the timeout for each individual message on the stream.

        The timeout must be between 10-1000 milliseconds.
        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#timeout NetworkServicesLbTrafficExtension#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesLbTrafficExtensionExtensionChainsExtensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesLbTrafficExtensionExtensionChainsExtensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbTrafficExtension.NetworkServicesLbTrafficExtensionExtensionChainsExtensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e57aeec91d70befd0c2e23f770366879db4761a276527c50f513846477ddefb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesLbTrafficExtensionExtensionChainsExtensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9903b44a3fb204ba98b107d05ef64896fd2e6ab37073584731f49d060b934402)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesLbTrafficExtensionExtensionChainsExtensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__830fe84ca958c9e26689c46e6c86050b5a31c3ac7639ad1da6dd62d2faf09992)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2e0b97a1c3e917276b8024e1d157a3342c2946c94aeea8c005ed529003462aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7fdfcc0d774b721c46779b4735963d7b8821efc6a368ffb7c6c2f0ae64d1379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbTrafficExtensionExtensionChainsExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbTrafficExtensionExtensionChainsExtensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbTrafficExtensionExtensionChainsExtensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c928285159782cff4468308591033c7ebe27e3d31b1461e7d599ae4d3f25d8cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesLbTrafficExtensionExtensionChainsExtensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbTrafficExtension.NetworkServicesLbTrafficExtensionExtensionChainsExtensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab36519c347416ffa28fd141c576792fc44ee7cc69374b5b389807a500aeead6)
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

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetSupportedEvents")
    def reset_supported_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportedEvents", []))

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
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="supportedEventsInput")
    def supported_events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "supportedEventsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4e0affaa2db6cadbe175b9b72dfea7cc80de7c0d2fda2941ef108292a5fc93ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00fbf81ad3a6fe038ae5030d7b4a251e393b2db5ea3d7d9ca1af64bd492c2c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOpen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardHeaders")
    def forward_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "forwardHeaders"))

    @forward_headers.setter
    def forward_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6a458bfbe023ce59ce46fb9857b0d076377f10079da2a5c6013fff3617ee78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755575a1877ee026a0ac37373d77a12acb156a90818de8fde3c0b914a2ba7196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80666537be11b5a0714b8529c4b3da315e38e11fd502db3f1292bd792fa171a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82bc6c1efd864f3e89a422267dbeefd02030914539fa0b590eaecc7be7e1b7f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportedEvents")
    def supported_events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedEvents"))

    @supported_events.setter
    def supported_events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1acb0a2a75916a20f608d827b6ebb17c8f3e50716d16e4f36ec520b3cfe334ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportedEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09cbad874ed36650eb540833f7d1799686f2e30262432703dc910dfa2022da1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbTrafficExtensionExtensionChainsExtensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbTrafficExtensionExtensionChainsExtensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbTrafficExtensionExtensionChainsExtensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__569d096f93cb902c9ff10f01b22e360bd850c345d3b46f4140cfc50c60974825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesLbTrafficExtensionExtensionChainsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbTrafficExtension.NetworkServicesLbTrafficExtensionExtensionChainsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12a6ee5ec49a6a2d04e6b520dac79a1f546cbd9b55d19ba6d17e664df1dc22ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesLbTrafficExtensionExtensionChainsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88633611fc7f1f7773892499a85bcd36f94b2719cfadeb77cd32d3254e059722)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesLbTrafficExtensionExtensionChainsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa40bcfa9f46be7bcee2119d0d3d213b1aa4726b7d43a5082f90c935bce25db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__906114c81ed18319c6e6766e3e98e71f6a7efa2b651a9d5cc873d5e05b35ec11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0162fcf2f3218d18e1c436a723a2ceae98a298d1d1f2344356e402045fe20e33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbTrafficExtensionExtensionChains]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbTrafficExtensionExtensionChains]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbTrafficExtensionExtensionChains]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447dcf91a4876d7275d5dff564bb791f7043ee0a9ef0a988475b3ca84ce6ceda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesLbTrafficExtension.NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition",
    jsii_struct_bases=[],
    name_mapping={"cel_expression": "celExpression"},
)
class NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition:
    def __init__(self, *, cel_expression: builtins.str) -> None:
        '''
        :param cel_expression: A Common Expression Language (CEL) expression that is used to match requests for which the extension chain is executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#cel_expression NetworkServicesLbTrafficExtension#cel_expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e76b13797026cfabae564125be9e5984024f8c3bd15e52ca998e3aa7d1e188)
            check_type(argname="argument cel_expression", value=cel_expression, expected_type=type_hints["cel_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cel_expression": cel_expression,
        }

    @builtins.property
    def cel_expression(self) -> builtins.str:
        '''A Common Expression Language (CEL) expression that is used to match requests for which the extension chain is executed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#cel_expression NetworkServicesLbTrafficExtension#cel_expression}
        '''
        result = self._values.get("cel_expression")
        assert result is not None, "Required property 'cel_expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesLbTrafficExtensionExtensionChainsMatchConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbTrafficExtension.NetworkServicesLbTrafficExtensionExtensionChainsMatchConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42174e19abf449041d99ece18536fd3cc6ed26572e95e6201cb095d6ae7bff29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc64fffb7dff0ac13abef7abe5a7815b8bdcc1a5f783a2b6098c49a642f0dcee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "celExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition]:
        return typing.cast(typing.Optional[NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b2bdd4cbfcd893e61ff0468c7faf9535eaed03c0fe797959f803bb625cda72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesLbTrafficExtensionExtensionChainsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbTrafficExtension.NetworkServicesLbTrafficExtensionExtensionChainsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__610d149779219c12dde6a4e81ec8046978665104d5b7838c308ede5aa97531c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExtensions")
    def put_extensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesLbTrafficExtensionExtensionChainsExtensions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5084d4b5c30e93f5e4b54e9a0b074e65eb84316821217b0a162be6129a8850bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtensions", [value]))

    @jsii.member(jsii_name="putMatchCondition")
    def put_match_condition(self, *, cel_expression: builtins.str) -> None:
        '''
        :param cel_expression: A Common Expression Language (CEL) expression that is used to match requests for which the extension chain is executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#cel_expression NetworkServicesLbTrafficExtension#cel_expression}
        '''
        value = NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition(
            cel_expression=cel_expression
        )

        return typing.cast(None, jsii.invoke(self, "putMatchCondition", [value]))

    @builtins.property
    @jsii.member(jsii_name="extensions")
    def extensions(
        self,
    ) -> NetworkServicesLbTrafficExtensionExtensionChainsExtensionsList:
        return typing.cast(NetworkServicesLbTrafficExtensionExtensionChainsExtensionsList, jsii.get(self, "extensions"))

    @builtins.property
    @jsii.member(jsii_name="matchCondition")
    def match_condition(
        self,
    ) -> NetworkServicesLbTrafficExtensionExtensionChainsMatchConditionOutputReference:
        return typing.cast(NetworkServicesLbTrafficExtensionExtensionChainsMatchConditionOutputReference, jsii.get(self, "matchCondition"))

    @builtins.property
    @jsii.member(jsii_name="extensionsInput")
    def extensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbTrafficExtensionExtensionChainsExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbTrafficExtensionExtensionChainsExtensions]]], jsii.get(self, "extensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchConditionInput")
    def match_condition_input(
        self,
    ) -> typing.Optional[NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition]:
        return typing.cast(typing.Optional[NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition], jsii.get(self, "matchConditionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__44dea3dffbb25230afb2f47b1604ce19bd7571ebf29c07972dc22ec57062c3b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbTrafficExtensionExtensionChains]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbTrafficExtensionExtensionChains]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbTrafficExtensionExtensionChains]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d44b80f576d57486733d7d3b79ff6e93686c00573e8400cd93e315c6d9f3fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesLbTrafficExtension.NetworkServicesLbTrafficExtensionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkServicesLbTrafficExtensionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#create NetworkServicesLbTrafficExtension#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#delete NetworkServicesLbTrafficExtension#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#update NetworkServicesLbTrafficExtension#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b750b287dba9e63f43a44fd43cbb54e26546dacbb8f44fba256c8c64e8f654c5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#create NetworkServicesLbTrafficExtension#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#delete NetworkServicesLbTrafficExtension#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_lb_traffic_extension#update NetworkServicesLbTrafficExtension#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesLbTrafficExtensionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesLbTrafficExtensionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesLbTrafficExtension.NetworkServicesLbTrafficExtensionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c05838b54c2e37820439cb1e1955d57ba6ae96e0664e360c227ffa1ce0ea65c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc8b8224db0fdb764ebb3b79f75b1b086e2d1d0fa1f392cbc6d747576a867b26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78104666983080973defa494424873d67e414bde6f5a092c106e24241d9f432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3cb81a21fa37dde02b615de776e7dd4314d3b8decccff9f3bf672605d595246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbTrafficExtensionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbTrafficExtensionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbTrafficExtensionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec98bf82fea6c252e4f2c5d5c5f2c200578c46b461378055d3fbb4877cebc7cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkServicesLbTrafficExtension",
    "NetworkServicesLbTrafficExtensionConfig",
    "NetworkServicesLbTrafficExtensionExtensionChains",
    "NetworkServicesLbTrafficExtensionExtensionChainsExtensions",
    "NetworkServicesLbTrafficExtensionExtensionChainsExtensionsList",
    "NetworkServicesLbTrafficExtensionExtensionChainsExtensionsOutputReference",
    "NetworkServicesLbTrafficExtensionExtensionChainsList",
    "NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition",
    "NetworkServicesLbTrafficExtensionExtensionChainsMatchConditionOutputReference",
    "NetworkServicesLbTrafficExtensionExtensionChainsOutputReference",
    "NetworkServicesLbTrafficExtensionTimeouts",
    "NetworkServicesLbTrafficExtensionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3bd4d233ff08ea64ba403631d0ee20f7505e5cf95ca1a37f5483c5abbe3788a1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    extension_chains: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesLbTrafficExtensionExtensionChains, typing.Dict[builtins.str, typing.Any]]]],
    forwarding_rules: typing.Sequence[builtins.str],
    location: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesLbTrafficExtensionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__01f9cc86dc5d91b6b0df70626aff73515fcad88858b993f65e3d560c39947f5e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c781256f1ee90de875f19125a49e89b5e180c770d03cf26d3959f83ea0835f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesLbTrafficExtensionExtensionChains, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f36c0e901af456a4f7eb814f9cb7d160fe63f8482ff28160418201866e9a8d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826dafcecb965ab34a6977616f47645d53192fb9f31a8315790c735e63a68666(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9bf8ce21223de686b762bc34bf58001eb16e5f54344ad7753e8b12aa63c67a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a7f10c77aff4c0830416495be84a26b90f2355cf78ed666dececc1d7241d6a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27f7b9d43afb4d2b0e32d71efb4e15f3d921317f4473877bc7bd4a9fd51f518(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d619c90dc8198e06a1905ab48680151a0411c4bb2689a365207aa53e10ef8059(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4988e451a4143b72003cae494c039c147382a627dad7463e0336d25eea944d71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3195c06fb3d6935eafb18dc352478d7f352ed5a17b060ee3f8f65c14f01d3539(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4438ebebddac59e064eeee87d75ff8631e7d09a7396d5010e1fb7d00a18004(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    extension_chains: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesLbTrafficExtensionExtensionChains, typing.Dict[builtins.str, typing.Any]]]],
    forwarding_rules: typing.Sequence[builtins.str],
    location: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesLbTrafficExtensionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ac4c01a0db85ea03d504a4bd904deaba3112dcd905b6283f1535ccb02db89e(
    *,
    extensions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesLbTrafficExtensionExtensionChainsExtensions, typing.Dict[builtins.str, typing.Any]]]],
    match_condition: typing.Union[NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c78c3bcc98112bd915290d0234dd89380fad107712d149e628df89783e25098(
    *,
    name: builtins.str,
    service: builtins.str,
    authority: typing.Optional[builtins.str] = None,
    fail_open: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forward_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    supported_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e57aeec91d70befd0c2e23f770366879db4761a276527c50f513846477ddefb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9903b44a3fb204ba98b107d05ef64896fd2e6ab37073584731f49d060b934402(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830fe84ca958c9e26689c46e6c86050b5a31c3ac7639ad1da6dd62d2faf09992(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e0b97a1c3e917276b8024e1d157a3342c2946c94aeea8c005ed529003462aa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7fdfcc0d774b721c46779b4735963d7b8821efc6a368ffb7c6c2f0ae64d1379(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c928285159782cff4468308591033c7ebe27e3d31b1461e7d599ae4d3f25d8cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbTrafficExtensionExtensionChainsExtensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab36519c347416ffa28fd141c576792fc44ee7cc69374b5b389807a500aeead6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0affaa2db6cadbe175b9b72dfea7cc80de7c0d2fda2941ef108292a5fc93ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00fbf81ad3a6fe038ae5030d7b4a251e393b2db5ea3d7d9ca1af64bd492c2c5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6a458bfbe023ce59ce46fb9857b0d076377f10079da2a5c6013fff3617ee78(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755575a1877ee026a0ac37373d77a12acb156a90818de8fde3c0b914a2ba7196(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80666537be11b5a0714b8529c4b3da315e38e11fd502db3f1292bd792fa171a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82bc6c1efd864f3e89a422267dbeefd02030914539fa0b590eaecc7be7e1b7f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1acb0a2a75916a20f608d827b6ebb17c8f3e50716d16e4f36ec520b3cfe334ad(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09cbad874ed36650eb540833f7d1799686f2e30262432703dc910dfa2022da1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569d096f93cb902c9ff10f01b22e360bd850c345d3b46f4140cfc50c60974825(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbTrafficExtensionExtensionChainsExtensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a6ee5ec49a6a2d04e6b520dac79a1f546cbd9b55d19ba6d17e664df1dc22ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88633611fc7f1f7773892499a85bcd36f94b2719cfadeb77cd32d3254e059722(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa40bcfa9f46be7bcee2119d0d3d213b1aa4726b7d43a5082f90c935bce25db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906114c81ed18319c6e6766e3e98e71f6a7efa2b651a9d5cc873d5e05b35ec11(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0162fcf2f3218d18e1c436a723a2ceae98a298d1d1f2344356e402045fe20e33(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447dcf91a4876d7275d5dff564bb791f7043ee0a9ef0a988475b3ca84ce6ceda(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesLbTrafficExtensionExtensionChains]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e76b13797026cfabae564125be9e5984024f8c3bd15e52ca998e3aa7d1e188(
    *,
    cel_expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42174e19abf449041d99ece18536fd3cc6ed26572e95e6201cb095d6ae7bff29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc64fffb7dff0ac13abef7abe5a7815b8bdcc1a5f783a2b6098c49a642f0dcee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b2bdd4cbfcd893e61ff0468c7faf9535eaed03c0fe797959f803bb625cda72(
    value: typing.Optional[NetworkServicesLbTrafficExtensionExtensionChainsMatchCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610d149779219c12dde6a4e81ec8046978665104d5b7838c308ede5aa97531c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5084d4b5c30e93f5e4b54e9a0b074e65eb84316821217b0a162be6129a8850bf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesLbTrafficExtensionExtensionChainsExtensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44dea3dffbb25230afb2f47b1604ce19bd7571ebf29c07972dc22ec57062c3b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d44b80f576d57486733d7d3b79ff6e93686c00573e8400cd93e315c6d9f3fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbTrafficExtensionExtensionChains]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b750b287dba9e63f43a44fd43cbb54e26546dacbb8f44fba256c8c64e8f654c5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c05838b54c2e37820439cb1e1955d57ba6ae96e0664e360c227ffa1ce0ea65c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8b8224db0fdb764ebb3b79f75b1b086e2d1d0fa1f392cbc6d747576a867b26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78104666983080973defa494424873d67e414bde6f5a092c106e24241d9f432(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3cb81a21fa37dde02b615de776e7dd4314d3b8decccff9f3bf672605d595246(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec98bf82fea6c252e4f2c5d5c5f2c200578c46b461378055d3fbb4877cebc7cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesLbTrafficExtensionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
