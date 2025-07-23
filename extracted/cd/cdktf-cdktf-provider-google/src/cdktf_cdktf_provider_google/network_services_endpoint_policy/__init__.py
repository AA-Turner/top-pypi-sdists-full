r'''
# `google_network_services_endpoint_policy`

Refer to the Terraform Registry for docs: [`google_network_services_endpoint_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy).
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


class NetworkServicesEndpointPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEndpointPolicy.NetworkServicesEndpointPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy google_network_services_endpoint_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        endpoint_matcher: typing.Union["NetworkServicesEndpointPolicyEndpointMatcher", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        type: builtins.str,
        authorization_policy: typing.Optional[builtins.str] = None,
        client_tls_policy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        server_tls_policy: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesEndpointPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_port_selector: typing.Optional[typing.Union["NetworkServicesEndpointPolicyTrafficPortSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy google_network_services_endpoint_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param endpoint_matcher: endpoint_matcher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#endpoint_matcher NetworkServicesEndpointPolicy#endpoint_matcher}
        :param name: Name of the EndpointPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#name NetworkServicesEndpointPolicy#name}
        :param type: The type of endpoint policy. This is primarily used to validate the configuration. Possible values: ["SIDECAR_PROXY", "GRPC_SERVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#type NetworkServicesEndpointPolicy#type}
        :param authorization_policy: This field specifies the URL of AuthorizationPolicy resource that applies authorization policies to the inbound traffic at the matched endpoints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#authorization_policy NetworkServicesEndpointPolicy#authorization_policy}
        :param client_tls_policy: A URL referring to a ClientTlsPolicy resource. ClientTlsPolicy can be set to specify the authentication for traffic from the proxy to the actual endpoints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#client_tls_policy NetworkServicesEndpointPolicy#client_tls_policy}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#description NetworkServicesEndpointPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#id NetworkServicesEndpointPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the TcpRoute resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#labels NetworkServicesEndpointPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#project NetworkServicesEndpointPolicy#project}.
        :param server_tls_policy: A URL referring to ServerTlsPolicy resource. ServerTlsPolicy is used to determine the authentication policy to be applied to terminate the inbound traffic at the identified backends. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#server_tls_policy NetworkServicesEndpointPolicy#server_tls_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#timeouts NetworkServicesEndpointPolicy#timeouts}
        :param traffic_port_selector: traffic_port_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#traffic_port_selector NetworkServicesEndpointPolicy#traffic_port_selector}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5286fe8af6a9576105dc5e8a1ee4ae96659ce128185a98222f71200f278883)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkServicesEndpointPolicyConfig(
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
        '''Generates CDKTF code for importing a NetworkServicesEndpointPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkServicesEndpointPolicy to import.
        :param import_from_id: The id of the existing NetworkServicesEndpointPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkServicesEndpointPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab1049d0313de841695cdb9416c917d260d466c54e18d943069964418ebbf70a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEndpointMatcher")
    def put_endpoint_matcher(
        self,
        *,
        metadata_label_matcher: typing.Union["NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param metadata_label_matcher: metadata_label_matcher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#metadata_label_matcher NetworkServicesEndpointPolicy#metadata_label_matcher}
        '''
        value = NetworkServicesEndpointPolicyEndpointMatcher(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#create NetworkServicesEndpointPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#delete NetworkServicesEndpointPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#update NetworkServicesEndpointPolicy#update}.
        '''
        value = NetworkServicesEndpointPolicyTimeouts(
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
        :param ports: List of ports. Can be port numbers or port range (example, [80-90] specifies all ports from 80 to 90, including 80 and 90) or named ports or * to specify all ports. If the list is empty, all ports are selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#ports NetworkServicesEndpointPolicy#ports}
        '''
        value = NetworkServicesEndpointPolicyTrafficPortSelector(ports=ports)

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
    ) -> "NetworkServicesEndpointPolicyEndpointMatcherOutputReference":
        return typing.cast("NetworkServicesEndpointPolicyEndpointMatcherOutputReference", jsii.get(self, "endpointMatcher"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkServicesEndpointPolicyTimeoutsOutputReference":
        return typing.cast("NetworkServicesEndpointPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trafficPortSelector")
    def traffic_port_selector(
        self,
    ) -> "NetworkServicesEndpointPolicyTrafficPortSelectorOutputReference":
        return typing.cast("NetworkServicesEndpointPolicyTrafficPortSelectorOutputReference", jsii.get(self, "trafficPortSelector"))

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
    ) -> typing.Optional["NetworkServicesEndpointPolicyEndpointMatcher"]:
        return typing.cast(typing.Optional["NetworkServicesEndpointPolicyEndpointMatcher"], jsii.get(self, "endpointMatcherInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesEndpointPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesEndpointPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficPortSelectorInput")
    def traffic_port_selector_input(
        self,
    ) -> typing.Optional["NetworkServicesEndpointPolicyTrafficPortSelector"]:
        return typing.cast(typing.Optional["NetworkServicesEndpointPolicyTrafficPortSelector"], jsii.get(self, "trafficPortSelectorInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a28b37e5a1eb0a451f77576b54b157be1bd4bf5b09b112d31377d670b48d3049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTlsPolicy")
    def client_tls_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientTlsPolicy"))

    @client_tls_policy.setter
    def client_tls_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6bfad346b9b8ad63c2558c2c2430fb9b675b9c719e68c99244443d7eb6f4559)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTlsPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8805f3cd894d097b26fb0d6abc3b0e1b7209ffd58a4a783c51d9bfc24cbb8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad03cf48a72170972c08a785391ba6cb4f7e9908b6aa05a9ef6105e204fa916c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b34af6e9f4475d76f74cac0745a79757331bbb0060f394a2d1f6377dbe5043be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__406e0e9ce309300f24ed87316ee276c9f57f802ac0a3de33977665398fe800b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__529fffe3f925677472909968d5a711c7c5b7a184dc765b952252ee42ca161f61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverTlsPolicy")
    def server_tls_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverTlsPolicy"))

    @server_tls_policy.setter
    def server_tls_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42259ef4dae0e79fdc8ffbe3b39be7813c6c86fb0cb9b70244f984251c8d7eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverTlsPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3010c584aa38c9363ace88a224fb1b3db6168fce9b22e9a87892539b277200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEndpointPolicy.NetworkServicesEndpointPolicyConfig",
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
class NetworkServicesEndpointPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        endpoint_matcher: typing.Union["NetworkServicesEndpointPolicyEndpointMatcher", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        type: builtins.str,
        authorization_policy: typing.Optional[builtins.str] = None,
        client_tls_policy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        server_tls_policy: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesEndpointPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_port_selector: typing.Optional[typing.Union["NetworkServicesEndpointPolicyTrafficPortSelector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param endpoint_matcher: endpoint_matcher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#endpoint_matcher NetworkServicesEndpointPolicy#endpoint_matcher}
        :param name: Name of the EndpointPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#name NetworkServicesEndpointPolicy#name}
        :param type: The type of endpoint policy. This is primarily used to validate the configuration. Possible values: ["SIDECAR_PROXY", "GRPC_SERVER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#type NetworkServicesEndpointPolicy#type}
        :param authorization_policy: This field specifies the URL of AuthorizationPolicy resource that applies authorization policies to the inbound traffic at the matched endpoints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#authorization_policy NetworkServicesEndpointPolicy#authorization_policy}
        :param client_tls_policy: A URL referring to a ClientTlsPolicy resource. ClientTlsPolicy can be set to specify the authentication for traffic from the proxy to the actual endpoints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#client_tls_policy NetworkServicesEndpointPolicy#client_tls_policy}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#description NetworkServicesEndpointPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#id NetworkServicesEndpointPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the TcpRoute resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#labels NetworkServicesEndpointPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#project NetworkServicesEndpointPolicy#project}.
        :param server_tls_policy: A URL referring to ServerTlsPolicy resource. ServerTlsPolicy is used to determine the authentication policy to be applied to terminate the inbound traffic at the identified backends. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#server_tls_policy NetworkServicesEndpointPolicy#server_tls_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#timeouts NetworkServicesEndpointPolicy#timeouts}
        :param traffic_port_selector: traffic_port_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#traffic_port_selector NetworkServicesEndpointPolicy#traffic_port_selector}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(endpoint_matcher, dict):
            endpoint_matcher = NetworkServicesEndpointPolicyEndpointMatcher(**endpoint_matcher)
        if isinstance(timeouts, dict):
            timeouts = NetworkServicesEndpointPolicyTimeouts(**timeouts)
        if isinstance(traffic_port_selector, dict):
            traffic_port_selector = NetworkServicesEndpointPolicyTrafficPortSelector(**traffic_port_selector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417d7525e69ba77a618c0421d1150e7ee2b526fb82c31cdaca193b3cd0cc58cc)
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
    def endpoint_matcher(self) -> "NetworkServicesEndpointPolicyEndpointMatcher":
        '''endpoint_matcher block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#endpoint_matcher NetworkServicesEndpointPolicy#endpoint_matcher}
        '''
        result = self._values.get("endpoint_matcher")
        assert result is not None, "Required property 'endpoint_matcher' is missing"
        return typing.cast("NetworkServicesEndpointPolicyEndpointMatcher", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the EndpointPolicy resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#name NetworkServicesEndpointPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of endpoint policy. This is primarily used to validate the configuration. Possible values: ["SIDECAR_PROXY", "GRPC_SERVER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#type NetworkServicesEndpointPolicy#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_policy(self) -> typing.Optional[builtins.str]:
        '''This field specifies the URL of AuthorizationPolicy resource that applies authorization policies to the inbound traffic at the matched endpoints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#authorization_policy NetworkServicesEndpointPolicy#authorization_policy}
        '''
        result = self._values.get("authorization_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_tls_policy(self) -> typing.Optional[builtins.str]:
        '''A URL referring to a ClientTlsPolicy resource.

        ClientTlsPolicy can be set to specify the authentication for traffic from the proxy to the actual endpoints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#client_tls_policy NetworkServicesEndpointPolicy#client_tls_policy}
        '''
        result = self._values.get("client_tls_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A free-text description of the resource. Max length 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#description NetworkServicesEndpointPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#id NetworkServicesEndpointPolicy#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#labels NetworkServicesEndpointPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#project NetworkServicesEndpointPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_tls_policy(self) -> typing.Optional[builtins.str]:
        '''A URL referring to ServerTlsPolicy resource.

        ServerTlsPolicy is used to determine the authentication policy to be applied to terminate the inbound traffic at the identified backends.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#server_tls_policy NetworkServicesEndpointPolicy#server_tls_policy}
        '''
        result = self._values.get("server_tls_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkServicesEndpointPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#timeouts NetworkServicesEndpointPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkServicesEndpointPolicyTimeouts"], result)

    @builtins.property
    def traffic_port_selector(
        self,
    ) -> typing.Optional["NetworkServicesEndpointPolicyTrafficPortSelector"]:
        '''traffic_port_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#traffic_port_selector NetworkServicesEndpointPolicy#traffic_port_selector}
        '''
        result = self._values.get("traffic_port_selector")
        return typing.cast(typing.Optional["NetworkServicesEndpointPolicyTrafficPortSelector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEndpointPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEndpointPolicy.NetworkServicesEndpointPolicyEndpointMatcher",
    jsii_struct_bases=[],
    name_mapping={"metadata_label_matcher": "metadataLabelMatcher"},
)
class NetworkServicesEndpointPolicyEndpointMatcher:
    def __init__(
        self,
        *,
        metadata_label_matcher: typing.Union["NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param metadata_label_matcher: metadata_label_matcher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#metadata_label_matcher NetworkServicesEndpointPolicy#metadata_label_matcher}
        '''
        if isinstance(metadata_label_matcher, dict):
            metadata_label_matcher = NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher(**metadata_label_matcher)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76bf9c21942b125f6f7193880675ff846b1e48b97618527721ae67ffbddabfdf)
            check_type(argname="argument metadata_label_matcher", value=metadata_label_matcher, expected_type=type_hints["metadata_label_matcher"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metadata_label_matcher": metadata_label_matcher,
        }

    @builtins.property
    def metadata_label_matcher(
        self,
    ) -> "NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher":
        '''metadata_label_matcher block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#metadata_label_matcher NetworkServicesEndpointPolicy#metadata_label_matcher}
        '''
        result = self._values.get("metadata_label_matcher")
        assert result is not None, "Required property 'metadata_label_matcher' is missing"
        return typing.cast("NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEndpointPolicyEndpointMatcher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEndpointPolicy.NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher",
    jsii_struct_bases=[],
    name_mapping={
        "metadata_label_match_criteria": "metadataLabelMatchCriteria",
        "metadata_labels": "metadataLabels",
    },
)
class NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher:
    def __init__(
        self,
        *,
        metadata_label_match_criteria: builtins.str,
        metadata_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param metadata_label_match_criteria: Specifies how matching should be done. Possible values: ["MATCH_ANY", "MATCH_ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#metadata_label_match_criteria NetworkServicesEndpointPolicy#metadata_label_match_criteria}
        :param metadata_labels: metadata_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#metadata_labels NetworkServicesEndpointPolicy#metadata_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0390c9b441003e3a25ce24b8a90912ec91b1a602e3f7a515261e6020f255f5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#metadata_label_match_criteria NetworkServicesEndpointPolicy#metadata_label_match_criteria}
        '''
        result = self._values.get("metadata_label_match_criteria")
        assert result is not None, "Required property 'metadata_label_match_criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels"]]]:
        '''metadata_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#metadata_labels NetworkServicesEndpointPolicy#metadata_labels}
        '''
        result = self._values.get("metadata_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEndpointPolicy.NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels",
    jsii_struct_bases=[],
    name_mapping={"label_name": "labelName", "label_value": "labelValue"},
)
class NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels:
    def __init__(self, *, label_name: builtins.str, label_value: builtins.str) -> None:
        '''
        :param label_name: Required. Label name presented as key in xDS Node Metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#label_name NetworkServicesEndpointPolicy#label_name}
        :param label_value: Required. Label value presented as value corresponding to the above key, in xDS Node Metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#label_value NetworkServicesEndpointPolicy#label_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08a1c42e67006bc2b75c9464f51eecca1007b444aa663da6cc5aa10de8652cb)
            check_type(argname="argument label_name", value=label_name, expected_type=type_hints["label_name"])
            check_type(argname="argument label_value", value=label_value, expected_type=type_hints["label_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label_name": label_name,
            "label_value": label_value,
        }

    @builtins.property
    def label_name(self) -> builtins.str:
        '''Required. Label name presented as key in xDS Node Metadata.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#label_name NetworkServicesEndpointPolicy#label_name}
        '''
        result = self._values.get("label_name")
        assert result is not None, "Required property 'label_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def label_value(self) -> builtins.str:
        '''Required. Label value presented as value corresponding to the above key, in xDS Node Metadata.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#label_value NetworkServicesEndpointPolicy#label_value}
        '''
        result = self._values.get("label_value")
        assert result is not None, "Required property 'label_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEndpointPolicy.NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ffdb705034e7043fe2812f067a7ae6300290c5871b2e33d3c7c4e4a8bcdff39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56bc99ee2e3268a4fd103fa585b79ab9fa93cd0ba1eb290e7c63086f12b386ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec4fc61c525cd4d38be94ae2c4471a81209f46247d1563d8db387b3a9435a262)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ea167f8ab22ae01fdb077165f84f1bc873474e2fa8e19d0857244417b0ed435)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85690a901f7cd0c65dc8356d5b329776c0e099c2f9b7f39d78fc8a491165501b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33ed7b69d42d48b12666496e1ae43ade711dc1a210bdd4d8efe6fd165d12526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEndpointPolicy.NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47a28ca93decae34bdf23ad0bc77ade00e965d2c63f5358b640880c9d19ef79a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e968f21647e039401d394b7da658e2777c1df3820305a368f6f96653d7eff6d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labelValue")
    def label_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelValue"))

    @label_value.setter
    def label_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16322ef953486bed0b2a32d1a726f453642a79b1c5c0e9280de5495c364d6c53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05798e10452c386901e2806abb40625e8c265e80fbebcfdc995f1a1cfa77b404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEndpointPolicy.NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b91bd606e763c106b56376c2498018c3eafc7efa3de26099bd393b89a86af338)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetadataLabels")
    def put_metadata_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff25ebf69074840b78b6ebee5c6f586632521c731fe32d49a27d377ae02f1bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadataLabels", [value]))

    @jsii.member(jsii_name="resetMetadataLabels")
    def reset_metadata_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataLabels", []))

    @builtins.property
    @jsii.member(jsii_name="metadataLabels")
    def metadata_labels(
        self,
    ) -> NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsList:
        return typing.cast(NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsList, jsii.get(self, "metadataLabels"))

    @builtins.property
    @jsii.member(jsii_name="metadataLabelMatchCriteriaInput")
    def metadata_label_match_criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataLabelMatchCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataLabelsInput")
    def metadata_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]], jsii.get(self, "metadataLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataLabelMatchCriteria")
    def metadata_label_match_criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataLabelMatchCriteria"))

    @metadata_label_match_criteria.setter
    def metadata_label_match_criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af9a7d4f04d3f13cb4ae85b869580c411792344f0691ab0a143419cf1144d390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataLabelMatchCriteria", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher]:
        return typing.cast(typing.Optional[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae3cd5493f210652d384c76856de6668431668b7f1e98ddac68f41a63194e92c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEndpointPolicyEndpointMatcherOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEndpointPolicy.NetworkServicesEndpointPolicyEndpointMatcherOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__230cca51630160ae9ad3bc181f1dd6d48bcf19351d90d6fb658cd85c5363d895)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetadataLabelMatcher")
    def put_metadata_label_matcher(
        self,
        *,
        metadata_label_match_criteria: builtins.str,
        metadata_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param metadata_label_match_criteria: Specifies how matching should be done. Possible values: ["MATCH_ANY", "MATCH_ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#metadata_label_match_criteria NetworkServicesEndpointPolicy#metadata_label_match_criteria}
        :param metadata_labels: metadata_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#metadata_labels NetworkServicesEndpointPolicy#metadata_labels}
        '''
        value = NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher(
            metadata_label_match_criteria=metadata_label_match_criteria,
            metadata_labels=metadata_labels,
        )

        return typing.cast(None, jsii.invoke(self, "putMetadataLabelMatcher", [value]))

    @builtins.property
    @jsii.member(jsii_name="metadataLabelMatcher")
    def metadata_label_matcher(
        self,
    ) -> NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherOutputReference:
        return typing.cast(NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherOutputReference, jsii.get(self, "metadataLabelMatcher"))

    @builtins.property
    @jsii.member(jsii_name="metadataLabelMatcherInput")
    def metadata_label_matcher_input(
        self,
    ) -> typing.Optional[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher]:
        return typing.cast(typing.Optional[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher], jsii.get(self, "metadataLabelMatcherInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEndpointPolicyEndpointMatcher]:
        return typing.cast(typing.Optional[NetworkServicesEndpointPolicyEndpointMatcher], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEndpointPolicyEndpointMatcher],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb71c59013c7fa01794067dc5453c579eb25adc25fb22d85ad9b7e7299c31f43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEndpointPolicy.NetworkServicesEndpointPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkServicesEndpointPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#create NetworkServicesEndpointPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#delete NetworkServicesEndpointPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#update NetworkServicesEndpointPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032abac7dd2059b1e2580414f84c32bd99bdc039632943ab7111cbe5c235ac59)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#create NetworkServicesEndpointPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#delete NetworkServicesEndpointPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#update NetworkServicesEndpointPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEndpointPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEndpointPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEndpointPolicy.NetworkServicesEndpointPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dddf56e6adb4c0c35243bd56db42e851ff24432d34ec211290c517db3fad3eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29ac11f54e50f4c6ab2cff48c744710c65f0e97f156f13832b7a6519a87a1663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f206810a5185f5c85b630eca06b06c5b5ec2c19229ab92a87a4a27029e9ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b25275dcccee6ffa86c4e48ec14e5acbc625ce34f49ee1bb10d59046b327b26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEndpointPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEndpointPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEndpointPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2673a4e14b015048c5e63f9b61f3a30b97c87f8c556c4b23852629533e2353bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEndpointPolicy.NetworkServicesEndpointPolicyTrafficPortSelector",
    jsii_struct_bases=[],
    name_mapping={"ports": "ports"},
)
class NetworkServicesEndpointPolicyTrafficPortSelector:
    def __init__(self, *, ports: typing.Sequence[builtins.str]) -> None:
        '''
        :param ports: List of ports. Can be port numbers or port range (example, [80-90] specifies all ports from 80 to 90, including 80 and 90) or named ports or * to specify all ports. If the list is empty, all ports are selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#ports NetworkServicesEndpointPolicy#ports}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7fe37cebcb82994413abf4a450b6f24a337ac1716d3986c7ab823d9a5d49c5)
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ports": ports,
        }

    @builtins.property
    def ports(self) -> typing.List[builtins.str]:
        '''List of ports.

        Can be port numbers or port range (example, [80-90] specifies all ports from 80 to 90, including 80 and 90) or named ports or * to specify all ports. If the list is empty, all ports are selected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_endpoint_policy#ports NetworkServicesEndpointPolicy#ports}
        '''
        result = self._values.get("ports")
        assert result is not None, "Required property 'ports' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEndpointPolicyTrafficPortSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEndpointPolicyTrafficPortSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEndpointPolicy.NetworkServicesEndpointPolicyTrafficPortSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6215f91dce2c75b7652e0634e96af79cfc851761725c9a13ec55a26c81c40683)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c70692fce27b63b3a82cbfe4880904259dd56089f44d710cec15ee457fcc29c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEndpointPolicyTrafficPortSelector]:
        return typing.cast(typing.Optional[NetworkServicesEndpointPolicyTrafficPortSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEndpointPolicyTrafficPortSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__988fda5fb061bc4e9feff2558854e3fca63105d0af0f876e52fd63c5b50e729a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkServicesEndpointPolicy",
    "NetworkServicesEndpointPolicyConfig",
    "NetworkServicesEndpointPolicyEndpointMatcher",
    "NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher",
    "NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels",
    "NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsList",
    "NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabelsOutputReference",
    "NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherOutputReference",
    "NetworkServicesEndpointPolicyEndpointMatcherOutputReference",
    "NetworkServicesEndpointPolicyTimeouts",
    "NetworkServicesEndpointPolicyTimeoutsOutputReference",
    "NetworkServicesEndpointPolicyTrafficPortSelector",
    "NetworkServicesEndpointPolicyTrafficPortSelectorOutputReference",
]

publication.publish()

def _typecheckingstub__9d5286fe8af6a9576105dc5e8a1ee4ae96659ce128185a98222f71200f278883(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    endpoint_matcher: typing.Union[NetworkServicesEndpointPolicyEndpointMatcher, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    type: builtins.str,
    authorization_policy: typing.Optional[builtins.str] = None,
    client_tls_policy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    server_tls_policy: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesEndpointPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_port_selector: typing.Optional[typing.Union[NetworkServicesEndpointPolicyTrafficPortSelector, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ab1049d0313de841695cdb9416c917d260d466c54e18d943069964418ebbf70a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a28b37e5a1eb0a451f77576b54b157be1bd4bf5b09b112d31377d670b48d3049(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6bfad346b9b8ad63c2558c2c2430fb9b675b9c719e68c99244443d7eb6f4559(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8805f3cd894d097b26fb0d6abc3b0e1b7209ffd58a4a783c51d9bfc24cbb8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad03cf48a72170972c08a785391ba6cb4f7e9908b6aa05a9ef6105e204fa916c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34af6e9f4475d76f74cac0745a79757331bbb0060f394a2d1f6377dbe5043be(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__406e0e9ce309300f24ed87316ee276c9f57f802ac0a3de33977665398fe800b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529fffe3f925677472909968d5a711c7c5b7a184dc765b952252ee42ca161f61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42259ef4dae0e79fdc8ffbe3b39be7813c6c86fb0cb9b70244f984251c8d7eea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3010c584aa38c9363ace88a224fb1b3db6168fce9b22e9a87892539b277200(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417d7525e69ba77a618c0421d1150e7ee2b526fb82c31cdaca193b3cd0cc58cc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    endpoint_matcher: typing.Union[NetworkServicesEndpointPolicyEndpointMatcher, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    type: builtins.str,
    authorization_policy: typing.Optional[builtins.str] = None,
    client_tls_policy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    server_tls_policy: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesEndpointPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_port_selector: typing.Optional[typing.Union[NetworkServicesEndpointPolicyTrafficPortSelector, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76bf9c21942b125f6f7193880675ff846b1e48b97618527721ae67ffbddabfdf(
    *,
    metadata_label_matcher: typing.Union[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0390c9b441003e3a25ce24b8a90912ec91b1a602e3f7a515261e6020f255f5(
    *,
    metadata_label_match_criteria: builtins.str,
    metadata_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08a1c42e67006bc2b75c9464f51eecca1007b444aa663da6cc5aa10de8652cb(
    *,
    label_name: builtins.str,
    label_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ffdb705034e7043fe2812f067a7ae6300290c5871b2e33d3c7c4e4a8bcdff39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56bc99ee2e3268a4fd103fa585b79ab9fa93cd0ba1eb290e7c63086f12b386ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4fc61c525cd4d38be94ae2c4471a81209f46247d1563d8db387b3a9435a262(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea167f8ab22ae01fdb077165f84f1bc873474e2fa8e19d0857244417b0ed435(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85690a901f7cd0c65dc8356d5b329776c0e099c2f9b7f39d78fc8a491165501b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33ed7b69d42d48b12666496e1ae43ade711dc1a210bdd4d8efe6fd165d12526(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a28ca93decae34bdf23ad0bc77ade00e965d2c63f5358b640880c9d19ef79a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e968f21647e039401d394b7da658e2777c1df3820305a368f6f96653d7eff6d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16322ef953486bed0b2a32d1a726f453642a79b1c5c0e9280de5495c364d6c53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05798e10452c386901e2806abb40625e8c265e80fbebcfdc995f1a1cfa77b404(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91bd606e763c106b56376c2498018c3eafc7efa3de26099bd393b89a86af338(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff25ebf69074840b78b6ebee5c6f586632521c731fe32d49a27d377ae02f1bf0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcherMetadataLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9a7d4f04d3f13cb4ae85b869580c411792344f0691ab0a143419cf1144d390(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3cd5493f210652d384c76856de6668431668b7f1e98ddac68f41a63194e92c(
    value: typing.Optional[NetworkServicesEndpointPolicyEndpointMatcherMetadataLabelMatcher],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230cca51630160ae9ad3bc181f1dd6d48bcf19351d90d6fb658cd85c5363d895(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb71c59013c7fa01794067dc5453c579eb25adc25fb22d85ad9b7e7299c31f43(
    value: typing.Optional[NetworkServicesEndpointPolicyEndpointMatcher],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032abac7dd2059b1e2580414f84c32bd99bdc039632943ab7111cbe5c235ac59(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dddf56e6adb4c0c35243bd56db42e851ff24432d34ec211290c517db3fad3eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ac11f54e50f4c6ab2cff48c744710c65f0e97f156f13832b7a6519a87a1663(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f206810a5185f5c85b630eca06b06c5b5ec2c19229ab92a87a4a27029e9ce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b25275dcccee6ffa86c4e48ec14e5acbc625ce34f49ee1bb10d59046b327b26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2673a4e14b015048c5e63f9b61f3a30b97c87f8c556c4b23852629533e2353bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEndpointPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7fe37cebcb82994413abf4a450b6f24a337ac1716d3986c7ab823d9a5d49c5(
    *,
    ports: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6215f91dce2c75b7652e0634e96af79cfc851761725c9a13ec55a26c81c40683(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70692fce27b63b3a82cbfe4880904259dd56089f44d710cec15ee457fcc29c0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988fda5fb061bc4e9feff2558854e3fca63105d0af0f876e52fd63c5b50e729a(
    value: typing.Optional[NetworkServicesEndpointPolicyTrafficPortSelector],
) -> None:
    """Type checking stubs"""
    pass
