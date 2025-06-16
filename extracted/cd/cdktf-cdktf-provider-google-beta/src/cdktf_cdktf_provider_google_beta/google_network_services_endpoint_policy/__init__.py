r'''
# `google_network_services_endpoint_policy`

Refer to the Terraform Registry for docs: [`google_network_services_endpoint_policy`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy).
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


class GoogleNetworkServicesEndpointPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEndpointPolicy.GoogleNetworkServicesEndpointPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy google_network_services_endpoint_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        endpoint_matcher: typing.Union["GoogleNetworkServicesEndpointPolicyEndpointMatcher", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        type: builtins.str,
        authorization_policy: typing.Optional[builtins.str] = None,
        client_tls_policy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        server_tls_policy: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkServicesEndpointPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_port_selector: typing.Optional[typing.Union["GoogleNetworkServicesEndpointPolicyTrafficPortSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy google_network_services_endpoint_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param endpoint_matcher: endpoint_matcher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#endpoint_matcher GoogleNetworkServicesEndpointPolicy#endpoint_matcher}
        :param name: Name of the EndpointPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#name GoogleNetworkServicesEndpointPolicy#name}
        :param type: The type of endpoint policy. This is primarily used to validate the configuration. Possible values: ["SIDECAR_PROXY", "GRPC_SERVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#type GoogleNetworkServicesEndpointPolicy#type}
        :param authorization_policy: This field specifies the URL of AuthorizationPolicy resource that applies authorization policies to the inbound traffic at the matched endpoints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#authorization_policy GoogleNetworkServicesEndpointPolicy#authorization_policy}
        :param client_tls_policy: A URL referring to a ClientTlsPolicy resource. ClientTlsPolicy can be set to specify the authentication for traffic from the proxy to the actual endpoints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#client_tls_policy GoogleNetworkServicesEndpointPolicy#client_tls_policy}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#description GoogleNetworkServicesEndpointPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#id GoogleNetworkServicesEndpointPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the TcpRoute resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#labels GoogleNetworkServicesEndpointPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#project GoogleNetworkServicesEndpointPolicy#project}.
        :param server_tls_policy: A URL referring to ServerTlsPolicy resource. ServerTlsPolicy is used to determine the authentication policy to be applied to terminate the inbound traffic at the identified backends. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#server_tls_policy GoogleNetworkServicesEndpointPolicy#server_tls_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#timeouts GoogleNetworkServicesEndpointPolicy#timeouts}
        :param traffic_port_selector: traffic_port_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#traffic_port_selector GoogleNetworkServicesEndpointPolicy#traffic_port_selector}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a9b58fb0570f11319ffeb8705ae709d72687759b796b43df345fbaf9e6ce3e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetworkServicesEndpointPolicyConfig(
            endpoint_matcher=endpoint_matcher,
            name=name,
            type=type,
            authorization_policy=authorization_policy,
            client_tls_policy=client_tls_policy,
            description=description,
            id=id,
            labels=labels,
            project=project,
            server_tls_policy=server_tls_policy,
            timeouts=timeouts,
            traffic_port_selector=traffic_port_selector,
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
        '''Generates CDKTF code for importing a GoogleNetworkServicesEndpointPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetworkServicesEndpointPolicy to import.
        :param import_from_id: The id of the existing GoogleNetworkServicesEndpointPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetworkServicesEndpointPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d89a8a1a2ceb8bc96aca17f4b00dea56cd8e9ca00d90deb0e3f137682e4160)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEndpointMatcher")
    def put_endpoint_matcher(
        self,
        *,
        metadata_label_matcher: typing.Union["GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param metadata_label_matcher: metadata_label_matcher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#metadata_label_matcher GoogleNetworkServicesEndpointPolicy#metadata_label_matcher}
        '''
        value = GoogleNetworkServicesEndpointPolicyEndpointMatcher(
            metadata_label_matcher=metadata_label_matcher
        )

        return typing.cast(None, jsii.invoke(self, "putEndpointMatcher", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#create GoogleNetworkServicesEndpointPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#delete GoogleNetworkServicesEndpointPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#update GoogleNetworkServicesEndpointPolicy#update}.
        '''
        value = GoogleNetworkServicesEndpointPolicyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTrafficPortSelector")
    def put_traffic_port_selector(
        self,
        *,
        ports: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param ports: List of ports. Can be port numbers or port range (example, [80-90] specifies all ports from 80 to 90, including 80 and 90) or named ports or * to specify all ports. If the list is empty, all ports are selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#ports GoogleNetworkServicesEndpointPolicy#ports}
        '''
        value = GoogleNetworkServicesEndpointPolicyTrafficPortSelector(ports=ports)

        return typing.cast(None, jsii.invoke(self, "putTrafficPortSelector", [value]))

    @jsii.member(jsii_name="resetAuthorizationPolicy")
    def reset_authorization_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizationPolicy", []))

    @jsii.member(jsii_name="resetClientTlsPolicy")
    def reset_client_tls_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientTlsPolicy", []))

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

    @jsii.member(jsii_name="resetServerTlsPolicy")
    def reset_server_tls_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerTlsPolicy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTrafficPortSelector")
    def reset_traffic_port_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrafficPortSelector", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="endpointMatcher")
    def endpoint_matcher(
        self,
    ) -> "GoogleNetworkServicesEndpointPolicyEndpointMatcherOutputReference":
        return typing.cast("GoogleNetworkServicesEndpointPolicyEndpointMatcherOutputReference", jsii.get(self, "endpointMatcher"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleNetworkServicesEndpointPolicyTimeoutsOutputReference":
        return typing.cast("GoogleNetworkServicesEndpointPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trafficPortSelector")
    def traffic_port_selector(
        self,
    ) -> "GoogleNetworkServicesEndpointPolicyTrafficPortSelectorOutputReference":
        return typing.cast("GoogleNetworkServicesEndpointPolicyTrafficPortSelectorOutputReference", jsii.get(self, "trafficPortSelector"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="authorizationPolicyInput")
    def authorization_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="clientTlsPolicyInput")
    def client_tls_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientTlsPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointMatcherInput")
    def endpoint_matcher_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEndpointPolicyEndpointMatcher"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEndpointPolicyEndpointMatcher"], jsii.get(self, "endpointMatcherInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="serverTlsPolicyInput")
    def server_tls_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverTlsPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkServicesEndpointPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkServicesEndpointPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficPortSelectorInput")
    def traffic_port_selector_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEndpointPolicyTrafficPortSelector"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEndpointPolicyTrafficPortSelector"], jsii.get(self, "trafficPortSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationPolicy")
    def authorization_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationPolicy"))

    @authorization_policy.setter
    def authorization_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25047e61d4f749a8b550636cc118b6bf01c5b9c26b436d75256adcb7351ccbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTlsPolicy")
    def client_tls_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientTlsPolicy"))

    @client_tls_policy.setter
    def client_tls_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34957db1cf11431ece992e5f12c0605362ab8ecc7b179173111fa112054fe59b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTlsPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6902489867c77342268032aace4f93ab4f4abf10619438513ed9d9780ded718b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fc0c18d66dfe4d6a15b314e9a7965b0beaf687edd342498260d58ef475803b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9976fedfff9c3d18f31e17f9953eb080f2d6ba826ccf5e9ce3a9df12452287f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77289cb350af0a9ca36e6d447277b60e632169caaf6bb1a6bdc8f4b78b70d98b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1fa33dc9d1d3cc8680456dd9bbc9691274b44e18ea78eee226b7ac00c226f15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverTlsPolicy")
    def server_tls_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverTlsPolicy"))

    @server_tls_policy.setter
    def server_tls_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e34a37a59cb072a43226614cfb31020a6496fcb94fd7e333e8216dc8a98ec9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverTlsPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef11e9698f295c30ed7a61f2cb408bb2a5b9324324c4a4afc4b6b223671c76e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEndpointPolicy.GoogleNetworkServicesEndpointPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "endpoint_matcher": "endpointMatcher",
        "name": "name",
        "type": "type",
        "authorization_policy": "authorizationPolicy",
        "client_tls_policy": "clientTlsPolicy",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "server_tls_policy": "serverTlsPolicy",
        "timeouts": "timeouts",
        "traffic_port_selector": "trafficPortSelector",
    },
)
class GoogleNetworkServicesEndpointPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        endpoint_matcher: typing.Union["GoogleNetworkServicesEndpointPolicyEndpointMatcher", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        type: builtins.str,
        authorization_policy: typing.Optional[builtins.str] = None,
        client_tls_policy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        server_tls_policy: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkServicesEndpointPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_port_selector: typing.Optional[typing.Union["GoogleNetworkServicesEndpointPolicyTrafficPortSelector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param endpoint_matcher: endpoint_matcher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#endpoint_matcher GoogleNetworkServicesEndpointPolicy#endpoint_matcher}
        :param name: Name of the EndpointPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#name GoogleNetworkServicesEndpointPolicy#name}
        :param type: The type of endpoint policy. This is primarily used to validate the configuration. Possible values: ["SIDECAR_PROXY", "GRPC_SERVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#type GoogleNetworkServicesEndpointPolicy#type}
        :param authorization_policy: This field specifies the URL of AuthorizationPolicy resource that applies authorization policies to the inbound traffic at the matched endpoints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#authorization_policy GoogleNetworkServicesEndpointPolicy#authorization_policy}
        :param client_tls_policy: A URL referring to a ClientTlsPolicy resource. ClientTlsPolicy can be set to specify the authentication for traffic from the proxy to the actual endpoints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#client_tls_policy GoogleNetworkServicesEndpointPolicy#client_tls_policy}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#description GoogleNetworkServicesEndpointPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#id GoogleNetworkServicesEndpointPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the TcpRoute resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#labels GoogleNetworkServicesEndpointPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#project GoogleNetworkServicesEndpointPolicy#project}.
        :param server_tls_policy: A URL referring to ServerTlsPolicy resource. ServerTlsPolicy is used to determine the authentication policy to be applied to terminate the inbound traffic at the identified backends. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#server_tls_policy GoogleNetworkServicesEndpointPolicy#server_tls_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#timeouts GoogleNetworkServicesEndpointPolicy#timeouts}
        :param traffic_port_selector: traffic_port_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#traffic_port_selector GoogleNetworkServicesEndpointPolicy#traffic_port_selector}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(endpoint_matcher, dict):
            endpoint_matcher = GoogleNetworkServicesEndpointPolicyEndpointMatcher(**endpoint_matcher)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetworkServicesEndpointPolicyTimeouts(**timeouts)
        if isinstance(traffic_port_selector, dict):
            traffic_port_selector = GoogleNetworkServicesEndpointPolicyTrafficPortSelector(**traffic_port_selector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c548d37d90633030df3904ef243c7f53db2200b0a58ebef8571a2e52600d9510)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument endpoint_matcher", value=endpoint_matcher, expected_type=type_hints["endpoint_matcher"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument authorization_policy", value=authorization_policy, expected_type=type_hints["authorization_policy"])
            check_type(argname="argument client_tls_policy", value=client_tls_policy, expected_type=type_hints["client_tls_policy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument server_tls_policy", value=server_tls_policy, expected_type=type_hints["server_tls_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument traffic_port_selector", value=traffic_port_selector, expected_type=type_hints["traffic_port_selector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint_matcher": endpoint_matcher,
            "name": name,
            "type": type,
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
        if authorization_policy is not None:
            self._values["authorization_policy"] = authorization_policy
        if client_tls_policy is not None:
            self._values["client_tls_policy"] = client_tls_policy
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if server_tls_policy is not None:
            self._values["server_tls_policy"] = server_tls_policy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if traffic_port_selector is not None:
            self._values["traffic_port_selector"] = traffic_port_selector

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
    def endpoint_matcher(self) -> "GoogleNetworkServicesEndpointPolicyEndpointMatcher":
        '''endpoint_matcher block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#endpoint_matcher GoogleNetworkServicesEndpointPolicy#endpoint_matcher}
        '''
        result = self._values.get("endpoint_matcher")
        assert result is not None, "Required property 'endpoint_matcher' is missing"
        return typing.cast("GoogleNetworkServicesEndpointPolicyEndpointMatcher", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the EndpointPolicy resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#name GoogleNetworkServicesEndpointPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of endpoint policy. This is primarily used to validate the configuration. Possible values: ["SIDECAR_PROXY", "GRPC_SERVER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#type GoogleNetworkServicesEndpointPolicy#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_policy(self) -> typing.Optional[builtins.str]:
        '''This field specifies the URL of AuthorizationPolicy resource that applies authorization policies to the inbound traffic at the matched endpoints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#authorization_policy GoogleNetworkServicesEndpointPolicy#authorization_policy}
        '''
        result = self._values.get("authorization_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_tls_policy(self) -> typing.Optional[builtins.str]:
        '''A URL referring to a ClientTlsPolicy resource.

        ClientTlsPolicy can be set to specify the authentication for traffic from the proxy to the actual endpoints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#client_tls_policy GoogleNetworkServicesEndpointPolicy#client_tls_policy}
        '''
        result = self._values.get("client_tls_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A free-text description of the resource. Max length 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#description GoogleNetworkServicesEndpointPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#id GoogleNetworkServicesEndpointPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of label tags associated with the TcpRoute resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#labels GoogleNetworkServicesEndpointPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#project GoogleNetworkServicesEndpointPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_tls_policy(self) -> typing.Optional[builtins.str]:
        '''A URL referring to ServerTlsPolicy resource.

        ServerTlsPolicy is used to determine the authentication policy to be applied to terminate the inbound traffic at the identified backends.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#server_tls_policy GoogleNetworkServicesEndpointPolicy#server_tls_policy}
        '''
        result = self._values.get("server_tls_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEndpointPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#timeouts GoogleNetworkServicesEndpointPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetworkServicesEndpointPolicyTimeouts"], result)

    @builtins.property
    def traffic_port_selector(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEndpointPolicyTrafficPortSelector"]:
        '''traffic_port_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#traffic_port_selector GoogleNetworkServicesEndpointPolicy#traffic_port_selector}
        '''
        result = self._values.get("traffic_port_selector")
        return typing.cast(typing.Optional["GoogleNetworkServicesEndpointPolicyTrafficPortSelector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEndpointPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEndpointPolicy.GoogleNetworkServicesEndpointPolicyEndpointMatcher",
    jsii_struct_bases=[],
    name_mapping={"metadata_label_matcher": "metadataLabelMatcher"},
)
class GoogleNetworkServicesEndpointPolicyEndpointMatcher:
    def __init__(
        self,
        *,
        metadata_label_matcher: typing.Union["GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param metadata_label_matcher: metadata_label_matcher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#metadata_label_matcher GoogleNetworkServicesEndpointPolicy#metadata_label_matcher}
        '''
        if isinstance(metadata_label_matcher, dict):
            metadata_label_matcher = GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher(**metadata_label_matcher)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b29ad6931f7dd5ab6e3e92278bfa25e584cd36ebc4e371a8830d4a0117eb1d)
            check_type(argname="argument metadata_label_matcher", value=metadata_label_matcher, expected_type=type_hints["metadata_label_matcher"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metadata_label_matcher": metadata_label_matcher,
        }

    @builtins.property
    def metadata_label_matcher(
        self,
    ) -> "GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher":
        '''metadata_label_matcher block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#metadata_label_matcher GoogleNetworkServicesEndpointPolicy#metadata_label_matcher}
        '''
        result = self._values.get("metadata_label_matcher")
        assert result is not None, "Required property 'metadata_label_matcher' is missing"
        return typing.cast("GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEndpointPolicyEndpointMatcher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEndpointPolicy.GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher",
    jsii_struct_bases=[],
    name_mapping={
        "metadata_label_match_criteria": "metadataLabelMatchCriteria",
        "metadata_labels": "metadataLabels",
    },
)
class GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher:
    def __init__(
        self,
        *,
        metadata_label_match_criteria: builtins.str,
        metadata_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param metadata_label_match_criteria: Specifies how matching should be done. Possible values: ["MATCH_ANY", "MATCH_ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#metadata_label_match_criteria GoogleNetworkServicesEndpointPolicy#metadata_label_match_criteria}
        :param metadata_labels: metadata_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#metadata_labels GoogleNetworkServicesEndpointPolicy#metadata_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44806c545ac26686931d2573c7c6cfbaa84d9c3e807370641917cc7979956dad)
            check_type(argname="argument metadata_label_match_criteria", value=metadata_label_match_criteria, expected_type=type_hints["metadata_label_match_criteria"])
            check_type(argname="argument metadata_labels", value=metadata_labels, expected_type=type_hints["metadata_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metadata_label_match_criteria": metadata_label_match_criteria,
        }
        if metadata_labels is not None:
            self._values["metadata_labels"] = metadata_labels

    @builtins.property
    def metadata_label_match_criteria(self) -> builtins.str:
        '''Specifies how matching should be done. Possible values: ["MATCH_ANY", "MATCH_ALL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#metadata_label_match_criteria GoogleNetworkServicesEndpointPolicy#metadata_label_match_criteria}
        '''
        result = self._values.get("metadata_label_match_criteria")
        assert result is not None, "Required property 'metadata_label_match_criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels"]]]:
        '''metadata_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#metadata_labels GoogleNetworkServicesEndpointPolicy#metadata_labels}
        '''
        result = self._values.get("metadata_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEndpointPolicy.GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels",
    jsii_struct_bases=[],
    name_mapping={"label_name": "labelName", "label_value": "labelValue"},
)
class GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels:
    def __init__(self, *, label_name: builtins.str, label_value: builtins.str) -> None:
        '''
        :param label_name: Required. Label name presented as key in xDS Node Metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#label_name GoogleNetworkServicesEndpointPolicy#label_name}
        :param label_value: Required. Label value presented as value corresponding to the above key, in xDS Node Metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#label_value GoogleNetworkServicesEndpointPolicy#label_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f85ce5a2f6b3c579f0a9ea29420429a592a3f62f0e6734ba6a8cf8f5dd02c1)
            check_type(argname="argument label_name", value=label_name, expected_type=type_hints["label_name"])
            check_type(argname="argument label_value", value=label_value, expected_type=type_hints["label_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label_name": label_name,
            "label_value": label_value,
        }

    @builtins.property
    def label_name(self) -> builtins.str:
        '''Required. Label name presented as key in xDS Node Metadata.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#label_name GoogleNetworkServicesEndpointPolicy#label_name}
        '''
        result = self._values.get("label_name")
        assert result is not None, "Required property 'label_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def label_value(self) -> builtins.str:
        '''Required. Label value presented as value corresponding to the above key, in xDS Node Metadata.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#label_value GoogleNetworkServicesEndpointPolicy#label_value}
        '''
        result = self._values.get("label_value")
        assert result is not None, "Required property 'label_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEndpointPolicy.GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__594a463f92e5e3d66de2afbad950cffa0ff1e61a4b627eeaeb67afd5a6731a58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1181c70723f7a7e300c351267f5673d4a608588240c5f8e5fab3a34dc278cf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef58a4543d51fbd5d8614e6fdee99746f20c6b768a2b5ce8ce586a16c6040d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__491f6579775c26a45fc07559e2c0760ca87ba40ee948ed9e335ccbab46c2a19b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bcbd12a3c78554366e112f3241023109f894a03306ff1505b8c1d1f557123fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab336f2d488d90b794bcb513812eba63a239e1d2a2ef6c5ea603fed9c7de67a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEndpointPolicy.GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbfd4a1d89dec098b0e5276e80d3800e3cdd67b423bf215f8d668823a0cd8261)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="labelNameInput")
    def label_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="labelValueInput")
    def label_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelValueInput"))

    @builtins.property
    @jsii.member(jsii_name="labelName")
    def label_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelName"))

    @label_name.setter
    def label_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea2d0f2c4d273926bf2ef83ba62ac8b79498687a15424930925942e7660496d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labelValue")
    def label_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelValue"))

    @label_value.setter
    def label_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__774e68407bd5e77f8fc226f4eab3e10914b2e185155821bdc83f8583b095af79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6263f00a23b11b972e3750d15934eaa5361a78486d583e791a8f7a511e0e7b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEndpointPolicy.GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f6c91ddd87a1329ab0d3398d25535a80fadac7c822b0bddfa4baaecbcaf08b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetadataLabels")
    def put_metadata_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83c8d1532253b144578e3bf03e5e3049859c8c096a0fa35bcf78743bae4b03a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadataLabels", [value]))

    @jsii.member(jsii_name="resetMetadataLabels")
    def reset_metadata_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataLabels", []))

    @builtins.property
    @jsii.member(jsii_name="metadataLabels")
    def metadata_labels(
        self,
    ) -> GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsList:
        return typing.cast(GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsList, jsii.get(self, "metadataLabels"))

    @builtins.property
    @jsii.member(jsii_name="metadataLabelMatchCriteriaInput")
    def metadata_label_match_criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataLabelMatchCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataLabelsInput")
    def metadata_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]], jsii.get(self, "metadataLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataLabelMatchCriteria")
    def metadata_label_match_criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataLabelMatchCriteria"))

    @metadata_label_match_criteria.setter
    def metadata_label_match_criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a1ea0e5c88b7983a9cf484ece72dd45444818e9b71d17046f7bdb6103c2ddd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataLabelMatchCriteria", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80142d4aa5fbce216d7b606a801a847d16a49fedfd59457d52da67df8dec3997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEndpointPolicyEndpointMatcherOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEndpointPolicy.GoogleNetworkServicesEndpointPolicyEndpointMatcherOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c2e358691d05cf958459970faf8519acfd9dfd74609dc561ae2dde72cc59f60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetadataLabelMatcher")
    def put_metadata_label_matcher(
        self,
        *,
        metadata_label_match_criteria: builtins.str,
        metadata_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param metadata_label_match_criteria: Specifies how matching should be done. Possible values: ["MATCH_ANY", "MATCH_ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#metadata_label_match_criteria GoogleNetworkServicesEndpointPolicy#metadata_label_match_criteria}
        :param metadata_labels: metadata_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#metadata_labels GoogleNetworkServicesEndpointPolicy#metadata_labels}
        '''
        value = GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher(
            metadata_label_match_criteria=metadata_label_match_criteria,
            metadata_labels=metadata_labels,
        )

        return typing.cast(None, jsii.invoke(self, "putMetadataLabelMatcher", [value]))

    @builtins.property
    @jsii.member(jsii_name="metadataLabelMatcher")
    def metadata_label_matcher(
        self,
    ) -> GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherOutputReference:
        return typing.cast(GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherOutputReference, jsii.get(self, "metadataLabelMatcher"))

    @builtins.property
    @jsii.member(jsii_name="metadataLabelMatcherInput")
    def metadata_label_matcher_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher], jsii.get(self, "metadataLabelMatcherInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEndpointPolicyEndpointMatcher]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEndpointPolicyEndpointMatcher], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEndpointPolicyEndpointMatcher],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b51856afd2ed9a3aae73d5467d61a0b1a567fc4c12fb679b06c117a70b5887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEndpointPolicy.GoogleNetworkServicesEndpointPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetworkServicesEndpointPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#create GoogleNetworkServicesEndpointPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#delete GoogleNetworkServicesEndpointPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#update GoogleNetworkServicesEndpointPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6e3fa7ea578b53e70bfb49ba92142a6c639db891941d5bdc3760994c098e87a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#create GoogleNetworkServicesEndpointPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#delete GoogleNetworkServicesEndpointPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#update GoogleNetworkServicesEndpointPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEndpointPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEndpointPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEndpointPolicy.GoogleNetworkServicesEndpointPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d07f28adbe130dd07fe9816b637d3bcb2204bb863ec09ca6e7405cf1a984dfd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57026cf00878ff929ae8fac150c7e01e8f6236044db218f093eaae2f3a2b036f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a74a605ea420923bb36863c400f0fa9b33d412a00bd834641f2a890f39c3a59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be2b8a81c547d4e491be7dcdb8576e9574100d1b361ff3a542502934663c20ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEndpointPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEndpointPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEndpointPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d4e5c3966294ccea7894a0a494ca517ef5483c05771d3d11b50665d57cb7be2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEndpointPolicy.GoogleNetworkServicesEndpointPolicyTrafficPortSelector",
    jsii_struct_bases=[],
    name_mapping={"ports": "ports"},
)
class GoogleNetworkServicesEndpointPolicyTrafficPortSelector:
    def __init__(self, *, ports: typing.Sequence[builtins.str]) -> None:
        '''
        :param ports: List of ports. Can be port numbers or port range (example, [80-90] specifies all ports from 80 to 90, including 80 and 90) or named ports or * to specify all ports. If the list is empty, all ports are selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#ports GoogleNetworkServicesEndpointPolicy#ports}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6623bb4e4b0ca85a4318e22dcebaa6f5720b46b298e92f291f2a511db7fd2f52)
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ports": ports,
        }

    @builtins.property
    def ports(self) -> typing.List[builtins.str]:
        '''List of ports.

        Can be port numbers or port range (example, [80-90] specifies all ports from 80 to 90, including 80 and 90) or named ports or * to specify all ports. If the list is empty, all ports are selected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_endpoint_policy#ports GoogleNetworkServicesEndpointPolicy#ports}
        '''
        result = self._values.get("ports")
        assert result is not None, "Required property 'ports' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEndpointPolicyTrafficPortSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEndpointPolicyTrafficPortSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEndpointPolicy.GoogleNetworkServicesEndpointPolicyTrafficPortSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac95d8f3d6f2805ad66357c4de93e2722c58ed4a1e95a360ea89ee40ddba1d4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d3af7107f86f7f49e54a90aa48bac8492e35a8dd9d0bdda9d46a441cf342c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEndpointPolicyTrafficPortSelector]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEndpointPolicyTrafficPortSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEndpointPolicyTrafficPortSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0bc816be92a7cd5fde68aee742d26acab72d556009893171facadb2010413d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetworkServicesEndpointPolicy",
    "GoogleNetworkServicesEndpointPolicyConfig",
    "GoogleNetworkServicesEndpointPolicyEndpointMatcher",
    "GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher",
    "GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels",
    "GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsList",
    "GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsOutputReference",
    "GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherOutputReference",
    "GoogleNetworkServicesEndpointPolicyEndpointMatcherOutputReference",
    "GoogleNetworkServicesEndpointPolicyTimeouts",
    "GoogleNetworkServicesEndpointPolicyTimeoutsOutputReference",
    "GoogleNetworkServicesEndpointPolicyTrafficPortSelector",
    "GoogleNetworkServicesEndpointPolicyTrafficPortSelectorOutputReference",
]

publication.publish()

def _typecheckingstub__f5a9b58fb0570f11319ffeb8705ae709d72687759b796b43df345fbaf9e6ce3e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    endpoint_matcher: typing.Union[GoogleNetworkServicesEndpointPolicyEndpointMatcher, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    type: builtins.str,
    authorization_policy: typing.Optional[builtins.str] = None,
    client_tls_policy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    server_tls_policy: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkServicesEndpointPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_port_selector: typing.Optional[typing.Union[GoogleNetworkServicesEndpointPolicyTrafficPortSelector, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__92d89a8a1a2ceb8bc96aca17f4b00dea56cd8e9ca00d90deb0e3f137682e4160(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25047e61d4f749a8b550636cc118b6bf01c5b9c26b436d75256adcb7351ccbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34957db1cf11431ece992e5f12c0605362ab8ecc7b179173111fa112054fe59b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6902489867c77342268032aace4f93ab4f4abf10619438513ed9d9780ded718b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc0c18d66dfe4d6a15b314e9a7965b0beaf687edd342498260d58ef475803b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9976fedfff9c3d18f31e17f9953eb080f2d6ba826ccf5e9ce3a9df12452287f4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77289cb350af0a9ca36e6d447277b60e632169caaf6bb1a6bdc8f4b78b70d98b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fa33dc9d1d3cc8680456dd9bbc9691274b44e18ea78eee226b7ac00c226f15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e34a37a59cb072a43226614cfb31020a6496fcb94fd7e333e8216dc8a98ec9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef11e9698f295c30ed7a61f2cb408bb2a5b9324324c4a4afc4b6b223671c76e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c548d37d90633030df3904ef243c7f53db2200b0a58ebef8571a2e52600d9510(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    endpoint_matcher: typing.Union[GoogleNetworkServicesEndpointPolicyEndpointMatcher, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    type: builtins.str,
    authorization_policy: typing.Optional[builtins.str] = None,
    client_tls_policy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    server_tls_policy: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkServicesEndpointPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_port_selector: typing.Optional[typing.Union[GoogleNetworkServicesEndpointPolicyTrafficPortSelector, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b29ad6931f7dd5ab6e3e92278bfa25e584cd36ebc4e371a8830d4a0117eb1d(
    *,
    metadata_label_matcher: typing.Union[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44806c545ac26686931d2573c7c6cfbaa84d9c3e807370641917cc7979956dad(
    *,
    metadata_label_match_criteria: builtins.str,
    metadata_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f85ce5a2f6b3c579f0a9ea29420429a592a3f62f0e6734ba6a8cf8f5dd02c1(
    *,
    label_name: builtins.str,
    label_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594a463f92e5e3d66de2afbad950cffa0ff1e61a4b627eeaeb67afd5a6731a58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1181c70723f7a7e300c351267f5673d4a608588240c5f8e5fab3a34dc278cf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef58a4543d51fbd5d8614e6fdee99746f20c6b768a2b5ce8ce586a16c6040d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491f6579775c26a45fc07559e2c0760ca87ba40ee948ed9e335ccbab46c2a19b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bcbd12a3c78554366e112f3241023109f894a03306ff1505b8c1d1f557123fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab336f2d488d90b794bcb513812eba63a239e1d2a2ef6c5ea603fed9c7de67a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbfd4a1d89dec098b0e5276e80d3800e3cdd67b423bf215f8d668823a0cd8261(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea2d0f2c4d273926bf2ef83ba62ac8b79498687a15424930925942e7660496d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774e68407bd5e77f8fc226f4eab3e10914b2e185155821bdc83f8583b095af79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6263f00a23b11b972e3750d15934eaa5361a78486d583e791a8f7a511e0e7b2d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6c91ddd87a1329ab0d3398d25535a80fadac7c822b0bddfa4baaecbcaf08b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83c8d1532253b144578e3bf03e5e3049859c8c096a0fa35bcf78743bae4b03a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1ea0e5c88b7983a9cf484ece72dd45444818e9b71d17046f7bdb6103c2ddd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80142d4aa5fbce216d7b606a801a847d16a49fedfd59457d52da67df8dec3997(
    value: typing.Optional[GoogleNetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2e358691d05cf958459970faf8519acfd9dfd74609dc561ae2dde72cc59f60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b51856afd2ed9a3aae73d5467d61a0b1a567fc4c12fb679b06c117a70b5887(
    value: typing.Optional[GoogleNetworkServicesEndpointPolicyEndpointMatcher],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e3fa7ea578b53e70bfb49ba92142a6c639db891941d5bdc3760994c098e87a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d07f28adbe130dd07fe9816b637d3bcb2204bb863ec09ca6e7405cf1a984dfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57026cf00878ff929ae8fac150c7e01e8f6236044db218f093eaae2f3a2b036f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a74a605ea420923bb36863c400f0fa9b33d412a00bd834641f2a890f39c3a59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2b8a81c547d4e491be7dcdb8576e9574100d1b361ff3a542502934663c20ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4e5c3966294ccea7894a0a494ca517ef5483c05771d3d11b50665d57cb7be2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEndpointPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6623bb4e4b0ca85a4318e22dcebaa6f5720b46b298e92f291f2a511db7fd2f52(
    *,
    ports: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac95d8f3d6f2805ad66357c4de93e2722c58ed4a1e95a360ea89ee40ddba1d4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d3af7107f86f7f49e54a90aa48bac8492e35a8dd9d0bdda9d46a441cf342c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0bc816be92a7cd5fde68aee742d26acab72d556009893171facadb2010413d(
    value: typing.Optional[GoogleNetworkServicesEndpointPolicyTrafficPortSelector],
) -> None:
    """Type checking stubs"""
    pass
