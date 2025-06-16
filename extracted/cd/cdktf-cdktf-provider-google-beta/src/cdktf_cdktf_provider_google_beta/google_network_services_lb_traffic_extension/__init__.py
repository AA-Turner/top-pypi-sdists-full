r'''
# `google_network_services_lb_traffic_extension`

Refer to the Terraform Registry for docs: [`google_network_services_lb_traffic_extension`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension).
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


class GoogleNetworkServicesLbTrafficExtension(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesLbTrafficExtension.GoogleNetworkServicesLbTrafficExtension",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension google_network_services_lb_traffic_extension}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        extension_chains: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesLbTrafficExtensionExtensionChains", typing.Dict[builtins.str, typing.Any]]]],
        forwarding_rules: typing.Sequence[builtins.str],
        location: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkServicesLbTrafficExtensionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension google_network_services_lb_traffic_extension} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param extension_chains: extension_chains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#extension_chains GoogleNetworkServicesLbTrafficExtension#extension_chains}
        :param forwarding_rules: A list of references to the forwarding rules to which this service extension is attached to. At least one forwarding rule is required. There can be only one LBTrafficExtension resource per forwarding rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#forwarding_rules GoogleNetworkServicesLbTrafficExtension#forwarding_rules}
        :param location: The location of the traffic extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#location GoogleNetworkServicesLbTrafficExtension#location}
        :param name: Name of the LbTrafficExtension resource in the following format: projects/{project}/locations/{location}/lbTrafficExtensions/{lbTrafficExtension}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#name GoogleNetworkServicesLbTrafficExtension#name}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#description GoogleNetworkServicesLbTrafficExtension#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#id GoogleNetworkServicesLbTrafficExtension#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the LbTrafficExtension resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#labels GoogleNetworkServicesLbTrafficExtension#labels}
        :param load_balancing_scheme: All backend services and forwarding rules referenced by this extension must share the same load balancing scheme. For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_ and `Supported application load balancers <https://cloud.google.com/service-extensions/docs/callouts-overview#supported-lbs>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#load_balancing_scheme GoogleNetworkServicesLbTrafficExtension#load_balancing_scheme}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#project GoogleNetworkServicesLbTrafficExtension#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#timeouts GoogleNetworkServicesLbTrafficExtension#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09bb1e9640c4151952238b94e219f28d8e59eacabf35b117a7cbe9a91c832d25)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetworkServicesLbTrafficExtensionConfig(
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
        '''Generates CDKTF code for importing a GoogleNetworkServicesLbTrafficExtension resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetworkServicesLbTrafficExtension to import.
        :param import_from_id: The id of the existing GoogleNetworkServicesLbTrafficExtension that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetworkServicesLbTrafficExtension to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aebfd80b1663b0f1e454dbd79e3e809966b411d6f3cb050fc87c0b5900155f27)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExtensionChains")
    def put_extension_chains(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesLbTrafficExtensionExtensionChains", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3036d7d850d69eddb5990bd2f18902817269ffe8dc1ba316dd3cfd5169fd57)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#create GoogleNetworkServicesLbTrafficExtension#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#delete GoogleNetworkServicesLbTrafficExtension#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#update GoogleNetworkServicesLbTrafficExtension#update}.
        '''
        value = GoogleNetworkServicesLbTrafficExtensionTimeouts(
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
    ) -> "GoogleNetworkServicesLbTrafficExtensionExtensionChainsList":
        return typing.cast("GoogleNetworkServicesLbTrafficExtensionExtensionChainsList", jsii.get(self, "extensionChains"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleNetworkServicesLbTrafficExtensionTimeoutsOutputReference":
        return typing.cast("GoogleNetworkServicesLbTrafficExtensionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionChainsInput")
    def extension_chains_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesLbTrafficExtensionExtensionChains"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesLbTrafficExtensionExtensionChains"]]], jsii.get(self, "extensionChainsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkServicesLbTrafficExtensionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkServicesLbTrafficExtensionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f2cc94ba75c091c5adbf8e435912424811551de17d6bfd53483c0507dde561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardingRules")
    def forwarding_rules(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "forwardingRules"))

    @forwarding_rules.setter
    def forwarding_rules(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933f0d8fdf1b8933a67a15ff2afe57aad4180c8f3360f143ccd4a9a763538d9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardingRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6284d7967bc7829c0616c6aa28fb6ec0d8328e7633ac431f3c8d7ec3e6da331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b00dc70a5f9fa33bfa67c7377e0119de50806272aa5b031ed4063291259fa26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e6ee1aac1143dadc033492eebee6ebe73532fcc6d7a880f727e610e1f42e2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20163ed3de285014c1ce8e9cd0f2d6e0b96c4ece40903f8333efeed22766c3bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddfd63b6a25f07ed6ad55d8cdb7550f60de64facf31a13c227d404bc0b3c9bc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737a5c697395811e03642f4240a23dc4ff9442d9bb227b29efa5e3cc8da5e932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesLbTrafficExtension.GoogleNetworkServicesLbTrafficExtensionConfig",
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
class GoogleNetworkServicesLbTrafficExtensionConfig(
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
        extension_chains: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesLbTrafficExtensionExtensionChains", typing.Dict[builtins.str, typing.Any]]]],
        forwarding_rules: typing.Sequence[builtins.str],
        location: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkServicesLbTrafficExtensionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param extension_chains: extension_chains block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#extension_chains GoogleNetworkServicesLbTrafficExtension#extension_chains}
        :param forwarding_rules: A list of references to the forwarding rules to which this service extension is attached to. At least one forwarding rule is required. There can be only one LBTrafficExtension resource per forwarding rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#forwarding_rules GoogleNetworkServicesLbTrafficExtension#forwarding_rules}
        :param location: The location of the traffic extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#location GoogleNetworkServicesLbTrafficExtension#location}
        :param name: Name of the LbTrafficExtension resource in the following format: projects/{project}/locations/{location}/lbTrafficExtensions/{lbTrafficExtension}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#name GoogleNetworkServicesLbTrafficExtension#name}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#description GoogleNetworkServicesLbTrafficExtension#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#id GoogleNetworkServicesLbTrafficExtension#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the LbTrafficExtension resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#labels GoogleNetworkServicesLbTrafficExtension#labels}
        :param load_balancing_scheme: All backend services and forwarding rules referenced by this extension must share the same load balancing scheme. For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_ and `Supported application load balancers <https://cloud.google.com/service-extensions/docs/callouts-overview#supported-lbs>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#load_balancing_scheme GoogleNetworkServicesLbTrafficExtension#load_balancing_scheme}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#project GoogleNetworkServicesLbTrafficExtension#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#timeouts GoogleNetworkServicesLbTrafficExtension#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetworkServicesLbTrafficExtensionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dcb026067be4426aadc30b6751fdd77c3030861290c492e4cce50ee56158bef)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesLbTrafficExtensionExtensionChains"]]:
        '''extension_chains block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#extension_chains GoogleNetworkServicesLbTrafficExtension#extension_chains}
        '''
        result = self._values.get("extension_chains")
        assert result is not None, "Required property 'extension_chains' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesLbTrafficExtensionExtensionChains"]], result)

    @builtins.property
    def forwarding_rules(self) -> typing.List[builtins.str]:
        '''A list of references to the forwarding rules to which this service extension is attached to.

        At least one forwarding rule is required. There can be only one LBTrafficExtension resource per forwarding rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#forwarding_rules GoogleNetworkServicesLbTrafficExtension#forwarding_rules}
        '''
        result = self._values.get("forwarding_rules")
        assert result is not None, "Required property 'forwarding_rules' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the traffic extension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#location GoogleNetworkServicesLbTrafficExtension#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the LbTrafficExtension resource in the following format: projects/{project}/locations/{location}/lbTrafficExtensions/{lbTrafficExtension}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#name GoogleNetworkServicesLbTrafficExtension#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#description GoogleNetworkServicesLbTrafficExtension#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#id GoogleNetworkServicesLbTrafficExtension#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#labels GoogleNetworkServicesLbTrafficExtension#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def load_balancing_scheme(self) -> typing.Optional[builtins.str]:
        '''All backend services and forwarding rules referenced by this extension must share the same load balancing scheme.

        For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_ and
        `Supported application load balancers <https://cloud.google.com/service-extensions/docs/callouts-overview#supported-lbs>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#load_balancing_scheme GoogleNetworkServicesLbTrafficExtension#load_balancing_scheme}
        '''
        result = self._values.get("load_balancing_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#project GoogleNetworkServicesLbTrafficExtension#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleNetworkServicesLbTrafficExtensionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#timeouts GoogleNetworkServicesLbTrafficExtension#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetworkServicesLbTrafficExtensionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesLbTrafficExtensionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesLbTrafficExtension.GoogleNetworkServicesLbTrafficExtensionExtensionChains",
    jsii_struct_bases=[],
    name_mapping={
        "extensions": "extensions",
        "match_condition": "matchCondition",
        "name": "name",
    },
)
class GoogleNetworkServicesLbTrafficExtensionExtensionChains:
    def __init__(
        self,
        *,
        extensions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions", typing.Dict[builtins.str, typing.Any]]]],
        match_condition: typing.Union["GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param extensions: extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#extensions GoogleNetworkServicesLbTrafficExtension#extensions}
        :param match_condition: match_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#match_condition GoogleNetworkServicesLbTrafficExtension#match_condition}
        :param name: The name for this extension chain. The name is logged as part of the HTTP request logs. The name must conform with RFC-1034, is restricted to lower-cased letters, numbers and hyphens, and can have a maximum length of 63 characters. Additionally, the first character must be a letter and the last a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#name GoogleNetworkServicesLbTrafficExtension#name}
        '''
        if isinstance(match_condition, dict):
            match_condition = GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition(**match_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9633ae7a20dd409047a2982d08804a3b8a680956c6d4b9f64538e3b6e1791cac)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions"]]:
        '''extensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#extensions GoogleNetworkServicesLbTrafficExtension#extensions}
        '''
        result = self._values.get("extensions")
        assert result is not None, "Required property 'extensions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions"]], result)

    @builtins.property
    def match_condition(
        self,
    ) -> "GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition":
        '''match_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#match_condition GoogleNetworkServicesLbTrafficExtension#match_condition}
        '''
        result = self._values.get("match_condition")
        assert result is not None, "Required property 'match_condition' is missing"
        return typing.cast("GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for this extension chain.

        The name is logged as part of the HTTP request logs.
        The name must conform with RFC-1034, is restricted to lower-cased letters, numbers and hyphens,
        and can have a maximum length of 63 characters. Additionally, the first character must be a letter
        and the last a letter or a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#name GoogleNetworkServicesLbTrafficExtension#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesLbTrafficExtensionExtensionChains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesLbTrafficExtension.GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions",
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
class GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions:
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
        :param name: The name for this extension. The name is logged as part of the HTTP request logs. The name must conform with RFC-1034, is restricted to lower-cased letters, numbers and hyphens, and can have a maximum length of 63 characters. Additionally, the first character must be a letter and the last a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#name GoogleNetworkServicesLbTrafficExtension#name}
        :param service: The reference to the service that runs the extension. Must be a reference to a backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#service GoogleNetworkServicesLbTrafficExtension#service}
        :param authority: The :authority header in the gRPC request sent from Envoy to the extension service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#authority GoogleNetworkServicesLbTrafficExtension#authority}
        :param fail_open: Determines how the proxy behaves if the call to the extension fails or times out. When set to TRUE, request or response processing continues without error. Any subsequent extensions in the extension chain are also executed. When set to FALSE: * If response headers have not been delivered to the downstream client, a generic 500 error is returned to the client. The error response can be tailored by configuring a custom error response in the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#fail_open GoogleNetworkServicesLbTrafficExtension#fail_open}
        :param forward_headers: List of the HTTP headers to forward to the extension (from the client or backend). If omitted, all headers are sent. Each element is a string indicating the header name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#forward_headers GoogleNetworkServicesLbTrafficExtension#forward_headers}
        :param metadata: Metadata associated with the extension. This field is used to pass metadata to the extension service. You can set up key value pairs for metadata as you like and need. f.e. {"key": "value", "key2": "value2"}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#metadata GoogleNetworkServicesLbTrafficExtension#metadata}
        :param supported_events: A set of events during request or response processing for which this extension is called. This field is required for the LbTrafficExtension resource. It's not relevant for the LbRouteExtension resource. Possible values:'EVENT_TYPE_UNSPECIFIED', 'REQUEST_HEADERS', 'REQUEST_BODY', 'RESPONSE_HEADERS', 'RESPONSE_BODY', 'RESPONSE_BODY' and 'RESPONSE_BODY'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#supported_events GoogleNetworkServicesLbTrafficExtension#supported_events}
        :param timeout: Specifies the timeout for each individual message on the stream. The timeout must be between 10-1000 milliseconds. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#timeout GoogleNetworkServicesLbTrafficExtension#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0004767036cc9b6b7757909a40b29942981e39ba6bd0c26c9dfae21ef53a6e0f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#name GoogleNetworkServicesLbTrafficExtension#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''The reference to the service that runs the extension. Must be a reference to a backend service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#service GoogleNetworkServicesLbTrafficExtension#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authority(self) -> typing.Optional[builtins.str]:
        '''The :authority header in the gRPC request sent from Envoy to the extension service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#authority GoogleNetworkServicesLbTrafficExtension#authority}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#fail_open GoogleNetworkServicesLbTrafficExtension#fail_open}
        '''
        result = self._values.get("fail_open")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forward_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of the HTTP headers to forward to the extension (from the client or backend).

        If omitted, all headers are sent. Each element is a string indicating the header name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#forward_headers GoogleNetworkServicesLbTrafficExtension#forward_headers}
        '''
        result = self._values.get("forward_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata associated with the extension.

        This field is used to pass metadata to the extension service.
        You can set up key value pairs for metadata as you like and need.
        f.e. {"key": "value", "key2": "value2"}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#metadata GoogleNetworkServicesLbTrafficExtension#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def supported_events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of events during request or response processing for which this extension is called.

        This field is required for the LbTrafficExtension resource. It's not relevant for the LbRouteExtension
        resource. Possible values:'EVENT_TYPE_UNSPECIFIED', 'REQUEST_HEADERS', 'REQUEST_BODY', 'RESPONSE_HEADERS',
        'RESPONSE_BODY', 'RESPONSE_BODY' and 'RESPONSE_BODY'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#supported_events GoogleNetworkServicesLbTrafficExtension#supported_events}
        '''
        result = self._values.get("supported_events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Specifies the timeout for each individual message on the stream.

        The timeout must be between 10-1000 milliseconds.
        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#timeout GoogleNetworkServicesLbTrafficExtension#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesLbTrafficExtension.GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03c62cc2a23749c642de0bebc55d71caabec415fd381482ceb41fdc18038791c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d27d4c8752347ad399ee84c80f1abd51b41950e658bdddd7e8db90c54043c56b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b50f260c16739a1eaa2a97080d6ece6b6e1fed4257742e0f7d6ce2cce682dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b49688c8b1eebcb46c8b6a5a1d29db38eb5e7863caf75028228f47088ee70706)
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
            type_hints = typing.get_type_hints(_typecheckingstub__644d8f4e1fcfa51316e0244b011fd5a207ebb5f2b440200b8cfdb112421c9ed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0a8c899034d3bb85d34a392d5a3015ad0c90a87ee590ffcaad9b4facc2643b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesLbTrafficExtension.GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94b05c242e2d32559c8be49aa3d3f6d7379f1b3619aaa1e5dcde2f6551976a6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54a32b3a81302f96b89dbaf6b8e010ae63c2ee0154f08cf50bae9b85a382f36b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fef3b22d8e147c9865273c5eec18b018b06f85dcd8493569a63b4bb96169ed94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOpen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardHeaders")
    def forward_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "forwardHeaders"))

    @forward_headers.setter
    def forward_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5462067c77a2443304b763490257a9eb175463f342a519348589b04351e04eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13bdd76faf716902dcbff575646b9c66ca68db5b75990bd0870d9760c2fb9f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23d2802894a9dab73954f70f0f9f5447efc0e2cbe60b208615f197bf8739f14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5def115c8efa28b72399b93e4140e89ab101d2f73d02417b3ed9d15262314c3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportedEvents")
    def supported_events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedEvents"))

    @supported_events.setter
    def supported_events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45dfd06cefe89f499ffb2e9b7c3d4b903f094ba1b23bf6024ca61fbe3be2031e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportedEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c27371a86e6ea3154bc5a95ae7e6a508292371e111314f281d7dfd3f88c099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7448dcd90b0bd7aa53ff3a5070502651f5015f56cf53c35ad7d8c82ecd50e40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesLbTrafficExtensionExtensionChainsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesLbTrafficExtension.GoogleNetworkServicesLbTrafficExtensionExtensionChainsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adc2194d6063e29f966ec93b67abf58527c6744f1b3d049959fb3a2c07124185)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesLbTrafficExtensionExtensionChainsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34cebc239f450992c3da4e365607ba61896d56805b9c6dbbc745d332d9c71af)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesLbTrafficExtensionExtensionChainsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac80fd7539b448af5fbc63890b2d2e06c1f70c9d326d54189b5e7c7b337af93b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ef8d971baff6f6a9b068bac21ed7c8ea9e22de92a1e7d843de7bf9dc3830560)
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
            type_hints = typing.get_type_hints(_typecheckingstub__880a1cd6987bfa6982aaeb41511507e46ce18c93b021bf6fdb91e7e8e60a78b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesLbTrafficExtensionExtensionChains]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesLbTrafficExtensionExtensionChains]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesLbTrafficExtensionExtensionChains]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe8c1a5b482701b334cbf417106c311a8b0f555246522165ad85a0c022864b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesLbTrafficExtension.GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition",
    jsii_struct_bases=[],
    name_mapping={"cel_expression": "celExpression"},
)
class GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition:
    def __init__(self, *, cel_expression: builtins.str) -> None:
        '''
        :param cel_expression: A Common Expression Language (CEL) expression that is used to match requests for which the extension chain is executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#cel_expression GoogleNetworkServicesLbTrafficExtension#cel_expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1299adccf0eaf62c89ec5d5550498ad68453a9b691339841b27c16f4b37b1128)
            check_type(argname="argument cel_expression", value=cel_expression, expected_type=type_hints["cel_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cel_expression": cel_expression,
        }

    @builtins.property
    def cel_expression(self) -> builtins.str:
        '''A Common Expression Language (CEL) expression that is used to match requests for which the extension chain is executed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#cel_expression GoogleNetworkServicesLbTrafficExtension#cel_expression}
        '''
        result = self._values.get("cel_expression")
        assert result is not None, "Required property 'cel_expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesLbTrafficExtension.GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaf14d558b5bbc6f5eec239b3411c057289b669701bcca1aeec8c02c8d746b37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c047f0f2a960e4daf6bda02427ce94e694781707fe2a36a977b08d98b0b98c14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "celExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition]:
        return typing.cast(typing.Optional[GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b467e67c4fe7e14c7de14b9af07698c7160d3ce45fa17a01049b42e6d62ac28d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesLbTrafficExtensionExtensionChainsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesLbTrafficExtension.GoogleNetworkServicesLbTrafficExtensionExtensionChainsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5017e0c8fc1d91a4c96e912f50d1394b3c8b68fd4526b2ebf2b1d834d6917799)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExtensions")
    def put_extensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ac5c5bb9ad4c70750e2042f611e77ae5f20016d2d65cb531fed825dd43f7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtensions", [value]))

    @jsii.member(jsii_name="putMatchCondition")
    def put_match_condition(self, *, cel_expression: builtins.str) -> None:
        '''
        :param cel_expression: A Common Expression Language (CEL) expression that is used to match requests for which the extension chain is executed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#cel_expression GoogleNetworkServicesLbTrafficExtension#cel_expression}
        '''
        value = GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition(
            cel_expression=cel_expression
        )

        return typing.cast(None, jsii.invoke(self, "putMatchCondition", [value]))

    @builtins.property
    @jsii.member(jsii_name="extensions")
    def extensions(
        self,
    ) -> GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensionsList:
        return typing.cast(GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensionsList, jsii.get(self, "extensions"))

    @builtins.property
    @jsii.member(jsii_name="matchCondition")
    def match_condition(
        self,
    ) -> GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchConditionOutputReference:
        return typing.cast(GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchConditionOutputReference, jsii.get(self, "matchCondition"))

    @builtins.property
    @jsii.member(jsii_name="extensionsInput")
    def extensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions]]], jsii.get(self, "extensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchConditionInput")
    def match_condition_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition]:
        return typing.cast(typing.Optional[GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition], jsii.get(self, "matchConditionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__820153fc5a9b27fc4a5eaf3ad66a996c88d483c8ad3adffd71f51f953f234da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesLbTrafficExtensionExtensionChains]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesLbTrafficExtensionExtensionChains]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesLbTrafficExtensionExtensionChains]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dab62211a40755c52a996bb4d40eecf3371b74b1c45a358cad6cdc5440d4127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesLbTrafficExtension.GoogleNetworkServicesLbTrafficExtensionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetworkServicesLbTrafficExtensionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#create GoogleNetworkServicesLbTrafficExtension#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#delete GoogleNetworkServicesLbTrafficExtension#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#update GoogleNetworkServicesLbTrafficExtension#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__869d580eaa5961dbc320e8f15ccc32526387d2fc3351cab18c154c681de74294)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#create GoogleNetworkServicesLbTrafficExtension#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#delete GoogleNetworkServicesLbTrafficExtension#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_lb_traffic_extension#update GoogleNetworkServicesLbTrafficExtension#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesLbTrafficExtensionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesLbTrafficExtensionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesLbTrafficExtension.GoogleNetworkServicesLbTrafficExtensionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89e953de2df80db5429ee7f32d358f2e19e9fc8372743677450b7bab96fbf5e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e074f643597d8dde400a43503f18c827c5d0ffa21433e0dc9d688dfe9fa2bd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e76646b130f94f9f651e4dd35d39b1ac9328aeaf15a25011b7b7751527687c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d46b3a27b6b79a4180da893bad9f43ca0315218f50b2f92eedd441cb2b4624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesLbTrafficExtensionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesLbTrafficExtensionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesLbTrafficExtensionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__452eb41439d36569e502299c9540610b6f77bdae6b8821fc577e882c979d6bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetworkServicesLbTrafficExtension",
    "GoogleNetworkServicesLbTrafficExtensionConfig",
    "GoogleNetworkServicesLbTrafficExtensionExtensionChains",
    "GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions",
    "GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensionsList",
    "GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensionsOutputReference",
    "GoogleNetworkServicesLbTrafficExtensionExtensionChainsList",
    "GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition",
    "GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchConditionOutputReference",
    "GoogleNetworkServicesLbTrafficExtensionExtensionChainsOutputReference",
    "GoogleNetworkServicesLbTrafficExtensionTimeouts",
    "GoogleNetworkServicesLbTrafficExtensionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__09bb1e9640c4151952238b94e219f28d8e59eacabf35b117a7cbe9a91c832d25(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    extension_chains: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesLbTrafficExtensionExtensionChains, typing.Dict[builtins.str, typing.Any]]]],
    forwarding_rules: typing.Sequence[builtins.str],
    location: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkServicesLbTrafficExtensionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__aebfd80b1663b0f1e454dbd79e3e809966b411d6f3cb050fc87c0b5900155f27(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3036d7d850d69eddb5990bd2f18902817269ffe8dc1ba316dd3cfd5169fd57(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesLbTrafficExtensionExtensionChains, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f2cc94ba75c091c5adbf8e435912424811551de17d6bfd53483c0507dde561(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933f0d8fdf1b8933a67a15ff2afe57aad4180c8f3360f143ccd4a9a763538d9f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6284d7967bc7829c0616c6aa28fb6ec0d8328e7633ac431f3c8d7ec3e6da331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b00dc70a5f9fa33bfa67c7377e0119de50806272aa5b031ed4063291259fa26(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e6ee1aac1143dadc033492eebee6ebe73532fcc6d7a880f727e610e1f42e2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20163ed3de285014c1ce8e9cd0f2d6e0b96c4ece40903f8333efeed22766c3bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfd63b6a25f07ed6ad55d8cdb7550f60de64facf31a13c227d404bc0b3c9bc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737a5c697395811e03642f4240a23dc4ff9442d9bb227b29efa5e3cc8da5e932(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dcb026067be4426aadc30b6751fdd77c3030861290c492e4cce50ee56158bef(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    extension_chains: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesLbTrafficExtensionExtensionChains, typing.Dict[builtins.str, typing.Any]]]],
    forwarding_rules: typing.Sequence[builtins.str],
    location: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkServicesLbTrafficExtensionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9633ae7a20dd409047a2982d08804a3b8a680956c6d4b9f64538e3b6e1791cac(
    *,
    extensions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions, typing.Dict[builtins.str, typing.Any]]]],
    match_condition: typing.Union[GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0004767036cc9b6b7757909a40b29942981e39ba6bd0c26c9dfae21ef53a6e0f(
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

def _typecheckingstub__03c62cc2a23749c642de0bebc55d71caabec415fd381482ceb41fdc18038791c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27d4c8752347ad399ee84c80f1abd51b41950e658bdddd7e8db90c54043c56b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b50f260c16739a1eaa2a97080d6ece6b6e1fed4257742e0f7d6ce2cce682dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49688c8b1eebcb46c8b6a5a1d29db38eb5e7863caf75028228f47088ee70706(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644d8f4e1fcfa51316e0244b011fd5a207ebb5f2b440200b8cfdb112421c9ed2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a8c899034d3bb85d34a392d5a3015ad0c90a87ee590ffcaad9b4facc2643b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b05c242e2d32559c8be49aa3d3f6d7379f1b3619aaa1e5dcde2f6551976a6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a32b3a81302f96b89dbaf6b8e010ae63c2ee0154f08cf50bae9b85a382f36b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef3b22d8e147c9865273c5eec18b018b06f85dcd8493569a63b4bb96169ed94(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5462067c77a2443304b763490257a9eb175463f342a519348589b04351e04eb2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13bdd76faf716902dcbff575646b9c66ca68db5b75990bd0870d9760c2fb9f7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23d2802894a9dab73954f70f0f9f5447efc0e2cbe60b208615f197bf8739f14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5def115c8efa28b72399b93e4140e89ab101d2f73d02417b3ed9d15262314c3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45dfd06cefe89f499ffb2e9b7c3d4b903f094ba1b23bf6024ca61fbe3be2031e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c27371a86e6ea3154bc5a95ae7e6a508292371e111314f281d7dfd3f88c099(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7448dcd90b0bd7aa53ff3a5070502651f5015f56cf53c35ad7d8c82ecd50e40(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc2194d6063e29f966ec93b67abf58527c6744f1b3d049959fb3a2c07124185(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34cebc239f450992c3da4e365607ba61896d56805b9c6dbbc745d332d9c71af(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac80fd7539b448af5fbc63890b2d2e06c1f70c9d326d54189b5e7c7b337af93b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef8d971baff6f6a9b068bac21ed7c8ea9e22de92a1e7d843de7bf9dc3830560(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880a1cd6987bfa6982aaeb41511507e46ce18c93b021bf6fdb91e7e8e60a78b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe8c1a5b482701b334cbf417106c311a8b0f555246522165ad85a0c022864b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesLbTrafficExtensionExtensionChains]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1299adccf0eaf62c89ec5d5550498ad68453a9b691339841b27c16f4b37b1128(
    *,
    cel_expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf14d558b5bbc6f5eec239b3411c057289b669701bcca1aeec8c02c8d746b37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c047f0f2a960e4daf6bda02427ce94e694781707fe2a36a977b08d98b0b98c14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b467e67c4fe7e14c7de14b9af07698c7160d3ce45fa17a01049b42e6d62ac28d(
    value: typing.Optional[GoogleNetworkServicesLbTrafficExtensionExtensionChainsMatchCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5017e0c8fc1d91a4c96e912f50d1394b3c8b68fd4526b2ebf2b1d834d6917799(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ac5c5bb9ad4c70750e2042f611e77ae5f20016d2d65cb531fed825dd43f7eb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesLbTrafficExtensionExtensionChainsExtensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820153fc5a9b27fc4a5eaf3ad66a996c88d483c8ad3adffd71f51f953f234da3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dab62211a40755c52a996bb4d40eecf3371b74b1c45a358cad6cdc5440d4127(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesLbTrafficExtensionExtensionChains]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__869d580eaa5961dbc320e8f15ccc32526387d2fc3351cab18c154c681de74294(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e953de2df80db5429ee7f32d358f2e19e9fc8372743677450b7bab96fbf5e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e074f643597d8dde400a43503f18c827c5d0ffa21433e0dc9d688dfe9fa2bd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e76646b130f94f9f651e4dd35d39b1ac9328aeaf15a25011b7b7751527687c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d46b3a27b6b79a4180da893bad9f43ca0315218f50b2f92eedd441cb2b4624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__452eb41439d36569e502299c9540610b6f77bdae6b8821fc577e882c979d6bc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesLbTrafficExtensionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
