r'''
# `google_network_services_edge_cache_service`

Refer to the Terraform Registry for docs: [`google_network_services_edge_cache_service`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service).
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


class NetworkServicesEdgeCacheService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service google_network_services_edge_cache_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        routing: typing.Union["NetworkServicesEdgeCacheServiceRouting", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        disable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_quic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        edge_security_policy: typing.Optional[builtins.str] = None,
        edge_ssl_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_config: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        require_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service google_network_services_edge_cache_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#name NetworkServicesEdgeCacheService#name}
        :param routing: routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#routing NetworkServicesEdgeCacheService#routing}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#description NetworkServicesEdgeCacheService#description}
        :param disable_http2: Disables HTTP/2. HTTP/2 (h2) is enabled by default and recommended for performance. HTTP/2 improves connection re-use and reduces connection setup overhead by sending multiple streams over the same connection. Some legacy HTTP clients may have issues with HTTP/2 connections due to broken HTTP/2 implementations. Setting this to true will prevent HTTP/2 from being advertised and negotiated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#disable_http2 NetworkServicesEdgeCacheService#disable_http2}
        :param disable_quic: HTTP/3 (IETF QUIC) and Google QUIC are enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#disable_quic NetworkServicesEdgeCacheService#disable_quic}
        :param edge_security_policy: Resource URL that points at the Cloud Armor edge security policy that is applied on each request against the EdgeCacheService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#edge_security_policy NetworkServicesEdgeCacheService#edge_security_policy}
        :param edge_ssl_certificates: URLs to sslCertificate resources that are used to authenticate connections between users and the EdgeCacheService. Note that only "global" certificates with a "scope" of "EDGE_CACHE" can be attached to an EdgeCacheService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#edge_ssl_certificates NetworkServicesEdgeCacheService#edge_ssl_certificates}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#id NetworkServicesEdgeCacheService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the EdgeCache resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#labels NetworkServicesEdgeCacheService#labels}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#log_config NetworkServicesEdgeCacheService#log_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#project NetworkServicesEdgeCacheService#project}.
        :param require_tls: Require TLS (HTTPS) for all clients connecting to this service. Clients who connect over HTTP (port 80) will receive a HTTP 301 to the same URL over HTTPS (port 443). You must have at least one (1) edgeSslCertificate specified to enable this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#require_tls NetworkServicesEdgeCacheService#require_tls}
        :param ssl_policy: URL of the SslPolicy resource that will be associated with the EdgeCacheService. If not set, the EdgeCacheService has no SSL policy configured, and will default to the "COMPATIBLE" policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#ssl_policy NetworkServicesEdgeCacheService#ssl_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#timeouts NetworkServicesEdgeCacheService#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c189ce9f2f0edc8557df9fa311275589f2f85e6da60f36319b147ea830e81d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkServicesEdgeCacheServiceConfig(
            name=name,
            routing=routing,
            description=description,
            disable_http2=disable_http2,
            disable_quic=disable_quic,
            edge_security_policy=edge_security_policy,
            edge_ssl_certificates=edge_ssl_certificates,
            id=id,
            labels=labels,
            log_config=log_config,
            project=project,
            require_tls=require_tls,
            ssl_policy=ssl_policy,
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
        '''Generates CDKTF code for importing a NetworkServicesEdgeCacheService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkServicesEdgeCacheService to import.
        :param import_from_id: The id of the existing NetworkServicesEdgeCacheService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkServicesEdgeCacheService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f0543362cf0da1418bf7e335365741313092838d0980df1fd202bc741a272a8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLogConfig")
    def put_log_config(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sample_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable: Specifies whether to enable logging for traffic served by this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#enable NetworkServicesEdgeCacheService#enable}
        :param sample_rate: Configures the sampling rate of requests, where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0, and the value of the field must be in [0, 1]. This field can only be specified if logging is enabled for this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#sample_rate NetworkServicesEdgeCacheService#sample_rate}
        '''
        value = NetworkServicesEdgeCacheServiceLogConfig(
            enable=enable, sample_rate=sample_rate
        )

        return typing.cast(None, jsii.invoke(self, "putLogConfig", [value]))

    @jsii.member(jsii_name="putRouting")
    def put_routing(
        self,
        *,
        host_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingHostRule", typing.Dict[builtins.str, typing.Any]]]],
        path_matcher: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcher", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param host_rule: host_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#host_rule NetworkServicesEdgeCacheService#host_rule}
        :param path_matcher: path_matcher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_matcher NetworkServicesEdgeCacheService#path_matcher}
        '''
        value = NetworkServicesEdgeCacheServiceRouting(
            host_rule=host_rule, path_matcher=path_matcher
        )

        return typing.cast(None, jsii.invoke(self, "putRouting", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#create NetworkServicesEdgeCacheService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#delete NetworkServicesEdgeCacheService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#update NetworkServicesEdgeCacheService#update}.
        '''
        value = NetworkServicesEdgeCacheServiceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisableHttp2")
    def reset_disable_http2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableHttp2", []))

    @jsii.member(jsii_name="resetDisableQuic")
    def reset_disable_quic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableQuic", []))

    @jsii.member(jsii_name="resetEdgeSecurityPolicy")
    def reset_edge_security_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeSecurityPolicy", []))

    @jsii.member(jsii_name="resetEdgeSslCertificates")
    def reset_edge_ssl_certificates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeSslCertificates", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLogConfig")
    def reset_log_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRequireTls")
    def reset_require_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireTls", []))

    @jsii.member(jsii_name="resetSslPolicy")
    def reset_ssl_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslPolicy", []))

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
    @jsii.member(jsii_name="ipv4Addresses")
    def ipv4_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipv4Addresses"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Addresses")
    def ipv6_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipv6Addresses"))

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(self) -> "NetworkServicesEdgeCacheServiceLogConfigOutputReference":
        return typing.cast("NetworkServicesEdgeCacheServiceLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="routing")
    def routing(self) -> "NetworkServicesEdgeCacheServiceRoutingOutputReference":
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingOutputReference", jsii.get(self, "routing"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkServicesEdgeCacheServiceTimeoutsOutputReference":
        return typing.cast("NetworkServicesEdgeCacheServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableHttp2Input")
    def disable_http2_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableHttp2Input"))

    @builtins.property
    @jsii.member(jsii_name="disableQuicInput")
    def disable_quic_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableQuicInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeSecurityPolicyInput")
    def edge_security_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeSecurityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeSslCertificatesInput")
    def edge_ssl_certificates_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "edgeSslCertificatesInput"))

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
    @jsii.member(jsii_name="logConfigInput")
    def log_config_input(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceLogConfig"]:
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceLogConfig"], jsii.get(self, "logConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="requireTlsInput")
    def require_tls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireTlsInput"))

    @builtins.property
    @jsii.member(jsii_name="routingInput")
    def routing_input(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRouting"]:
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRouting"], jsii.get(self, "routingInput"))

    @builtins.property
    @jsii.member(jsii_name="sslPolicyInput")
    def ssl_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesEdgeCacheServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesEdgeCacheServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5237a4cd503468b2efaf9f972f8c127ee8df9aa809d7fd7dc59ef9a341dfd5c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableHttp2")
    def disable_http2(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableHttp2"))

    @disable_http2.setter
    def disable_http2(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba254a32d9b6de9b38ebfccc58bc781d21e73916cec9da1e77fc201f09625d1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableHttp2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableQuic")
    def disable_quic(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableQuic"))

    @disable_quic.setter
    def disable_quic(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__023beb1a3ab192b7116ff0dac46fd7df2156d8309cb9f2e93f8fcf57ba24b2f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableQuic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeSecurityPolicy")
    def edge_security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeSecurityPolicy"))

    @edge_security_policy.setter
    def edge_security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fffcab658cfac0b7ffc23826649a3c7cc14487c8595f2f163d4b301321e3cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeSecurityPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeSslCertificates")
    def edge_ssl_certificates(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "edgeSslCertificates"))

    @edge_ssl_certificates.setter
    def edge_ssl_certificates(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__561b16f03147a6ca98de48312767475cb07e83a0d53ca85b8851766c4944ac07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeSslCertificates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e1b2577a2bf25ba54293bcb7bb2774ef56a47b5cbbb97e64b9ac648edc8548c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__344f2211bf2bb2da43910a4d9449580e0f647251f3a5a76ea0841cc2c8bd6e6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__413ac45f174a414dbdab18e7da7923ea7727dad86851caf91a942c550804f690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28ced80e8b06c6f05ed11cc0147e95f299a956ee23dc6c968714fb9f5e3df3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireTls")
    def require_tls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireTls"))

    @require_tls.setter
    def require_tls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__726fd79fbcbaa387f427cb90512b61b33f26bbd13c6b4fbb2ff393917b051724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireTls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslPolicy")
    def ssl_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslPolicy"))

    @ssl_policy.setter
    def ssl_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6caaef78ffa3bc830d92f958f2db8c7a4ce2b89a58735ae408ba2a117820a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslPolicy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "routing": "routing",
        "description": "description",
        "disable_http2": "disableHttp2",
        "disable_quic": "disableQuic",
        "edge_security_policy": "edgeSecurityPolicy",
        "edge_ssl_certificates": "edgeSslCertificates",
        "id": "id",
        "labels": "labels",
        "log_config": "logConfig",
        "project": "project",
        "require_tls": "requireTls",
        "ssl_policy": "sslPolicy",
        "timeouts": "timeouts",
    },
)
class NetworkServicesEdgeCacheServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        routing: typing.Union["NetworkServicesEdgeCacheServiceRouting", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        disable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_quic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        edge_security_policy: typing.Optional[builtins.str] = None,
        edge_ssl_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_config: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        require_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#name NetworkServicesEdgeCacheService#name}
        :param routing: routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#routing NetworkServicesEdgeCacheService#routing}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#description NetworkServicesEdgeCacheService#description}
        :param disable_http2: Disables HTTP/2. HTTP/2 (h2) is enabled by default and recommended for performance. HTTP/2 improves connection re-use and reduces connection setup overhead by sending multiple streams over the same connection. Some legacy HTTP clients may have issues with HTTP/2 connections due to broken HTTP/2 implementations. Setting this to true will prevent HTTP/2 from being advertised and negotiated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#disable_http2 NetworkServicesEdgeCacheService#disable_http2}
        :param disable_quic: HTTP/3 (IETF QUIC) and Google QUIC are enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#disable_quic NetworkServicesEdgeCacheService#disable_quic}
        :param edge_security_policy: Resource URL that points at the Cloud Armor edge security policy that is applied on each request against the EdgeCacheService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#edge_security_policy NetworkServicesEdgeCacheService#edge_security_policy}
        :param edge_ssl_certificates: URLs to sslCertificate resources that are used to authenticate connections between users and the EdgeCacheService. Note that only "global" certificates with a "scope" of "EDGE_CACHE" can be attached to an EdgeCacheService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#edge_ssl_certificates NetworkServicesEdgeCacheService#edge_ssl_certificates}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#id NetworkServicesEdgeCacheService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the EdgeCache resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#labels NetworkServicesEdgeCacheService#labels}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#log_config NetworkServicesEdgeCacheService#log_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#project NetworkServicesEdgeCacheService#project}.
        :param require_tls: Require TLS (HTTPS) for all clients connecting to this service. Clients who connect over HTTP (port 80) will receive a HTTP 301 to the same URL over HTTPS (port 443). You must have at least one (1) edgeSslCertificate specified to enable this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#require_tls NetworkServicesEdgeCacheService#require_tls}
        :param ssl_policy: URL of the SslPolicy resource that will be associated with the EdgeCacheService. If not set, the EdgeCacheService has no SSL policy configured, and will default to the "COMPATIBLE" policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#ssl_policy NetworkServicesEdgeCacheService#ssl_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#timeouts NetworkServicesEdgeCacheService#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(routing, dict):
            routing = NetworkServicesEdgeCacheServiceRouting(**routing)
        if isinstance(log_config, dict):
            log_config = NetworkServicesEdgeCacheServiceLogConfig(**log_config)
        if isinstance(timeouts, dict):
            timeouts = NetworkServicesEdgeCacheServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23c824d6b2fc0cc291b63f5cf85727d33edeabc5a1c053f6fe7c4d2141ca616)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument routing", value=routing, expected_type=type_hints["routing"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_http2", value=disable_http2, expected_type=type_hints["disable_http2"])
            check_type(argname="argument disable_quic", value=disable_quic, expected_type=type_hints["disable_quic"])
            check_type(argname="argument edge_security_policy", value=edge_security_policy, expected_type=type_hints["edge_security_policy"])
            check_type(argname="argument edge_ssl_certificates", value=edge_ssl_certificates, expected_type=type_hints["edge_ssl_certificates"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument require_tls", value=require_tls, expected_type=type_hints["require_tls"])
            check_type(argname="argument ssl_policy", value=ssl_policy, expected_type=type_hints["ssl_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "routing": routing,
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
        if disable_http2 is not None:
            self._values["disable_http2"] = disable_http2
        if disable_quic is not None:
            self._values["disable_quic"] = disable_quic
        if edge_security_policy is not None:
            self._values["edge_security_policy"] = edge_security_policy
        if edge_ssl_certificates is not None:
            self._values["edge_ssl_certificates"] = edge_ssl_certificates
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if log_config is not None:
            self._values["log_config"] = log_config
        if project is not None:
            self._values["project"] = project
        if require_tls is not None:
            self._values["require_tls"] = require_tls
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy
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
    def name(self) -> builtins.str:
        '''Name of the resource;

        provided by the client when the resource is created.
        The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
        and all following characters must be a dash, underscore, letter or digit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#name NetworkServicesEdgeCacheService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routing(self) -> "NetworkServicesEdgeCacheServiceRouting":
        '''routing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#routing NetworkServicesEdgeCacheService#routing}
        '''
        result = self._values.get("routing")
        assert result is not None, "Required property 'routing' is missing"
        return typing.cast("NetworkServicesEdgeCacheServiceRouting", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#description NetworkServicesEdgeCacheService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_http2(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables HTTP/2.

        HTTP/2 (h2) is enabled by default and recommended for performance. HTTP/2 improves connection re-use and reduces connection setup overhead by sending multiple streams over the same connection.

        Some legacy HTTP clients may have issues with HTTP/2 connections due to broken HTTP/2 implementations. Setting this to true will prevent HTTP/2 from being advertised and negotiated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#disable_http2 NetworkServicesEdgeCacheService#disable_http2}
        '''
        result = self._values.get("disable_http2")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_quic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''HTTP/3 (IETF QUIC) and Google QUIC are enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#disable_quic NetworkServicesEdgeCacheService#disable_quic}
        '''
        result = self._values.get("disable_quic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def edge_security_policy(self) -> typing.Optional[builtins.str]:
        '''Resource URL that points at the Cloud Armor edge security policy that is applied on each request against the EdgeCacheService.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#edge_security_policy NetworkServicesEdgeCacheService#edge_security_policy}
        '''
        result = self._values.get("edge_security_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_ssl_certificates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URLs to sslCertificate resources that are used to authenticate connections between users and the EdgeCacheService.

        Note that only "global" certificates with a "scope" of "EDGE_CACHE" can be attached to an EdgeCacheService.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#edge_ssl_certificates NetworkServicesEdgeCacheService#edge_ssl_certificates}
        '''
        result = self._values.get("edge_ssl_certificates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#id NetworkServicesEdgeCacheService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of label tags associated with the EdgeCache resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#labels NetworkServicesEdgeCacheService#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def log_config(self) -> typing.Optional["NetworkServicesEdgeCacheServiceLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#log_config NetworkServicesEdgeCacheService#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceLogConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#project NetworkServicesEdgeCacheService#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require TLS (HTTPS) for all clients connecting to this service.

        Clients who connect over HTTP (port 80) will receive a HTTP 301 to the same URL over HTTPS (port 443).
        You must have at least one (1) edgeSslCertificate specified to enable this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#require_tls NetworkServicesEdgeCacheService#require_tls}
        '''
        result = self._values.get("require_tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_policy(self) -> typing.Optional[builtins.str]:
        '''URL of the SslPolicy resource that will be associated with the EdgeCacheService.

        If not set, the EdgeCacheService has no SSL policy configured, and will default to the "COMPATIBLE" policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#ssl_policy NetworkServicesEdgeCacheService#ssl_policy}
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkServicesEdgeCacheServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#timeouts NetworkServicesEdgeCacheService#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceLogConfig",
    jsii_struct_bases=[],
    name_mapping={"enable": "enable", "sample_rate": "sampleRate"},
)
class NetworkServicesEdgeCacheServiceLogConfig:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sample_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable: Specifies whether to enable logging for traffic served by this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#enable NetworkServicesEdgeCacheService#enable}
        :param sample_rate: Configures the sampling rate of requests, where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0, and the value of the field must be in [0, 1]. This field can only be specified if logging is enabled for this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#sample_rate NetworkServicesEdgeCacheService#sample_rate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24bf96c419c7a1aaa097e44cb87ed443ece20868a763d5a0a69409de387c0186)
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument sample_rate", value=sample_rate, expected_type=type_hints["sample_rate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable is not None:
            self._values["enable"] = enable
        if sample_rate is not None:
            self._values["sample_rate"] = sample_rate

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to enable logging for traffic served by this service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#enable NetworkServicesEdgeCacheService#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sample_rate(self) -> typing.Optional[jsii.Number]:
        '''Configures the sampling rate of requests, where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0, and the value of the field must be in [0, 1].

        This field can only be specified if logging is enabled for this service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#sample_rate NetworkServicesEdgeCacheService#sample_rate}
        '''
        result = self._values.get("sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe48a9465b864fe8b8b9c107acb35c0edfa4dbd2c470f06454d2c825703b4b36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnable")
    def reset_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnable", []))

    @jsii.member(jsii_name="resetSampleRate")
    def reset_sample_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleRate", []))

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleRateInput")
    def sample_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sampleRateInput"))

    @builtins.property
    @jsii.member(jsii_name="enable")
    def enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enable"))

    @enable.setter
    def enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0bc94c6b40bee41240453372594f946a03a91fe762937601d891d9e08c56f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRate")
    def sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRate"))

    @sample_rate.setter
    def sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9003533898c3b3f95c03ed3f8d2c16905677e07f081891dbedc6ad158892d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceLogConfig]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheServiceLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6fbedd7e394a13bbfdf52149cc103b1175b9200ff627565d60894f788a4b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRouting",
    jsii_struct_bases=[],
    name_mapping={"host_rule": "hostRule", "path_matcher": "pathMatcher"},
)
class NetworkServicesEdgeCacheServiceRouting:
    def __init__(
        self,
        *,
        host_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingHostRule", typing.Dict[builtins.str, typing.Any]]]],
        path_matcher: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcher", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param host_rule: host_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#host_rule NetworkServicesEdgeCacheService#host_rule}
        :param path_matcher: path_matcher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_matcher NetworkServicesEdgeCacheService#path_matcher}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99302cd2b69b5c4b19d2bb86974718dce24810545d19f5b7b1f47da3df2b4bb2)
            check_type(argname="argument host_rule", value=host_rule, expected_type=type_hints["host_rule"])
            check_type(argname="argument path_matcher", value=path_matcher, expected_type=type_hints["path_matcher"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_rule": host_rule,
            "path_matcher": path_matcher,
        }

    @builtins.property
    def host_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingHostRule"]]:
        '''host_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#host_rule NetworkServicesEdgeCacheService#host_rule}
        '''
        result = self._values.get("host_rule")
        assert result is not None, "Required property 'host_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingHostRule"]], result)

    @builtins.property
    def path_matcher(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcher"]]:
        '''path_matcher block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_matcher NetworkServicesEdgeCacheService#path_matcher}
        '''
        result = self._values.get("path_matcher")
        assert result is not None, "Required property 'path_matcher' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcher"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingHostRule",
    jsii_struct_bases=[],
    name_mapping={
        "hosts": "hosts",
        "path_matcher": "pathMatcher",
        "description": "description",
    },
)
class NetworkServicesEdgeCacheServiceRoutingHostRule:
    def __init__(
        self,
        *,
        hosts: typing.Sequence[builtins.str],
        path_matcher: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hosts: The list of host patterns to match. Host patterns must be valid hostnames. Ports are not allowed. Wildcard hosts are supported in the suffix or prefix form. * matches any string of ([a-z0-9-.]*). It does not match the empty string. When multiple hosts are specified, hosts are matched in the following priority: 1. Exact domain names: ''www.foo.com''. 2. Suffix domain wildcards: ''*.foo.com'' or ''*-bar.foo.com''. 3. Prefix domain wildcards: ''foo.*'' or ''foo-*''. 4. Special wildcard ''*'' matching any domain. Notes:: The wildcard will not match the empty string. e.g. ''*-bar.foo.com'' will match ''baz-bar.foo.com'' but not ''-bar.foo.com''. The longest wildcards match first. Only a single host in the entire service can match on ''*''. A domain must be unique across all configured hosts within a service. Hosts are matched against the HTTP Host header, or for HTTP/2 and HTTP/3, the ":authority" header, from the incoming request. You may specify up to 10 hosts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#hosts NetworkServicesEdgeCacheService#hosts}
        :param path_matcher: The name of the pathMatcher associated with this hostRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_matcher NetworkServicesEdgeCacheService#path_matcher}
        :param description: A human-readable description of the hostRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#description NetworkServicesEdgeCacheService#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb772e4b0e3dc48ab8398a1f20b9067583a83d7e624bb0267617a3d115b139a)
            check_type(argname="argument hosts", value=hosts, expected_type=type_hints["hosts"])
            check_type(argname="argument path_matcher", value=path_matcher, expected_type=type_hints["path_matcher"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hosts": hosts,
            "path_matcher": path_matcher,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def hosts(self) -> typing.List[builtins.str]:
        '''The list of host patterns to match.

        Host patterns must be valid hostnames. Ports are not allowed. Wildcard hosts are supported in the suffix or prefix form. * matches any string of ([a-z0-9-.]*). It does not match the empty string.

        When multiple hosts are specified, hosts are matched in the following priority:

        1. Exact domain names: ''www.foo.com''.
        2. Suffix domain wildcards: ''*.foo.com'' or ''*-bar.foo.com''.
        3. Prefix domain wildcards: ''foo.*'' or ''foo-*''.
        4. Special wildcard ''*'' matching any domain.

        Notes::

           The wildcard will not match the empty string. e.g. ''*-bar.foo.com'' will match ''baz-bar.foo.com'' but not ''-bar.foo.com''. The longest wildcards match first. Only a single host in the entire service can match on ''*''. A domain must be unique across all configured hosts within a service.

           Hosts are matched against the HTTP Host header, or for HTTP/2 and HTTP/3, the ":authority" header, from the incoming request.

           You may specify up to 10 hosts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#hosts NetworkServicesEdgeCacheService#hosts}
        '''
        result = self._values.get("hosts")
        assert result is not None, "Required property 'hosts' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def path_matcher(self) -> builtins.str:
        '''The name of the pathMatcher associated with this hostRule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_matcher NetworkServicesEdgeCacheService#path_matcher}
        '''
        result = self._values.get("path_matcher")
        assert result is not None, "Required property 'path_matcher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the hostRule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#description NetworkServicesEdgeCacheService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingHostRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingHostRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingHostRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f30fd8452cf25e0479d4b9405e19d354a5a85535603cfa4091c3569d8b4e7746)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesEdgeCacheServiceRoutingHostRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08504028ffc3d42338552313f918cb0f70be395dcc57d3050cf46a3903b5d9a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingHostRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea9b488e0c33099c57f1f6081a7c60869080ad25441d6d3b7501e3111fb38d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c38ab4c63dd6a4036c7b12a8a76e1fe5d3aeecd38b3fdca81a4fe9f9a7a613e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92c8e1c6c7f1cb75b2e70d539c117878a53004724bcf170e2b9093406e7a8d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingHostRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingHostRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingHostRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daff4507db37c0ab1e9cec4de25ebfc7ea39cb9e59c775ff235d7b75af1e8a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingHostRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingHostRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e30bcc6e3a994d7ce342d49090809af1d9008b3ac5634c6aa5e5000f0d9910ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="hostsInput")
    def hosts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathMatcherInput")
    def path_matcher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathMatcherInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e7170132d67a5ecebc5100b3e7c397ccbfa8d2ee8bcf851392f026aae8f3f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hosts")
    def hosts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hosts"))

    @hosts.setter
    def hosts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca7429e4bce302bb6540b92d62a6b68f3f78f7bc3ddbf64e949763adf7af1c97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hosts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathMatcher")
    def path_matcher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathMatcher"))

    @path_matcher.setter
    def path_matcher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed96b080a67927aefeae2b371afea91bc963e20fc2a085d493db243909f0e84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathMatcher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingHostRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingHostRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingHostRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0fd75ad3bc2a13609fe8c8a25c51c0da8afb180a2d448f22ed4ca889b25af4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__918eedc821b777af34ff39cf0503061381a925af1049cb8c5fd90e090488e1bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHostRule")
    def put_host_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingHostRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00620d5a10148bcdd4a7a8b55a162be7d9cba72ad26c2ca6b9760b2c28df933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHostRule", [value]))

    @jsii.member(jsii_name="putPathMatcher")
    def put_path_matcher(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcher", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d0d3f33625fa80513874d18f5a13743f09be3f7ec381f9231ae150c3319efe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPathMatcher", [value]))

    @builtins.property
    @jsii.member(jsii_name="hostRule")
    def host_rule(self) -> NetworkServicesEdgeCacheServiceRoutingHostRuleList:
        return typing.cast(NetworkServicesEdgeCacheServiceRoutingHostRuleList, jsii.get(self, "hostRule"))

    @builtins.property
    @jsii.member(jsii_name="pathMatcher")
    def path_matcher(self) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherList":
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherList", jsii.get(self, "pathMatcher"))

    @builtins.property
    @jsii.member(jsii_name="hostRuleInput")
    def host_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingHostRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingHostRule]]], jsii.get(self, "hostRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="pathMatcherInput")
    def path_matcher_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcher"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcher"]]], jsii.get(self, "pathMatcherInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetworkServicesEdgeCacheServiceRouting]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRouting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheServiceRouting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87218fb13ef40f678085331c7abc0a627cef52d585f6824f2a93a22273b91185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcher",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "route_rule": "routeRule",
        "description": "description",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcher:
    def __init__(
        self,
        *,
        name: builtins.str,
        route_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name to which this PathMatcher is referred by the HostRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#name NetworkServicesEdgeCacheService#name}
        :param route_rule: route_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#route_rule NetworkServicesEdgeCacheService#route_rule}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#description NetworkServicesEdgeCacheService#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6cb0f753c4ca807820f3b9433e845e39a8921ef0b7f75377ab568ab3b94cb3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument route_rule", value=route_rule, expected_type=type_hints["route_rule"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "route_rule": route_rule,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        '''The name to which this PathMatcher is referred by the HostRule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#name NetworkServicesEdgeCacheService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def route_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule"]]:
        '''route_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#route_rule NetworkServicesEdgeCacheService#route_rule}
        '''
        result = self._values.get("route_rule")
        assert result is not None, "Required property 'route_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#description NetworkServicesEdgeCacheService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__517c9484327a765f87b19289ddc983ed2f250b62239101fc6f39c03f08ba7d35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e045f2a4598196d9cc896c119a724a32e18602da47ef2c822d10ca088bd36263)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e5e0f5fa893e24b00b6865938a3de257d07d1a1045faa6c5176b78291a3f048)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0d2f45d32e019d711959aa3a8efb951466ec660885b33c3b6da6f364e2d5231)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c7171b1a46b38a8c57a64881491960a0f11b5a731053b91e947cf10b96b3926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcher]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcher]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcher]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5974a3f6f03ce7d3cb0178ba63f11885f4ec90133feb882070685457b58b3031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingPathMatcherOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79c8203c1e3cbc7dbdd2a38a21c668bd44c6658573f218a1b4577c16accdbf24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRouteRule")
    def put_route_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e28fda8c3477d39559f59a4175a6c399e904aa835512e8309bd57c9f9d91b16d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRouteRule", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="routeRule")
    def route_rule(
        self,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleList":
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleList", jsii.get(self, "routeRule"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="routeRuleInput")
    def route_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule"]]], jsii.get(self, "routeRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__917026d5ff718141511c11fb32fc536ada7399fbbd9dacd170747fac9e1b2433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ef776287c8f3e39d5b73b53b562657f408387958f99065cb854fc53f563089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcher]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcher]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcher]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c7d592b542040e1613c123c94b7639ab60b1d3fd4bed4c1795cf2d9197b26e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule",
    jsii_struct_bases=[],
    name_mapping={
        "match_rule": "matchRule",
        "priority": "priority",
        "description": "description",
        "header_action": "headerAction",
        "origin": "origin",
        "route_action": "routeAction",
        "route_methods": "routeMethods",
        "url_redirect": "urlRedirect",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule:
    def __init__(
        self,
        *,
        match_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule", typing.Dict[builtins.str, typing.Any]]]],
        priority: builtins.str,
        description: typing.Optional[builtins.str] = None,
        header_action: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction", typing.Dict[builtins.str, typing.Any]]] = None,
        origin: typing.Optional[builtins.str] = None,
        route_action: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction", typing.Dict[builtins.str, typing.Any]]] = None,
        route_methods: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods", typing.Dict[builtins.str, typing.Any]]] = None,
        url_redirect: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param match_rule: match_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#match_rule NetworkServicesEdgeCacheService#match_rule}
        :param priority: The priority of this route rule, where 1 is the highest priority. You cannot configure two or more routeRules with the same priority. Priority for each rule must be set to a number between 1 and 999 inclusive. Priority numbers can have gaps, which enable you to add or remove rules in the future without affecting the rest of the rules. For example, 1, 2, 3, 4, 5, 9, 12, 16 is a valid series of priority numbers to which you could add rules numbered from 6 to 8, 10 to 11, and 13 to 15 in the future without any impact on existing rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#priority NetworkServicesEdgeCacheService#priority}
        :param description: A human-readable description of the routeRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#description NetworkServicesEdgeCacheService#description}
        :param header_action: header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_action NetworkServicesEdgeCacheService#header_action}
        :param origin: The Origin resource that requests to this route should fetch from when a matching response is not in cache. Origins can be defined as short names ("my-origin") or fully-qualified resource URLs - e.g. "networkservices.googleapis.com/projects/my-project/global/edgecacheorigins/my-origin" Only one of origin or urlRedirect can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#origin NetworkServicesEdgeCacheService#origin}
        :param route_action: route_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#route_action NetworkServicesEdgeCacheService#route_action}
        :param route_methods: route_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#route_methods NetworkServicesEdgeCacheService#route_methods}
        :param url_redirect: url_redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#url_redirect NetworkServicesEdgeCacheService#url_redirect}
        '''
        if isinstance(header_action, dict):
            header_action = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction(**header_action)
        if isinstance(route_action, dict):
            route_action = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction(**route_action)
        if isinstance(route_methods, dict):
            route_methods = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods(**route_methods)
        if isinstance(url_redirect, dict):
            url_redirect = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect(**url_redirect)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8af122e01125ab832afd1dbb02d367da3450fb20680c135ef4e64158c598804)
            check_type(argname="argument match_rule", value=match_rule, expected_type=type_hints["match_rule"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument header_action", value=header_action, expected_type=type_hints["header_action"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument route_action", value=route_action, expected_type=type_hints["route_action"])
            check_type(argname="argument route_methods", value=route_methods, expected_type=type_hints["route_methods"])
            check_type(argname="argument url_redirect", value=url_redirect, expected_type=type_hints["url_redirect"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_rule": match_rule,
            "priority": priority,
        }
        if description is not None:
            self._values["description"] = description
        if header_action is not None:
            self._values["header_action"] = header_action
        if origin is not None:
            self._values["origin"] = origin
        if route_action is not None:
            self._values["route_action"] = route_action
        if route_methods is not None:
            self._values["route_methods"] = route_methods
        if url_redirect is not None:
            self._values["url_redirect"] = url_redirect

    @builtins.property
    def match_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule"]]:
        '''match_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#match_rule NetworkServicesEdgeCacheService#match_rule}
        '''
        result = self._values.get("match_rule")
        assert result is not None, "Required property 'match_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule"]], result)

    @builtins.property
    def priority(self) -> builtins.str:
        '''The priority of this route rule, where 1 is the highest priority.

        You cannot configure two or more routeRules with the same priority. Priority for each rule must be set to a number between 1 and 999 inclusive.

        Priority numbers can have gaps, which enable you to add or remove rules in the future without affecting the rest of the rules. For example, 1, 2, 3, 4, 5, 9, 12, 16 is a valid series of priority numbers
        to which you could add rules numbered from 6 to 8, 10 to 11, and 13 to 15 in the future without any impact on existing rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#priority NetworkServicesEdgeCacheService#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the routeRule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#description NetworkServicesEdgeCacheService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_action(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction"]:
        '''header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_action NetworkServicesEdgeCacheService#header_action}
        '''
        result = self._values.get("header_action")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction"], result)

    @builtins.property
    def origin(self) -> typing.Optional[builtins.str]:
        '''The Origin resource that requests to this route should fetch from when a matching response is not in cache.

        Origins can be defined as short names ("my-origin") or fully-qualified resource URLs - e.g. "networkservices.googleapis.com/projects/my-project/global/edgecacheorigins/my-origin"

        Only one of origin or urlRedirect can be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#origin NetworkServicesEdgeCacheService#origin}
        '''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_action(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction"]:
        '''route_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#route_action NetworkServicesEdgeCacheService#route_action}
        '''
        result = self._values.get("route_action")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction"], result)

    @builtins.property
    def route_methods(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods"]:
        '''route_methods block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#route_methods NetworkServicesEdgeCacheService#route_methods}
        '''
        result = self._values.get("route_methods")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods"], result)

    @builtins.property
    def url_redirect(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect"]:
        '''url_redirect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#url_redirect NetworkServicesEdgeCacheService#url_redirect}
        '''
        result = self._values.get("url_redirect")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction",
    jsii_struct_bases=[],
    name_mapping={
        "request_header_to_add": "requestHeaderToAdd",
        "request_header_to_remove": "requestHeaderToRemove",
        "response_header_to_add": "responseHeaderToAdd",
        "response_header_to_remove": "responseHeaderToRemove",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction:
    def __init__(
        self,
        *,
        request_header_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header_to_remove: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove", typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_header_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd", typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_header_to_remove: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_header_to_add: request_header_to_add block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#request_header_to_add NetworkServicesEdgeCacheService#request_header_to_add}
        :param request_header_to_remove: request_header_to_remove block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#request_header_to_remove NetworkServicesEdgeCacheService#request_header_to_remove}
        :param response_header_to_add: response_header_to_add block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#response_header_to_add NetworkServicesEdgeCacheService#response_header_to_add}
        :param response_header_to_remove: response_header_to_remove block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#response_header_to_remove NetworkServicesEdgeCacheService#response_header_to_remove}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f637391c08bf429fdfc24bc064db9f4fb9b3bb4f581bd3c7a09d36f316e87d5)
            check_type(argname="argument request_header_to_add", value=request_header_to_add, expected_type=type_hints["request_header_to_add"])
            check_type(argname="argument request_header_to_remove", value=request_header_to_remove, expected_type=type_hints["request_header_to_remove"])
            check_type(argname="argument response_header_to_add", value=response_header_to_add, expected_type=type_hints["response_header_to_add"])
            check_type(argname="argument response_header_to_remove", value=response_header_to_remove, expected_type=type_hints["response_header_to_remove"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if request_header_to_add is not None:
            self._values["request_header_to_add"] = request_header_to_add
        if request_header_to_remove is not None:
            self._values["request_header_to_remove"] = request_header_to_remove
        if response_header_to_add is not None:
            self._values["response_header_to_add"] = response_header_to_add
        if response_header_to_remove is not None:
            self._values["response_header_to_remove"] = response_header_to_remove

    @builtins.property
    def request_header_to_add(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd"]]]:
        '''request_header_to_add block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#request_header_to_add NetworkServicesEdgeCacheService#request_header_to_add}
        '''
        result = self._values.get("request_header_to_add")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd"]]], result)

    @builtins.property
    def request_header_to_remove(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove"]]]:
        '''request_header_to_remove block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#request_header_to_remove NetworkServicesEdgeCacheService#request_header_to_remove}
        '''
        result = self._values.get("request_header_to_remove")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove"]]], result)

    @builtins.property
    def response_header_to_add(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd"]]]:
        '''response_header_to_add block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#response_header_to_add NetworkServicesEdgeCacheService#response_header_to_add}
        '''
        result = self._values.get("response_header_to_add")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd"]]], result)

    @builtins.property
    def response_header_to_remove(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove"]]]:
        '''response_header_to_remove block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#response_header_to_remove NetworkServicesEdgeCacheService#response_header_to_remove}
        '''
        result = self._values.get("response_header_to_remove")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99c96cae6de6c1330040b8a02933456d5bffa00e94915e114e9a6281af24e308)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestHeaderToAdd")
    def put_request_header_to_add(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f924f03ab07956fce69fd4e09e885215fe276236f74c74103f269fcd30c3506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeaderToAdd", [value]))

    @jsii.member(jsii_name="putRequestHeaderToRemove")
    def put_request_header_to_remove(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e5b123842356c17d308c0965a305029bb6d1a5405b5499ddfe4bf081f4bf8d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeaderToRemove", [value]))

    @jsii.member(jsii_name="putResponseHeaderToAdd")
    def put_response_header_to_add(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceab87f56ed76ce8dc6dd8f6dec8a8dd09938aa61dc37b318a7a96fc3802ea18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResponseHeaderToAdd", [value]))

    @jsii.member(jsii_name="putResponseHeaderToRemove")
    def put_response_header_to_remove(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ebd5720021cc377a54ba0ed8587f3d5a09632dc13444471c568d2268bbd1f02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResponseHeaderToRemove", [value]))

    @jsii.member(jsii_name="resetRequestHeaderToAdd")
    def reset_request_header_to_add(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeaderToAdd", []))

    @jsii.member(jsii_name="resetRequestHeaderToRemove")
    def reset_request_header_to_remove(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeaderToRemove", []))

    @jsii.member(jsii_name="resetResponseHeaderToAdd")
    def reset_response_header_to_add(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseHeaderToAdd", []))

    @jsii.member(jsii_name="resetResponseHeaderToRemove")
    def reset_response_header_to_remove(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseHeaderToRemove", []))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderToAdd")
    def request_header_to_add(
        self,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddList":
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddList", jsii.get(self, "requestHeaderToAdd"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderToRemove")
    def request_header_to_remove(
        self,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveList":
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveList", jsii.get(self, "requestHeaderToRemove"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderToAdd")
    def response_header_to_add(
        self,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddList":
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddList", jsii.get(self, "responseHeaderToAdd"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderToRemove")
    def response_header_to_remove(
        self,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveList":
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveList", jsii.get(self, "responseHeaderToRemove"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderToAddInput")
    def request_header_to_add_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd"]]], jsii.get(self, "requestHeaderToAddInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderToRemoveInput")
    def request_header_to_remove_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove"]]], jsii.get(self, "requestHeaderToRemoveInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderToAddInput")
    def response_header_to_add_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd"]]], jsii.get(self, "responseHeaderToAddInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderToRemoveInput")
    def response_header_to_remove_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove"]]], jsii.get(self, "responseHeaderToRemoveInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48044d073518fb41d86e18ca91ae45e745230876fbc588542c597735882c7258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd",
    jsii_struct_bases=[],
    name_mapping={
        "header_name": "headerName",
        "header_value": "headerValue",
        "replace": "replace",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        header_value: builtins.str,
        replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param header_name: The name of the header to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_name NetworkServicesEdgeCacheService#header_name}
        :param header_value: The value of the header to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_value NetworkServicesEdgeCacheService#header_value}
        :param replace: Whether to replace all existing headers with the same name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#replace NetworkServicesEdgeCacheService#replace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a5087c3afeca67a550086289add98e04216a8d68bc295a8530f7226bc6d0e2)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument header_value", value=header_value, expected_type=type_hints["header_value"])
            check_type(argname="argument replace", value=replace, expected_type=type_hints["replace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
            "header_value": header_value,
        }
        if replace is not None:
            self._values["replace"] = replace

    @builtins.property
    def header_name(self) -> builtins.str:
        '''The name of the header to add.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_name NetworkServicesEdgeCacheService#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_value(self) -> builtins.str:
        '''The value of the header to add.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_value NetworkServicesEdgeCacheService#header_value}
        '''
        result = self._values.get("header_value")
        assert result is not None, "Required property 'header_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to replace all existing headers with the same name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#replace NetworkServicesEdgeCacheService#replace}
        '''
        result = self._values.get("replace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d6e08027b2d4504d76892e2e0215a7cdb7ca8f87ab27467220d67dccdb66cbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a763d12e4ff031866f28f1714efd83d8e2ea068534de6e4b9a4d38e67c4e9c57)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd0e8fe589a5fe4cab9aaf7b3f315bbb89d3e521765ab48b80db7b8ac005c20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14ce188e5107f9e2e8049716c465bbb27054b20fa810435dc008dbbd0ff99d6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35090e3884f21106b7b8025652f4122f2224ba04c49bc092655549abc9b0381e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300c1d28d9e6d68966475112c0d1555a1620504ab0fed20828c3c1f6ad1c1e98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b74e8639faead4c6044091c86c340b5976a3aa517d1e251d4418ce7f81be43e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetReplace")
    def reset_replace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplace", []))

    @builtins.property
    @jsii.member(jsii_name="headerNameInput")
    def header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="headerValueInput")
    def header_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerValueInput"))

    @builtins.property
    @jsii.member(jsii_name="replaceInput")
    def replace_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "replaceInput"))

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e219295554c22ae72ff3a41a840d8c91c7a61e90b83b3e60a0ee974c9f520da8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405711b9c5046eaff1aed4a37fa96e66df0d5bd3f2d7f770f0632f0a0d46ff38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replace")
    def replace(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "replace"))

    @replace.setter
    def replace(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3fa2449ca7e806adb35a8e79f89e2e696bf7fc54c3fbdab3c5a9de0b80a4659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb67704211244ab352abfc271f3577b94b2fea1a34fefe6d0c20da4d02835efd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName"},
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove:
    def __init__(self, *, header_name: builtins.str) -> None:
        '''
        :param header_name: The name of the header to remove. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_name NetworkServicesEdgeCacheService#header_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17f72559031c443cc5718f51d310e5a51485fcbc40362e618c01550136bca3e)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
        }

    @builtins.property
    def header_name(self) -> builtins.str:
        '''The name of the header to remove.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_name NetworkServicesEdgeCacheService#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44d1c78ced6a35a43be762826ca75eee4ab115307b3a2b02fd0dd490035ff7a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61808d18afe2e7e1e37ebb88dbdb3f3a779be7fe54a0b0debb7c83b5f44af8c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9334a3725b6d7a2d9fd0facd0e29a4b0d3b049cda008295124eb33c1fef324)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82dab592af6ee65808b4c1c1e74bc70a750bd4a5dc3610c035de122f2aceb430)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eb3289622cad770ee6e41592bb38e30461c1337e075741feb34633752532b4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b123b3def0b0c6fc9bb90464511b1405f574e885be8fdaf584cfa4ec3633ffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9728f4e095403a4cc53fd51a8c9d55f2712da3e02d0e0daef661065961ecb823)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="headerNameInput")
    def header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddefdf8be13009d5f6a60c41384a5e2913290ce7b8312bd295edbedf9427f919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb09fa8f59aa9413cbef5ff54b9f464ca96d86e26ba007f09c959fd543a8f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd",
    jsii_struct_bases=[],
    name_mapping={
        "header_name": "headerName",
        "header_value": "headerValue",
        "replace": "replace",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        header_value: builtins.str,
        replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param header_name: The name of the header to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_name NetworkServicesEdgeCacheService#header_name}
        :param header_value: The value of the header to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_value NetworkServicesEdgeCacheService#header_value}
        :param replace: Whether to replace all existing headers with the same name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#replace NetworkServicesEdgeCacheService#replace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b143df35b98a8e3622dd89bcc6b066981bbe5f751a030f9e84e075a3ee725de)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument header_value", value=header_value, expected_type=type_hints["header_value"])
            check_type(argname="argument replace", value=replace, expected_type=type_hints["replace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
            "header_value": header_value,
        }
        if replace is not None:
            self._values["replace"] = replace

    @builtins.property
    def header_name(self) -> builtins.str:
        '''The name of the header to add.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_name NetworkServicesEdgeCacheService#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_value(self) -> builtins.str:
        '''The value of the header to add.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_value NetworkServicesEdgeCacheService#header_value}
        '''
        result = self._values.get("header_value")
        assert result is not None, "Required property 'header_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to replace all existing headers with the same name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#replace NetworkServicesEdgeCacheService#replace}
        '''
        result = self._values.get("replace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6306525ca5605ee3518ab74019925dd2df7a662e3f8b703a3a050889c66c1173)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aaf2f32eb05bbd6cf934bac2d8e91c35c473333b7f503011455f9a717fa326e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bca4d05fce52e862db29dbdf40cfd6103da16c26d1d12abd64dabf63a0901544)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40cf2e9dae902375904f6944dca79da5ecda140e56fc20967aaaa6cb36c91b10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29086fc5d28b8001d5d2d4288892d326f8fab9e4b17eb8c7e6a1a524418f48b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f168b0b0a9b11839c6509bb3585530685b0413a30d699b3d9e63544df29687c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf15a00300822f14b29860ce581b02f2983881c86c7a30e448730629bd6e59d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetReplace")
    def reset_replace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplace", []))

    @builtins.property
    @jsii.member(jsii_name="headerNameInput")
    def header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="headerValueInput")
    def header_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerValueInput"))

    @builtins.property
    @jsii.member(jsii_name="replaceInput")
    def replace_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "replaceInput"))

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963e7014330980fe3952756ea4e5db0f52c36bf0b17e3dc47909f57d45630035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599373d63bff6fd23ebb5ea9d7462eeb22780727a7b69ebe77c7c75d25c8fd4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replace")
    def replace(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "replace"))

    @replace.setter
    def replace(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6a28536ff48f999cb583cb78c357c4d593b820f8ab1b04f7d4201abd079c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26d176d30d74fe13954379e3f33b1843b551c779db9a1d60d3ad2060255c35d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName"},
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove:
    def __init__(self, *, header_name: builtins.str) -> None:
        '''
        :param header_name: Headers to remove from the response prior to sending it back to the client. Response headers are only sent to the client, and do not have an effect on the cache serving the response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_name NetworkServicesEdgeCacheService#header_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee0dc305d54c969ada4dc762399ee404307dc35f20eef380674c96cd5faab0d)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
        }

    @builtins.property
    def header_name(self) -> builtins.str:
        '''Headers to remove from the response prior to sending it back to the client.

        Response headers are only sent to the client, and do not have an effect on the cache serving the response.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_name NetworkServicesEdgeCacheService#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7737999c05a23161fb22e6713ed1ca34c05d79b4c0890b396c4951808b70e3b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15443eae981309556d27416b63842ddfe45d37d43f620ec0bdb1c69eef5dfed1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad5debca30ff31f7cc3203511ee02db4b8dddeee0d3c5fc177600daed92b73f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7983d0ee872cf90c69a53bef3b3d90f4131b375625ddac9e5ee0327bff7fafcd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba3012081a3dc3f5d2319ad6f494ccd437c2df95f1d376ff2e38c2dd41084707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeb8067a6e5b370033c5323711128fdee683c9a6baf611ba68d77cb816e13a21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7877c85c26c8cf9e60e48c1d2619bd7295913cba924427e93aeca415720b902)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="headerNameInput")
    def header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d070283ea9074ffea87ed9e0f885e70137bd76974b693e3302a6ee2cdf71588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7dca1d0cde0d4637df7e974bcada2dee08b7802e2922b883caa741d278e5ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc898715ed8e0f0af8ea342040c06be9e1d988e801c119621a0aa71265b6e37a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8264533b95d5dfd08f40c1c7bcd58bfea6dc464b426bca383048612c8fc8b84f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7026162ba1d97935f371a0bcae1168dec4b20c0ed216bf3460964ac7ada7d10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2b8545dbe6e5bd8e186769023b5c7a43b440e03b31a4ec67592bdd44f56b7f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dd7e9a45f21caeae679bf310910802622e1e6b1888eecce40a33eb04f3a9b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e387aeba87c6680bc789b8e6b9f3dfecd7c3710ec34cf34e6f471b81fd722012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule",
    jsii_struct_bases=[],
    name_mapping={
        "full_path_match": "fullPathMatch",
        "header_match": "headerMatch",
        "ignore_case": "ignoreCase",
        "path_template_match": "pathTemplateMatch",
        "prefix_match": "prefixMatch",
        "query_parameter_match": "queryParameterMatch",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule:
    def __init__(
        self,
        *,
        full_path_match: typing.Optional[builtins.str] = None,
        header_match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path_template_match: typing.Optional[builtins.str] = None,
        prefix_match: typing.Optional[builtins.str] = None,
        query_parameter_match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param full_path_match: For satisfying the matchRule condition, the path of the request must exactly match the value specified in fullPathMatch after removing any query parameters and anchor that may be part of the original URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#full_path_match NetworkServicesEdgeCacheService#full_path_match}
        :param header_match: header_match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_match NetworkServicesEdgeCacheService#header_match}
        :param ignore_case: Specifies that prefixMatch and fullPathMatch matches are case sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#ignore_case NetworkServicesEdgeCacheService#ignore_case}
        :param path_template_match: For satisfying the matchRule condition, the path of the request must match the wildcard pattern specified in pathTemplateMatch after removing any query parameters and anchor that may be part of the original URL. pathTemplateMatch must be between 1 and 255 characters (inclusive). The pattern specified by pathTemplateMatch may have at most 5 wildcard operators and at most 5 variable captures in total. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_template_match NetworkServicesEdgeCacheService#path_template_match}
        :param prefix_match: For satisfying the matchRule condition, the request's path must begin with the specified prefixMatch. prefixMatch must begin with a /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#prefix_match NetworkServicesEdgeCacheService#prefix_match}
        :param query_parameter_match: query_parameter_match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#query_parameter_match NetworkServicesEdgeCacheService#query_parameter_match}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18878045e76155bc406b1a671c0c2c9027adb40dd142e1854316eb7d8852cae8)
            check_type(argname="argument full_path_match", value=full_path_match, expected_type=type_hints["full_path_match"])
            check_type(argname="argument header_match", value=header_match, expected_type=type_hints["header_match"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument path_template_match", value=path_template_match, expected_type=type_hints["path_template_match"])
            check_type(argname="argument prefix_match", value=prefix_match, expected_type=type_hints["prefix_match"])
            check_type(argname="argument query_parameter_match", value=query_parameter_match, expected_type=type_hints["query_parameter_match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if full_path_match is not None:
            self._values["full_path_match"] = full_path_match
        if header_match is not None:
            self._values["header_match"] = header_match
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if path_template_match is not None:
            self._values["path_template_match"] = path_template_match
        if prefix_match is not None:
            self._values["prefix_match"] = prefix_match
        if query_parameter_match is not None:
            self._values["query_parameter_match"] = query_parameter_match

    @builtins.property
    def full_path_match(self) -> typing.Optional[builtins.str]:
        '''For satisfying the matchRule condition, the path of the request must exactly match the value specified in fullPathMatch after removing any query parameters and anchor that may be part of the original URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#full_path_match NetworkServicesEdgeCacheService#full_path_match}
        '''
        result = self._values.get("full_path_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_match(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch"]]]:
        '''header_match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_match NetworkServicesEdgeCacheService#header_match}
        '''
        result = self._values.get("header_match")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch"]]], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies that prefixMatch and fullPathMatch matches are case sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#ignore_case NetworkServicesEdgeCacheService#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path_template_match(self) -> typing.Optional[builtins.str]:
        '''For satisfying the matchRule condition, the path of the request must match the wildcard pattern specified in pathTemplateMatch after removing any query parameters and anchor that may be part of the original URL.

        pathTemplateMatch must be between 1 and 255 characters
        (inclusive).  The pattern specified by pathTemplateMatch may
        have at most 5 wildcard operators and at most 5 variable
        captures in total.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_template_match NetworkServicesEdgeCacheService#path_template_match}
        '''
        result = self._values.get("path_template_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix_match(self) -> typing.Optional[builtins.str]:
        '''For satisfying the matchRule condition, the request's path must begin with the specified prefixMatch.

        prefixMatch must begin with a /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#prefix_match NetworkServicesEdgeCacheService#prefix_match}
        '''
        result = self._values.get("prefix_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_parameter_match(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch"]]]:
        '''query_parameter_match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#query_parameter_match NetworkServicesEdgeCacheService#query_parameter_match}
        '''
        result = self._values.get("query_parameter_match")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch",
    jsii_struct_bases=[],
    name_mapping={
        "header_name": "headerName",
        "exact_match": "exactMatch",
        "invert_match": "invertMatch",
        "prefix_match": "prefixMatch",
        "present_match": "presentMatch",
        "suffix_match": "suffixMatch",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        exact_match: typing.Optional[builtins.str] = None,
        invert_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix_match: typing.Optional[builtins.str] = None,
        present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suffix_match: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param header_name: The header name to match on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_name NetworkServicesEdgeCacheService#header_name}
        :param exact_match: The value of the header should exactly match contents of exactMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#exact_match NetworkServicesEdgeCacheService#exact_match}
        :param invert_match: If set to false (default), the headerMatch is considered a match if the match criteria above are met. If set to true, the headerMatch is considered a match if the match criteria above are NOT met. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#invert_match NetworkServicesEdgeCacheService#invert_match}
        :param prefix_match: The value of the header must start with the contents of prefixMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#prefix_match NetworkServicesEdgeCacheService#prefix_match}
        :param present_match: A header with the contents of headerName must exist. The match takes place whether or not the request's header has a value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#present_match NetworkServicesEdgeCacheService#present_match}
        :param suffix_match: The value of the header must end with the contents of suffixMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#suffix_match NetworkServicesEdgeCacheService#suffix_match}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8dfecd7c8b832b2debd0be864c2b42d98e62bb7fc8ee93ab991acfff0d69f66)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument exact_match", value=exact_match, expected_type=type_hints["exact_match"])
            check_type(argname="argument invert_match", value=invert_match, expected_type=type_hints["invert_match"])
            check_type(argname="argument prefix_match", value=prefix_match, expected_type=type_hints["prefix_match"])
            check_type(argname="argument present_match", value=present_match, expected_type=type_hints["present_match"])
            check_type(argname="argument suffix_match", value=suffix_match, expected_type=type_hints["suffix_match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
        }
        if exact_match is not None:
            self._values["exact_match"] = exact_match
        if invert_match is not None:
            self._values["invert_match"] = invert_match
        if prefix_match is not None:
            self._values["prefix_match"] = prefix_match
        if present_match is not None:
            self._values["present_match"] = present_match
        if suffix_match is not None:
            self._values["suffix_match"] = suffix_match

    @builtins.property
    def header_name(self) -> builtins.str:
        '''The header name to match on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#header_name NetworkServicesEdgeCacheService#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exact_match(self) -> typing.Optional[builtins.str]:
        '''The value of the header should exactly match contents of exactMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#exact_match NetworkServicesEdgeCacheService#exact_match}
        '''
        result = self._values.get("exact_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to false (default), the headerMatch is considered a match if the match criteria above are met.

        If set to true, the headerMatch is considered a match if the match criteria above are NOT met.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#invert_match NetworkServicesEdgeCacheService#invert_match}
        '''
        result = self._values.get("invert_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix_match(self) -> typing.Optional[builtins.str]:
        '''The value of the header must start with the contents of prefixMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#prefix_match NetworkServicesEdgeCacheService#prefix_match}
        '''
        result = self._values.get("prefix_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def present_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A header with the contents of headerName must exist.

        The match takes place whether or not the request's header has a value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#present_match NetworkServicesEdgeCacheService#present_match}
        '''
        result = self._values.get("present_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def suffix_match(self) -> typing.Optional[builtins.str]:
        '''The value of the header must end with the contents of suffixMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#suffix_match NetworkServicesEdgeCacheService#suffix_match}
        '''
        result = self._values.get("suffix_match")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__629daa08cbaf8f4aea74734ff4a9949a309aa4df575173324a1a184acb89a939)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da5552f202155e249ea80608dd26ce5c10378fd1b377a018395f19f337e634a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69fd0e422a0bc119acf0ae095f021811d0cd8974c3a1190f8a000413ea6bb23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e25666493aebcc28fdd3049fec7751ca8c0c843b5d2e4bc1f4d71805bfd7ef4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93f3d89eb38beadf1c9f1463ee7f962f8382e8b2169541484c8cfea2d717de0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92d2aa8baeae231a9c55de144f14dde6fc1c63d0e70370b2a596e92b3f99e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b337855d3db2780533a9abbc11f59752c60bee07867eec3a9a92f1fc79cf0776)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExactMatch")
    def reset_exact_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExactMatch", []))

    @jsii.member(jsii_name="resetInvertMatch")
    def reset_invert_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvertMatch", []))

    @jsii.member(jsii_name="resetPrefixMatch")
    def reset_prefix_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixMatch", []))

    @jsii.member(jsii_name="resetPresentMatch")
    def reset_present_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPresentMatch", []))

    @jsii.member(jsii_name="resetSuffixMatch")
    def reset_suffix_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffixMatch", []))

    @builtins.property
    @jsii.member(jsii_name="exactMatchInput")
    def exact_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="headerNameInput")
    def header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="invertMatchInput")
    def invert_match_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixMatchInput")
    def prefix_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="presentMatchInput")
    def present_match_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "presentMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixMatchInput")
    def suffix_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="exactMatch")
    def exact_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exactMatch"))

    @exact_match.setter
    def exact_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da3adaaac0454eb0ba7b1520a618f7dd7d00f4f6c44d19b57622707b33b6e65b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exactMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b788459afb28db0af440abec93005f1e7efba0e397c49bee265fc7f2d2fd496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invertMatch")
    def invert_match(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invertMatch"))

    @invert_match.setter
    def invert_match(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b11c2799628f71ae0ef410d713bc94797cbc2357d45605f1685fabebef71470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixMatch")
    def prefix_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixMatch"))

    @prefix_match.setter
    def prefix_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ffb266c39b714e2832118228efeb7c08ae36d7758220403371e3f4e5d83339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="presentMatch")
    def present_match(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "presentMatch"))

    @present_match.setter
    def present_match(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc4f93b6fb0f2e82811f1885150bc63f70f73439ea5d089ca9af213b1bb241e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "presentMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffixMatch")
    def suffix_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffixMatch"))

    @suffix_match.setter
    def suffix_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c97dbe2b9dd76d2f9f2e63d0ff3ce28dba7e559c6b1ae9e6d4901d58786a92b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffixMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4adfa5e90581973b58cf79149ff3a2a8efacd5ece21f6dcbca3411bae0cf78a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad0250dbab483ac3f27145066341d65e63be82c5f894488e5211d8f6aea74a69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c9c5522176ea1040980cbd99ee4bf757d9516b44a6a705c97742d1c62f2a3f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef389801c2b9c85e834985f05f4d04130f7a4023ad393d66963dcff849b539c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55fce2dde1c4392183f70736006227ac9b1e46d8b3c67e775a85d54a4eac990d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5da51e70cedd59038c7ff37146a2ea3907cca3a2131dea230a5f093e4f84b1fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf471188280722e75bbca9362638dee70d1ddf83cd01e7bab8c5f5d0086cc34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1573d79eb927e64f72bb56ec948d860e5e7239d294d7842426ec42abe6172fe1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaderMatch")
    def put_header_match(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aceaab46c4cbb4a3021e0e79df6bb4ea56f10d159f81a391ef035034c706cfbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaderMatch", [value]))

    @jsii.member(jsii_name="putQueryParameterMatch")
    def put_query_parameter_match(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf9a1c0b74076439dc1cf9ec06d79cf3eca0c01fc1fd05941d0cc08eb240d47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryParameterMatch", [value]))

    @jsii.member(jsii_name="resetFullPathMatch")
    def reset_full_path_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFullPathMatch", []))

    @jsii.member(jsii_name="resetHeaderMatch")
    def reset_header_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderMatch", []))

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetPathTemplateMatch")
    def reset_path_template_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathTemplateMatch", []))

    @jsii.member(jsii_name="resetPrefixMatch")
    def reset_prefix_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixMatch", []))

    @jsii.member(jsii_name="resetQueryParameterMatch")
    def reset_query_parameter_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryParameterMatch", []))

    @builtins.property
    @jsii.member(jsii_name="headerMatch")
    def header_match(
        self,
    ) -> NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchList:
        return typing.cast(NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchList, jsii.get(self, "headerMatch"))

    @builtins.property
    @jsii.member(jsii_name="queryParameterMatch")
    def query_parameter_match(
        self,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchList":
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchList", jsii.get(self, "queryParameterMatch"))

    @builtins.property
    @jsii.member(jsii_name="fullPathMatchInput")
    def full_path_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fullPathMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="headerMatchInput")
    def header_match_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]], jsii.get(self, "headerMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="pathTemplateMatchInput")
    def path_template_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathTemplateMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixMatchInput")
    def prefix_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParameterMatchInput")
    def query_parameter_match_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch"]]], jsii.get(self, "queryParameterMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="fullPathMatch")
    def full_path_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullPathMatch"))

    @full_path_match.setter
    def full_path_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ace81f9c78b3ca8ce0331672eeee1b9f90fcc861f5d6802649b5d87c242e0615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullPathMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d36d1a3e620a04d0b4c3e64edb57409af274f18fdf9611bce0ac396584acdd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathTemplateMatch")
    def path_template_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathTemplateMatch"))

    @path_template_match.setter
    def path_template_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f3e95077514a1bebef169418b01399d08a5673f1fc02c040d3c227ee33e81c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathTemplateMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixMatch")
    def prefix_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixMatch"))

    @prefix_match.setter
    def prefix_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408fc004e6ef9e06a87a2e2ed07d4e3e9519534b3a818cb80ec670eefe63b5e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6c29fe3b6866d4dc38dab5d9df5fd5bd93f66bcaf733f79b74a067fe4000326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "exact_match": "exactMatch",
        "present_match": "presentMatch",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch:
    def __init__(
        self,
        *,
        name: builtins.str,
        exact_match: typing.Optional[builtins.str] = None,
        present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: The name of the query parameter to match. The query parameter must exist in the request, in the absence of which the request match fails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#name NetworkServicesEdgeCacheService#name}
        :param exact_match: The queryParameterMatch matches if the value of the parameter exactly matches the contents of exactMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#exact_match NetworkServicesEdgeCacheService#exact_match}
        :param present_match: Specifies that the queryParameterMatch matches if the request contains the query parameter, irrespective of whether the parameter has a value or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#present_match NetworkServicesEdgeCacheService#present_match}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606afefc0e88cb34b8de3640d4351a930d33358522bb80cc672f6b560b53c03e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument exact_match", value=exact_match, expected_type=type_hints["exact_match"])
            check_type(argname="argument present_match", value=present_match, expected_type=type_hints["present_match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if exact_match is not None:
            self._values["exact_match"] = exact_match
        if present_match is not None:
            self._values["present_match"] = present_match

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the query parameter to match.

        The query parameter must exist in the request, in the absence of which the request match fails.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#name NetworkServicesEdgeCacheService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exact_match(self) -> typing.Optional[builtins.str]:
        '''The queryParameterMatch matches if the value of the parameter exactly matches the contents of exactMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#exact_match NetworkServicesEdgeCacheService#exact_match}
        '''
        result = self._values.get("exact_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def present_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies that the queryParameterMatch matches if the request contains the query parameter, irrespective of whether the parameter has a value or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#present_match NetworkServicesEdgeCacheService#present_match}
        '''
        result = self._values.get("present_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3beabaa153c79555409332fdda87ba765a68db1df1359606d10d4b88f8fc7752)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a29bbeb8c4cda4f402633977a06a35e4b624d26cc69470fabdd889347018baa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25b5e8738e740136997dff2ebc3e44d7ad43f86e2486d4120f6f29010815919)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a8bd717a0d35e3fc3a7188b73d857e5241ddcb6ab785ad73ab9d89b975874e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d87373c6bcdc031ec66bacb9e289aa82edecd8e30255d4d46796bed42c8eff0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e17107b30a2adcbfbdee30328dcbec6b576c923495a4fd857c3e61de4583645e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8aee0bca3219e5ffa79dae90736184f415e248b819c7803f800d8cfd836fe1c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExactMatch")
    def reset_exact_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExactMatch", []))

    @jsii.member(jsii_name="resetPresentMatch")
    def reset_present_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPresentMatch", []))

    @builtins.property
    @jsii.member(jsii_name="exactMatchInput")
    def exact_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="presentMatchInput")
    def present_match_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "presentMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="exactMatch")
    def exact_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exactMatch"))

    @exact_match.setter
    def exact_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__004a6ba330e2af89c104a778f6cd1299522b66f34cfdd3ebce95b1ddefb136e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exactMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e4767f42122a61c7c2368f6892606a3d9eb68471276bbff16b507ba3411d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="presentMatch")
    def present_match(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "presentMatch"))

    @present_match.setter
    def present_match(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663d22a99b22d43d6ac100e41291ec6fa9b4ffb3aaf4399e283139d1b5cb8e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "presentMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ce9c2c112f40b0a35fb1252bed4741a6779e7907a8095ae794d42f8b3e87df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2114c1d9609df0fd3d4c2f0222ef3a4ce89637761846dabd76aa6387b7834045)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaderAction")
    def put_header_action(
        self,
        *,
        request_header_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd, typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header_to_remove: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove, typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_header_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd, typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_header_to_remove: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_header_to_add: request_header_to_add block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#request_header_to_add NetworkServicesEdgeCacheService#request_header_to_add}
        :param request_header_to_remove: request_header_to_remove block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#request_header_to_remove NetworkServicesEdgeCacheService#request_header_to_remove}
        :param response_header_to_add: response_header_to_add block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#response_header_to_add NetworkServicesEdgeCacheService#response_header_to_add}
        :param response_header_to_remove: response_header_to_remove block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#response_header_to_remove NetworkServicesEdgeCacheService#response_header_to_remove}
        '''
        value = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction(
            request_header_to_add=request_header_to_add,
            request_header_to_remove=request_header_to_remove,
            response_header_to_add=response_header_to_add,
            response_header_to_remove=response_header_to_remove,
        )

        return typing.cast(None, jsii.invoke(self, "putHeaderAction", [value]))

    @jsii.member(jsii_name="putMatchRule")
    def put_match_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f99f199439fffc8e1c779d1efb6e7187500eb786043bfdc9f9f9e549db2600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchRule", [value]))

    @jsii.member(jsii_name="putRouteAction")
    def put_route_action(
        self,
        *,
        cdn_policy: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_mode: typing.Optional[builtins.str] = None,
        cors_policy: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        url_rewrite: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#cdn_policy NetworkServicesEdgeCacheService#cdn_policy}
        :param compression_mode: Setting the compression mode to automatic enables dynamic compression for every eligible response. When dynamic compression is enabled, it is recommended to also set a cache policy to maximize efficiency. Possible values: ["DISABLED", "AUTOMATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#compression_mode NetworkServicesEdgeCacheService#compression_mode}
        :param cors_policy: cors_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#cors_policy NetworkServicesEdgeCacheService#cors_policy}
        :param url_rewrite: url_rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#url_rewrite NetworkServicesEdgeCacheService#url_rewrite}
        '''
        value = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction(
            cdn_policy=cdn_policy,
            compression_mode=compression_mode,
            cors_policy=cors_policy,
            url_rewrite=url_rewrite,
        )

        return typing.cast(None, jsii.invoke(self, "putRouteAction", [value]))

    @jsii.member(jsii_name="putRouteMethods")
    def put_route_methods(
        self,
        *,
        allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_methods: The non-empty set of HTTP methods that are allowed for this route. Any combination of "GET", "HEAD", "OPTIONS", "PUT", "POST", "DELETE", and "PATCH". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allowed_methods NetworkServicesEdgeCacheService#allowed_methods}
        '''
        value = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods(
            allowed_methods=allowed_methods
        )

        return typing.cast(None, jsii.invoke(self, "putRouteMethods", [value]))

    @jsii.member(jsii_name="putUrlRedirect")
    def put_url_redirect(
        self,
        *,
        host_redirect: typing.Optional[builtins.str] = None,
        https_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path_redirect: typing.Optional[builtins.str] = None,
        prefix_redirect: typing.Optional[builtins.str] = None,
        redirect_response_code: typing.Optional[builtins.str] = None,
        strip_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param host_redirect: The host that will be used in the redirect response instead of the one that was supplied in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#host_redirect NetworkServicesEdgeCacheService#host_redirect}
        :param https_redirect: If set to true, the URL scheme in the redirected request is set to https. If set to false, the URL scheme of the redirected request will remain the same as that of the request. This can only be set if there is at least one (1) edgeSslCertificate set on the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#https_redirect NetworkServicesEdgeCacheService#https_redirect}
        :param path_redirect: The path that will be used in the redirect response instead of the one that was supplied in the request. pathRedirect cannot be supplied together with prefixRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect. The path value must be between 1 and 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_redirect NetworkServicesEdgeCacheService#path_redirect}
        :param prefix_redirect: The prefix that replaces the prefixMatch specified in the routeRule, retaining the remaining portion of the URL before redirecting the request. prefixRedirect cannot be supplied together with pathRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#prefix_redirect NetworkServicesEdgeCacheService#prefix_redirect}
        :param redirect_response_code: The HTTP Status code to use for this RedirectAction. The supported values are: - 'MOVED_PERMANENTLY_DEFAULT', which is the default value and corresponds to 301. - 'FOUND', which corresponds to 302. - 'SEE_OTHER' which corresponds to 303. - 'TEMPORARY_REDIRECT', which corresponds to 307. in this case, the request method will be retained. - 'PERMANENT_REDIRECT', which corresponds to 308. in this case, the request method will be retained. Possible values: ["MOVED_PERMANENTLY_DEFAULT", "FOUND", "SEE_OTHER", "TEMPORARY_REDIRECT", "PERMANENT_REDIRECT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#redirect_response_code NetworkServicesEdgeCacheService#redirect_response_code}
        :param strip_query: If set to true, any accompanying query portion of the original URL is removed prior to redirecting the request. If set to false, the query portion of the original URL is retained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#strip_query NetworkServicesEdgeCacheService#strip_query}
        '''
        value = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect(
            host_redirect=host_redirect,
            https_redirect=https_redirect,
            path_redirect=path_redirect,
            prefix_redirect=prefix_redirect,
            redirect_response_code=redirect_response_code,
            strip_query=strip_query,
        )

        return typing.cast(None, jsii.invoke(self, "putUrlRedirect", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHeaderAction")
    def reset_header_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderAction", []))

    @jsii.member(jsii_name="resetOrigin")
    def reset_origin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrigin", []))

    @jsii.member(jsii_name="resetRouteAction")
    def reset_route_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteAction", []))

    @jsii.member(jsii_name="resetRouteMethods")
    def reset_route_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteMethods", []))

    @jsii.member(jsii_name="resetUrlRedirect")
    def reset_url_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlRedirect", []))

    @builtins.property
    @jsii.member(jsii_name="headerAction")
    def header_action(
        self,
    ) -> NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionOutputReference:
        return typing.cast(NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionOutputReference, jsii.get(self, "headerAction"))

    @builtins.property
    @jsii.member(jsii_name="matchRule")
    def match_rule(
        self,
    ) -> NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleList:
        return typing.cast(NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleList, jsii.get(self, "matchRule"))

    @builtins.property
    @jsii.member(jsii_name="routeAction")
    def route_action(
        self,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionOutputReference":
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionOutputReference", jsii.get(self, "routeAction"))

    @builtins.property
    @jsii.member(jsii_name="routeMethods")
    def route_methods(
        self,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethodsOutputReference":
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethodsOutputReference", jsii.get(self, "routeMethods"))

    @builtins.property
    @jsii.member(jsii_name="urlRedirect")
    def url_redirect(
        self,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirectOutputReference":
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirectOutputReference", jsii.get(self, "urlRedirect"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="headerActionInput")
    def header_action_input(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction], jsii.get(self, "headerActionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchRuleInput")
    def match_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]], jsii.get(self, "matchRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="originInput")
    def origin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="routeActionInput")
    def route_action_input(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction"]:
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction"], jsii.get(self, "routeActionInput"))

    @builtins.property
    @jsii.member(jsii_name="routeMethodsInput")
    def route_methods_input(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods"]:
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods"], jsii.get(self, "routeMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRedirectInput")
    def url_redirect_input(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect"]:
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect"], jsii.get(self, "urlRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151a3a6c35f4ecb381dd08c46afcbfed7eb98fff53031ae4fd6eaa06841cc3e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "origin"))

    @origin.setter
    def origin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__453fab5a3e4a2161385866d23e32747b3958c291ea079c9488b3b248b59a3e1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "origin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77493902bfb6c0af047a83b453eed95c7ad0c4c443fa46321e9843d093e7146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb04ff6b6cc9ec36ea41788fb61dfb665806372cb3a959b44ce28b65e664119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction",
    jsii_struct_bases=[],
    name_mapping={
        "cdn_policy": "cdnPolicy",
        "compression_mode": "compressionMode",
        "cors_policy": "corsPolicy",
        "url_rewrite": "urlRewrite",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction:
    def __init__(
        self,
        *,
        cdn_policy: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_mode: typing.Optional[builtins.str] = None,
        cors_policy: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        url_rewrite: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#cdn_policy NetworkServicesEdgeCacheService#cdn_policy}
        :param compression_mode: Setting the compression mode to automatic enables dynamic compression for every eligible response. When dynamic compression is enabled, it is recommended to also set a cache policy to maximize efficiency. Possible values: ["DISABLED", "AUTOMATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#compression_mode NetworkServicesEdgeCacheService#compression_mode}
        :param cors_policy: cors_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#cors_policy NetworkServicesEdgeCacheService#cors_policy}
        :param url_rewrite: url_rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#url_rewrite NetworkServicesEdgeCacheService#url_rewrite}
        '''
        if isinstance(cdn_policy, dict):
            cdn_policy = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy(**cdn_policy)
        if isinstance(cors_policy, dict):
            cors_policy = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy(**cors_policy)
        if isinstance(url_rewrite, dict):
            url_rewrite = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite(**url_rewrite)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3bf4b2751a9fd04694026fa3ab613987e3e66ab8d5f501a4c0112449aad3482)
            check_type(argname="argument cdn_policy", value=cdn_policy, expected_type=type_hints["cdn_policy"])
            check_type(argname="argument compression_mode", value=compression_mode, expected_type=type_hints["compression_mode"])
            check_type(argname="argument cors_policy", value=cors_policy, expected_type=type_hints["cors_policy"])
            check_type(argname="argument url_rewrite", value=url_rewrite, expected_type=type_hints["url_rewrite"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cdn_policy is not None:
            self._values["cdn_policy"] = cdn_policy
        if compression_mode is not None:
            self._values["compression_mode"] = compression_mode
        if cors_policy is not None:
            self._values["cors_policy"] = cors_policy
        if url_rewrite is not None:
            self._values["url_rewrite"] = url_rewrite

    @builtins.property
    def cdn_policy(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy"]:
        '''cdn_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#cdn_policy NetworkServicesEdgeCacheService#cdn_policy}
        '''
        result = self._values.get("cdn_policy")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy"], result)

    @builtins.property
    def compression_mode(self) -> typing.Optional[builtins.str]:
        '''Setting the compression mode to automatic enables dynamic compression for every eligible response.

        When dynamic compression is enabled, it is recommended to also set a cache policy to maximize efficiency. Possible values: ["DISABLED", "AUTOMATIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#compression_mode NetworkServicesEdgeCacheService#compression_mode}
        '''
        result = self._values.get("compression_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors_policy(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy"]:
        '''cors_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#cors_policy NetworkServicesEdgeCacheService#cors_policy}
        '''
        result = self._values.get("cors_policy")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy"], result)

    @builtins.property
    def url_rewrite(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite"]:
        '''url_rewrite block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#url_rewrite NetworkServicesEdgeCacheService#url_rewrite}
        '''
        result = self._values.get("url_rewrite")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "add_signatures": "addSignatures",
        "cache_key_policy": "cacheKeyPolicy",
        "cache_mode": "cacheMode",
        "client_ttl": "clientTtl",
        "default_ttl": "defaultTtl",
        "max_ttl": "maxTtl",
        "negative_caching": "negativeCaching",
        "negative_caching_policy": "negativeCachingPolicy",
        "signed_request_keyset": "signedRequestKeyset",
        "signed_request_maximum_expiration_ttl": "signedRequestMaximumExpirationTtl",
        "signed_request_mode": "signedRequestMode",
        "signed_token_options": "signedTokenOptions",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy:
    def __init__(
        self,
        *,
        add_signatures: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_key_policy: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[builtins.str] = None,
        default_ttl: typing.Optional[builtins.str] = None,
        max_ttl: typing.Optional[builtins.str] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        signed_request_keyset: typing.Optional[builtins.str] = None,
        signed_request_maximum_expiration_ttl: typing.Optional[builtins.str] = None,
        signed_request_mode: typing.Optional[builtins.str] = None,
        signed_token_options: typing.Optional[typing.Union["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param add_signatures: add_signatures block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#add_signatures NetworkServicesEdgeCacheService#add_signatures}
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#cache_key_policy NetworkServicesEdgeCacheService#cache_key_policy}
        :param cache_mode: Cache modes allow users to control the behaviour of the cache, what content it should cache automatically, whether to respect origin headers, or whether to unconditionally cache all responses. For all cache modes, Cache-Control headers will be passed to the client. Use clientTtl to override what is sent to the client. Possible values: ["CACHE_ALL_STATIC", "USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "BYPASS_CACHE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#cache_mode NetworkServicesEdgeCacheService#cache_mode}
        :param client_ttl: Specifies a separate client (e.g. browser client) TTL, separate from the TTL used by the edge caches. Leaving this empty will use the same cache TTL for both the CDN and the client-facing response. - The TTL must be > 0 and <= 86400s (1 day) - The clientTtl cannot be larger than the defaultTtl (if set) - Fractions of a second are not allowed. Omit this field to use the defaultTtl, or the max-age set by the origin, as the client-facing TTL. When the cache mode is set to "USE_ORIGIN_HEADERS" or "BYPASS_CACHE", you must omit this field. A duration in seconds terminated by 's'. Example: "3s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#client_ttl NetworkServicesEdgeCacheService#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). Defaults to 3600s (1 hour). - The TTL must be >= 0 and <= 31,536,000 seconds (1 year) - Setting a TTL of "0" means "always revalidate" (equivalent to must-revalidate) - The value of defaultTTL cannot be set to a value greater than that of maxTTL. - Fractions of a second are not allowed. - When the cacheMode is set to FORCE_CACHE_ALL, the defaultTTL will overwrite the TTL set in all responses. Note that infrequently accessed objects may be evicted from the cache before the defined TTL. Objects that expire will be revalidated with the origin. When the cache mode is set to "USE_ORIGIN_HEADERS" or "BYPASS_CACHE", you must omit this field. A duration in seconds terminated by 's'. Example: "3s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#default_ttl NetworkServicesEdgeCacheService#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Defaults to 86400s (1 day). Cache directives that attempt to set a max-age or s-maxage higher than this, or an Expires header more than maxTtl seconds in the future will be capped at the value of maxTTL, as if it were the value of an s-maxage Cache-Control directive. - The TTL must be >= 0 and <= 31,536,000 seconds (1 year) - Setting a TTL of "0" means "always revalidate" - The value of maxTtl must be equal to or greater than defaultTtl. - Fractions of a second are not allowed. When the cache mode is set to "USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", or "BYPASS_CACHE", you must omit this field. A duration in seconds terminated by 's'. Example: "3s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#max_ttl NetworkServicesEdgeCacheService#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. This can reduce the load on your origin and improve end-user experience by reducing response latency. By default, the CDNPolicy will apply the following default TTLs to these status codes: - HTTP 300 (Multiple Choice), 301, 308 (Permanent Redirects): 10m - HTTP 404 (Not Found), 410 (Gone), 451 (Unavailable For Legal Reasons): 120s - HTTP 405 (Method Not Found), 414 (URI Too Long), 501 (Not Implemented): 60s These defaults can be overridden in negativeCachingPolicy Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#negative_caching NetworkServicesEdgeCacheService#negative_caching}
        :param negative_caching_policy: Sets a cache TTL for the specified HTTP status code. negativeCaching must be enabled to configure negativeCachingPolicy. - Omitting the policy and leaving negativeCaching enabled will use the default TTLs for each status code, defined in negativeCaching. - TTLs must be >= 0 (where 0 is "always revalidate") and <= 86400s (1 day) Note that when specifying an explicit negativeCachingPolicy, you should take care to specify a cache TTL for all response codes that you wish to cache. The CDNPolicy will not apply any default negative caching when a policy exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#negative_caching_policy NetworkServicesEdgeCacheService#negative_caching_policy}
        :param signed_request_keyset: The EdgeCacheKeyset containing the set of public keys used to validate signed requests at the edge. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#signed_request_keyset NetworkServicesEdgeCacheService#signed_request_keyset}
        :param signed_request_maximum_expiration_ttl: Limit how far into the future the expiration time of a signed request may be. When set, a signed request is rejected if its expiration time is later than now + signedRequestMaximumExpirationTtl, where now is the time at which the signed request is first handled by the CDN. - The TTL must be > 0. - Fractions of a second are not allowed. By default, signedRequestMaximumExpirationTtl is not set and the expiration time of a signed request may be arbitrarily far into future. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#signed_request_maximum_expiration_ttl NetworkServicesEdgeCacheService#signed_request_maximum_expiration_ttl}
        :param signed_request_mode: Whether to enforce signed requests. The default value is DISABLED, which means all content is public, and does not authorize access. You must also set a signedRequestKeyset to enable signed requests. When set to REQUIRE_SIGNATURES, all matching requests will have their signature validated. Requests that were not signed with the corresponding private key, or that are otherwise invalid (expired, do not match the signature, IP address, or header) will be rejected with a HTTP 403 and (if enabled) logged. Possible values: ["DISABLED", "REQUIRE_SIGNATURES", "REQUIRE_TOKENS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#signed_request_mode NetworkServicesEdgeCacheService#signed_request_mode}
        :param signed_token_options: signed_token_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#signed_token_options NetworkServicesEdgeCacheService#signed_token_options}
        '''
        if isinstance(add_signatures, dict):
            add_signatures = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures(**add_signatures)
        if isinstance(cache_key_policy, dict):
            cache_key_policy = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy(**cache_key_policy)
        if isinstance(signed_token_options, dict):
            signed_token_options = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions(**signed_token_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7664c3e48a20a800949f8d9c133627ad6fc1a8615b84ba9eaea0965356e53a7)
            check_type(argname="argument add_signatures", value=add_signatures, expected_type=type_hints["add_signatures"])
            check_type(argname="argument cache_key_policy", value=cache_key_policy, expected_type=type_hints["cache_key_policy"])
            check_type(argname="argument cache_mode", value=cache_mode, expected_type=type_hints["cache_mode"])
            check_type(argname="argument client_ttl", value=client_ttl, expected_type=type_hints["client_ttl"])
            check_type(argname="argument default_ttl", value=default_ttl, expected_type=type_hints["default_ttl"])
            check_type(argname="argument max_ttl", value=max_ttl, expected_type=type_hints["max_ttl"])
            check_type(argname="argument negative_caching", value=negative_caching, expected_type=type_hints["negative_caching"])
            check_type(argname="argument negative_caching_policy", value=negative_caching_policy, expected_type=type_hints["negative_caching_policy"])
            check_type(argname="argument signed_request_keyset", value=signed_request_keyset, expected_type=type_hints["signed_request_keyset"])
            check_type(argname="argument signed_request_maximum_expiration_ttl", value=signed_request_maximum_expiration_ttl, expected_type=type_hints["signed_request_maximum_expiration_ttl"])
            check_type(argname="argument signed_request_mode", value=signed_request_mode, expected_type=type_hints["signed_request_mode"])
            check_type(argname="argument signed_token_options", value=signed_token_options, expected_type=type_hints["signed_token_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_signatures is not None:
            self._values["add_signatures"] = add_signatures
        if cache_key_policy is not None:
            self._values["cache_key_policy"] = cache_key_policy
        if cache_mode is not None:
            self._values["cache_mode"] = cache_mode
        if client_ttl is not None:
            self._values["client_ttl"] = client_ttl
        if default_ttl is not None:
            self._values["default_ttl"] = default_ttl
        if max_ttl is not None:
            self._values["max_ttl"] = max_ttl
        if negative_caching is not None:
            self._values["negative_caching"] = negative_caching
        if negative_caching_policy is not None:
            self._values["negative_caching_policy"] = negative_caching_policy
        if signed_request_keyset is not None:
            self._values["signed_request_keyset"] = signed_request_keyset
        if signed_request_maximum_expiration_ttl is not None:
            self._values["signed_request_maximum_expiration_ttl"] = signed_request_maximum_expiration_ttl
        if signed_request_mode is not None:
            self._values["signed_request_mode"] = signed_request_mode
        if signed_token_options is not None:
            self._values["signed_token_options"] = signed_token_options

    @builtins.property
    def add_signatures(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures"]:
        '''add_signatures block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#add_signatures NetworkServicesEdgeCacheService#add_signatures}
        '''
        result = self._values.get("add_signatures")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures"], result)

    @builtins.property
    def cache_key_policy(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy"]:
        '''cache_key_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#cache_key_policy NetworkServicesEdgeCacheService#cache_key_policy}
        '''
        result = self._values.get("cache_key_policy")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy"], result)

    @builtins.property
    def cache_mode(self) -> typing.Optional[builtins.str]:
        '''Cache modes allow users to control the behaviour of the cache, what content it should cache automatically, whether to respect origin headers, or whether to unconditionally cache all responses.

        For all cache modes, Cache-Control headers will be passed to the client. Use clientTtl to override what is sent to the client. Possible values: ["CACHE_ALL_STATIC", "USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "BYPASS_CACHE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#cache_mode NetworkServicesEdgeCacheService#cache_mode}
        '''
        result = self._values.get("cache_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_ttl(self) -> typing.Optional[builtins.str]:
        '''Specifies a separate client (e.g. browser client) TTL, separate from the TTL used by the edge caches. Leaving this empty will use the same cache TTL for both the CDN and the client-facing response.

        - The TTL must be > 0 and <= 86400s (1 day)
        - The clientTtl cannot be larger than the defaultTtl (if set)
        - Fractions of a second are not allowed.

        Omit this field to use the defaultTtl, or the max-age set by the origin, as the client-facing TTL.

        When the cache mode is set to "USE_ORIGIN_HEADERS" or "BYPASS_CACHE", you must omit this field.
        A duration in seconds terminated by 's'. Example: "3s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#client_ttl NetworkServicesEdgeCacheService#client_ttl}
        '''
        result = self._values.get("client_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[builtins.str]:
        '''Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age).

        Defaults to 3600s (1 hour).

        - The TTL must be >= 0 and <= 31,536,000 seconds (1 year)
        - Setting a TTL of "0" means "always revalidate" (equivalent to must-revalidate)
        - The value of defaultTTL cannot be set to a value greater than that of maxTTL.
        - Fractions of a second are not allowed.
        - When the cacheMode is set to FORCE_CACHE_ALL, the defaultTTL will overwrite the TTL set in all responses.

        Note that infrequently accessed objects may be evicted from the cache before the defined TTL. Objects that expire will be revalidated with the origin.

        When the cache mode is set to "USE_ORIGIN_HEADERS" or "BYPASS_CACHE", you must omit this field.

        A duration in seconds terminated by 's'. Example: "3s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#default_ttl NetworkServicesEdgeCacheService#default_ttl}
        '''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_ttl(self) -> typing.Optional[builtins.str]:
        '''Specifies the maximum allowed TTL for cached content served by this origin.

        Defaults to 86400s (1 day).

        Cache directives that attempt to set a max-age or s-maxage higher than this, or an Expires header more than maxTtl seconds in the future will be capped at the value of maxTTL, as if it were the value of an s-maxage Cache-Control directive.

        - The TTL must be >= 0 and <= 31,536,000 seconds (1 year)
        - Setting a TTL of "0" means "always revalidate"
        - The value of maxTtl must be equal to or greater than defaultTtl.
        - Fractions of a second are not allowed.

        When the cache mode is set to "USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", or "BYPASS_CACHE", you must omit this field.

        A duration in seconds terminated by 's'. Example: "3s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#max_ttl NetworkServicesEdgeCacheService#max_ttl}
        '''
        result = self._values.get("max_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negative_caching(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects.

        This can reduce the load on your origin and improve end-user experience by reducing response latency.

        By default, the CDNPolicy will apply the following default TTLs to these status codes:

        - HTTP 300 (Multiple Choice), 301, 308 (Permanent Redirects): 10m
        - HTTP 404 (Not Found), 410 (Gone), 451 (Unavailable For Legal Reasons): 120s
        - HTTP 405 (Method Not Found), 414 (URI Too Long), 501 (Not Implemented): 60s

        These defaults can be overridden in negativeCachingPolicy

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#negative_caching NetworkServicesEdgeCacheService#negative_caching}
        '''
        result = self._values.get("negative_caching")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def negative_caching_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Sets a cache TTL for the specified HTTP status code. negativeCaching must be enabled to configure negativeCachingPolicy.

        - Omitting the policy and leaving negativeCaching enabled will use the default TTLs for each status code, defined in negativeCaching.
        - TTLs must be >= 0 (where 0 is "always revalidate") and <= 86400s (1 day)

        Note that when specifying an explicit negativeCachingPolicy, you should take care to specify a cache TTL for all response codes that you wish to cache. The CDNPolicy will not apply any default negative caching when a policy exists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#negative_caching_policy NetworkServicesEdgeCacheService#negative_caching_policy}
        '''
        result = self._values.get("negative_caching_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def signed_request_keyset(self) -> typing.Optional[builtins.str]:
        '''The EdgeCacheKeyset containing the set of public keys used to validate signed requests at the edge.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#signed_request_keyset NetworkServicesEdgeCacheService#signed_request_keyset}
        '''
        result = self._values.get("signed_request_keyset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signed_request_maximum_expiration_ttl(self) -> typing.Optional[builtins.str]:
        '''Limit how far into the future the expiration time of a signed request may be.

        When set, a signed request is rejected if its expiration time is later than now + signedRequestMaximumExpirationTtl, where now is the time at which the signed request is first handled by the CDN.

        - The TTL must be > 0.
        - Fractions of a second are not allowed.

        By default, signedRequestMaximumExpirationTtl is not set and the expiration time of a signed request may be arbitrarily far into future.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#signed_request_maximum_expiration_ttl NetworkServicesEdgeCacheService#signed_request_maximum_expiration_ttl}
        '''
        result = self._values.get("signed_request_maximum_expiration_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signed_request_mode(self) -> typing.Optional[builtins.str]:
        '''Whether to enforce signed requests.

        The default value is DISABLED, which means all content is public, and does not authorize access.

        You must also set a signedRequestKeyset to enable signed requests.

        When set to REQUIRE_SIGNATURES, all matching requests will have their signature validated. Requests that were not signed with the corresponding private key, or that are otherwise invalid (expired, do not match the signature, IP address, or header) will be rejected with a HTTP 403 and (if enabled) logged. Possible values: ["DISABLED", "REQUIRE_SIGNATURES", "REQUIRE_TOKENS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#signed_request_mode NetworkServicesEdgeCacheService#signed_request_mode}
        '''
        result = self._values.get("signed_request_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signed_token_options(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions"]:
        '''signed_token_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#signed_token_options NetworkServicesEdgeCacheService#signed_token_options}
        '''
        result = self._values.get("signed_token_options")
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "copied_parameters": "copiedParameters",
        "keyset": "keyset",
        "token_query_parameter": "tokenQueryParameter",
        "token_ttl": "tokenTtl",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures:
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        copied_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
        keyset: typing.Optional[builtins.str] = None,
        token_query_parameter: typing.Optional[builtins.str] = None,
        token_ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param actions: The actions to take to add signatures to responses. Possible values: ["GENERATE_COOKIE", "GENERATE_TOKEN_HLS_COOKIELESS", "PROPAGATE_TOKEN_HLS_COOKIELESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#actions NetworkServicesEdgeCacheService#actions}
        :param copied_parameters: The parameters to copy from the verified token to the generated token. Only the following parameters may be copied: - 'PathGlobs' - 'paths' - 'acl' - 'URLPrefix' - 'IPRanges' - 'SessionID' - 'id' - 'Data' - 'data' - 'payload' - 'Headers' You may specify up to 6 parameters to copy. A given parameter is be copied only if the parameter exists in the verified token. Parameter names are matched exactly as specified. The order of the parameters does not matter. Duplicates are not allowed. This field may only be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#copied_parameters NetworkServicesEdgeCacheService#copied_parameters}
        :param keyset: The keyset to use for signature generation. The following are both valid paths to an EdgeCacheKeyset resource: - 'projects/project/locations/global/edgeCacheKeysets/yourKeyset' - 'yourKeyset' This must be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified. This field may not be specified otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#keyset NetworkServicesEdgeCacheService#keyset}
        :param token_query_parameter: The query parameter in which to put the generated token. If not specified, defaults to 'edge-cache-token'. If specified, the name must be 1-64 characters long and match the regular expression '`a-zA-Z <%5Ba-zA-Z0-9_-%5D>`_*' which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. This field may only be set when the GENERATE_TOKEN_HLS_COOKIELESS or PROPAGATE_TOKEN_HLS_COOKIELESS actions are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#token_query_parameter NetworkServicesEdgeCacheService#token_query_parameter}
        :param token_ttl: The duration the token is valid starting from the moment the token is first generated. Defaults to '86400s' (1 day). The TTL must be >= 0 and <= 604,800 seconds (1 week). This field may only be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#token_ttl NetworkServicesEdgeCacheService#token_ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b980123062746615f13eb149865e6f34cc0f70820ed2f8820d3756f701b476a)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument copied_parameters", value=copied_parameters, expected_type=type_hints["copied_parameters"])
            check_type(argname="argument keyset", value=keyset, expected_type=type_hints["keyset"])
            check_type(argname="argument token_query_parameter", value=token_query_parameter, expected_type=type_hints["token_query_parameter"])
            check_type(argname="argument token_ttl", value=token_ttl, expected_type=type_hints["token_ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
        }
        if copied_parameters is not None:
            self._values["copied_parameters"] = copied_parameters
        if keyset is not None:
            self._values["keyset"] = keyset
        if token_query_parameter is not None:
            self._values["token_query_parameter"] = token_query_parameter
        if token_ttl is not None:
            self._values["token_ttl"] = token_ttl

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''The actions to take to add signatures to responses. Possible values: ["GENERATE_COOKIE", "GENERATE_TOKEN_HLS_COOKIELESS", "PROPAGATE_TOKEN_HLS_COOKIELESS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#actions NetworkServicesEdgeCacheService#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def copied_parameters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The parameters to copy from the verified token to the generated token.

        Only the following parameters may be copied:

        - 'PathGlobs'
        - 'paths'
        - 'acl'
        - 'URLPrefix'
        - 'IPRanges'
        - 'SessionID'
        - 'id'
        - 'Data'
        - 'data'
        - 'payload'
        - 'Headers'

        You may specify up to 6 parameters to copy.  A given parameter is be copied only if the parameter exists in the verified token.  Parameter names are matched exactly as specified.  The order of the parameters does not matter.  Duplicates are not allowed.

        This field may only be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#copied_parameters NetworkServicesEdgeCacheService#copied_parameters}
        '''
        result = self._values.get("copied_parameters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def keyset(self) -> typing.Optional[builtins.str]:
        '''The keyset to use for signature generation.

        The following are both valid paths to an EdgeCacheKeyset resource:

        - 'projects/project/locations/global/edgeCacheKeysets/yourKeyset'
        - 'yourKeyset'

        This must be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified.  This field may not be specified otherwise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#keyset NetworkServicesEdgeCacheService#keyset}
        '''
        result = self._values.get("keyset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_query_parameter(self) -> typing.Optional[builtins.str]:
        '''The query parameter in which to put the generated token.

        If not specified, defaults to 'edge-cache-token'.

        If specified, the name must be 1-64 characters long and match the regular expression '`a-zA-Z <%5Ba-zA-Z0-9_-%5D>`_*' which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit.

        This field may only be set when the GENERATE_TOKEN_HLS_COOKIELESS or PROPAGATE_TOKEN_HLS_COOKIELESS actions are specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#token_query_parameter NetworkServicesEdgeCacheService#token_query_parameter}
        '''
        result = self._values.get("token_query_parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_ttl(self) -> typing.Optional[builtins.str]:
        '''The duration the token is valid starting from the moment the token is first generated.

        Defaults to '86400s' (1 day).

        The TTL must be >= 0 and <= 604,800 seconds (1 week).

        This field may only be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#token_ttl NetworkServicesEdgeCacheService#token_ttl}
        '''
        result = self._values.get("token_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5311a17b402cd62c5c5f6a99ae76c2f3c7684d278ef204e19dd4495162105922)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCopiedParameters")
    def reset_copied_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopiedParameters", []))

    @jsii.member(jsii_name="resetKeyset")
    def reset_keyset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyset", []))

    @jsii.member(jsii_name="resetTokenQueryParameter")
    def reset_token_query_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenQueryParameter", []))

    @jsii.member(jsii_name="resetTokenTtl")
    def reset_token_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenTtl", []))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="copiedParametersInput")
    def copied_parameters_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "copiedParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="keysetInput")
    def keyset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keysetInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenQueryParameterInput")
    def token_query_parameter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenQueryParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenTtlInput")
    def token_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125c719eb11a1b25de6302927b9353c10a4a301c9748f71c7f191befc8827238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="copiedParameters")
    def copied_parameters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "copiedParameters"))

    @copied_parameters.setter
    def copied_parameters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1027c610fb7b540146e7eece8867e24465939e42feeb199e93af67d6e2e42484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copiedParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyset")
    def keyset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyset"))

    @keyset.setter
    def keyset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860e43618b572d9afb76f32bf66eaf6bffd6f84616416485b8129febe63cb0fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenQueryParameter")
    def token_query_parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenQueryParameter"))

    @token_query_parameter.setter
    def token_query_parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c6b1b9783133bdd7ed0946769c3738cec2b470bb81a2f676e990aace2a01170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenQueryParameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenTtl")
    def token_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenTtl"))

    @token_ttl.setter
    def token_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1ab974aa5a7948e2d62f39d0c15c89d206952ad6854f045fc3fc72f1ee650b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c84defea692aabeaf70f5f9b772fff24bc71b82758749e69e24c07265b9015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "excluded_query_parameters": "excludedQueryParameters",
        "exclude_host": "excludeHost",
        "exclude_query_string": "excludeQueryString",
        "included_cookie_names": "includedCookieNames",
        "included_header_names": "includedHeaderNames",
        "included_query_parameters": "includedQueryParameters",
        "include_protocol": "includeProtocol",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy:
    def __init__(
        self,
        *,
        excluded_query_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_host: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_query_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        included_cookie_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_header_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_query_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_protocol: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param excluded_query_parameters: Names of query string parameters to exclude from cache keys. All other parameters will be included. Either specify includedQueryParameters or excludedQueryParameters, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#excluded_query_parameters NetworkServicesEdgeCacheService#excluded_query_parameters}
        :param exclude_host: If true, requests to different hosts will be cached separately. Note: this should only be enabled if hosts share the same origin and content. Removing the host from the cache key may inadvertently result in different objects being cached than intended, depending on which route the first user matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#exclude_host NetworkServicesEdgeCacheService#exclude_host}
        :param exclude_query_string: If true, exclude query string parameters from the cache key. If false (the default), include the query string parameters in the cache key according to includeQueryParameters and excludeQueryParameters. If neither includeQueryParameters nor excludeQueryParameters is set, the entire query string will be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#exclude_query_string NetworkServicesEdgeCacheService#exclude_query_string}
        :param included_cookie_names: Names of Cookies to include in cache keys. The cookie name and cookie value of each cookie named will be used as part of the cache key. Cookie names: - must be valid RFC 6265 "cookie-name" tokens - are case sensitive - cannot start with "Edge-Cache-" (case insensitive) Note that specifying several cookies, and/or cookies that have a large range of values (e.g., per-user) will dramatically impact the cache hit rate, and may result in a higher eviction rate and reduced performance. You may specify up to three cookie names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#included_cookie_names NetworkServicesEdgeCacheService#included_cookie_names}
        :param included_header_names: Names of HTTP request headers to include in cache keys. The value of the header field will be used as part of the cache key. - Header names must be valid HTTP RFC 7230 header field values. - Header field names are case insensitive - To include the HTTP method, use ":method" Note that specifying several headers, and/or headers that have a large range of values (e.g. per-user) will dramatically impact the cache hit rate, and may result in a higher eviction rate and reduced performance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#included_header_names NetworkServicesEdgeCacheService#included_header_names}
        :param included_query_parameters: Names of query string parameters to include in cache keys. All other parameters will be excluded. Either specify includedQueryParameters or excludedQueryParameters, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#included_query_parameters NetworkServicesEdgeCacheService#included_query_parameters}
        :param include_protocol: If true, http and https requests will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#include_protocol NetworkServicesEdgeCacheService#include_protocol}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7465134225dc6ae5a4c76cd85977fbdceaa20bf4ac369ebac8fc4b3639971b25)
            check_type(argname="argument excluded_query_parameters", value=excluded_query_parameters, expected_type=type_hints["excluded_query_parameters"])
            check_type(argname="argument exclude_host", value=exclude_host, expected_type=type_hints["exclude_host"])
            check_type(argname="argument exclude_query_string", value=exclude_query_string, expected_type=type_hints["exclude_query_string"])
            check_type(argname="argument included_cookie_names", value=included_cookie_names, expected_type=type_hints["included_cookie_names"])
            check_type(argname="argument included_header_names", value=included_header_names, expected_type=type_hints["included_header_names"])
            check_type(argname="argument included_query_parameters", value=included_query_parameters, expected_type=type_hints["included_query_parameters"])
            check_type(argname="argument include_protocol", value=include_protocol, expected_type=type_hints["include_protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excluded_query_parameters is not None:
            self._values["excluded_query_parameters"] = excluded_query_parameters
        if exclude_host is not None:
            self._values["exclude_host"] = exclude_host
        if exclude_query_string is not None:
            self._values["exclude_query_string"] = exclude_query_string
        if included_cookie_names is not None:
            self._values["included_cookie_names"] = included_cookie_names
        if included_header_names is not None:
            self._values["included_header_names"] = included_header_names
        if included_query_parameters is not None:
            self._values["included_query_parameters"] = included_query_parameters
        if include_protocol is not None:
            self._values["include_protocol"] = include_protocol

    @builtins.property
    def excluded_query_parameters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of query string parameters to exclude from cache keys. All other parameters will be included.

        Either specify includedQueryParameters or excludedQueryParameters, not both. '&' and '=' will be percent encoded and not treated as delimiters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#excluded_query_parameters NetworkServicesEdgeCacheService#excluded_query_parameters}
        '''
        result = self._values.get("excluded_query_parameters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclude_host(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, requests to different hosts will be cached separately.

        Note: this should only be enabled if hosts share the same origin and content. Removing the host from the cache key may inadvertently result in different objects being cached than intended, depending on which route the first user matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#exclude_host NetworkServicesEdgeCacheService#exclude_host}
        '''
        result = self._values.get("exclude_host")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclude_query_string(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, exclude query string parameters from the cache key.

        If false (the default), include the query string parameters in
        the cache key according to includeQueryParameters and
        excludeQueryParameters. If neither includeQueryParameters nor
        excludeQueryParameters is set, the entire query string will be
        included.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#exclude_query_string NetworkServicesEdgeCacheService#exclude_query_string}
        '''
        result = self._values.get("exclude_query_string")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def included_cookie_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of Cookies to include in cache keys.

        The cookie name and cookie value of each cookie named will be used as part of the cache key.

        Cookie names:

        - must be valid RFC 6265 "cookie-name" tokens
        - are case sensitive
        - cannot start with "Edge-Cache-" (case insensitive)

        Note that specifying several cookies, and/or cookies that have a large range of values (e.g., per-user) will dramatically impact the cache hit rate, and may result in a higher eviction rate and reduced performance.

        You may specify up to three cookie names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#included_cookie_names NetworkServicesEdgeCacheService#included_cookie_names}
        '''
        result = self._values.get("included_cookie_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_header_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of HTTP request headers to include in cache keys.

        The value of the header field will be used as part of the cache key.

        - Header names must be valid HTTP RFC 7230 header field values.
        - Header field names are case insensitive
        - To include the HTTP method, use ":method"

        Note that specifying several headers, and/or headers that have a large range of values (e.g. per-user) will dramatically impact the cache hit rate, and may result in a higher eviction rate and reduced performance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#included_header_names NetworkServicesEdgeCacheService#included_header_names}
        '''
        result = self._values.get("included_header_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_query_parameters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of query string parameters to include in cache keys. All other parameters will be excluded.

        Either specify includedQueryParameters or excludedQueryParameters, not both. '&' and '=' will be percent encoded and not treated as delimiters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#included_query_parameters NetworkServicesEdgeCacheService#included_query_parameters}
        '''
        result = self._values.get("included_query_parameters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, http and https requests will be cached separately.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#include_protocol NetworkServicesEdgeCacheService#include_protocol}
        '''
        result = self._values.get("include_protocol")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11f183c1f80f6043e5d84f75d482b42963bc229c5dbbb3f6664c8db78d9f17f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludedQueryParameters")
    def reset_excluded_query_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedQueryParameters", []))

    @jsii.member(jsii_name="resetExcludeHost")
    def reset_exclude_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeHost", []))

    @jsii.member(jsii_name="resetExcludeQueryString")
    def reset_exclude_query_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeQueryString", []))

    @jsii.member(jsii_name="resetIncludedCookieNames")
    def reset_included_cookie_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedCookieNames", []))

    @jsii.member(jsii_name="resetIncludedHeaderNames")
    def reset_included_header_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedHeaderNames", []))

    @jsii.member(jsii_name="resetIncludedQueryParameters")
    def reset_included_query_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedQueryParameters", []))

    @jsii.member(jsii_name="resetIncludeProtocol")
    def reset_include_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="excludedQueryParametersInput")
    def excluded_query_parameters_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedQueryParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeHostInput")
    def exclude_host_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeHostInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeQueryStringInput")
    def exclude_query_string_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeQueryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="includedCookieNamesInput")
    def included_cookie_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedCookieNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="includedHeaderNamesInput")
    def included_header_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedHeaderNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="includedQueryParametersInput")
    def included_query_parameters_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedQueryParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="includeProtocolInput")
    def include_protocol_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedQueryParameters")
    def excluded_query_parameters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedQueryParameters"))

    @excluded_query_parameters.setter
    def excluded_query_parameters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60700932dbfedc2860f2512736a48ec2e2e05bb57bbd03f5bf453e439badb45d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedQueryParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeHost")
    def exclude_host(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeHost"))

    @exclude_host.setter
    def exclude_host(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf916f377947762ee047f19f40a57dd3fc680483e4d3ed21c02c0d285a9acfab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeQueryString")
    def exclude_query_string(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeQueryString"))

    @exclude_query_string.setter
    def exclude_query_string(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d83e215ce126ab343480aed02c47436711f777952b9b108294a17a3c0e7d8cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeQueryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedCookieNames")
    def included_cookie_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedCookieNames"))

    @included_cookie_names.setter
    def included_cookie_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__110fbfb389fcd463bd523decd1531ea3d28a40c6bca465549d541682afd30797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedCookieNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedHeaderNames")
    def included_header_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedHeaderNames"))

    @included_header_names.setter
    def included_header_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1dc63e176cfef1c4b356e9de5bb5241c25fba459e044721be7b351b4b24edd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedHeaderNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedQueryParameters")
    def included_query_parameters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedQueryParameters"))

    @included_query_parameters.setter
    def included_query_parameters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0c053737e014dbbe3d1b34022f5c33f83f6a27dbc2175405696e9c133b0a83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedQueryParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeProtocol")
    def include_protocol(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeProtocol"))

    @include_protocol.setter
    def include_protocol(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9106c1bb5aff398d692bf3a9605aa6f79f3b377918c30aa78f31f4996a0a6fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a524aa55daa5d9de91c44e5e42135b4ed4a3c8c5ba42d8945c526bf068607c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cec6669d6053c357ce7d7c5f12ffa4cc51e418039ced836003225328b4283488)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAddSignatures")
    def put_add_signatures(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        copied_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
        keyset: typing.Optional[builtins.str] = None,
        token_query_parameter: typing.Optional[builtins.str] = None,
        token_ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param actions: The actions to take to add signatures to responses. Possible values: ["GENERATE_COOKIE", "GENERATE_TOKEN_HLS_COOKIELESS", "PROPAGATE_TOKEN_HLS_COOKIELESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#actions NetworkServicesEdgeCacheService#actions}
        :param copied_parameters: The parameters to copy from the verified token to the generated token. Only the following parameters may be copied: - 'PathGlobs' - 'paths' - 'acl' - 'URLPrefix' - 'IPRanges' - 'SessionID' - 'id' - 'Data' - 'data' - 'payload' - 'Headers' You may specify up to 6 parameters to copy. A given parameter is be copied only if the parameter exists in the verified token. Parameter names are matched exactly as specified. The order of the parameters does not matter. Duplicates are not allowed. This field may only be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#copied_parameters NetworkServicesEdgeCacheService#copied_parameters}
        :param keyset: The keyset to use for signature generation. The following are both valid paths to an EdgeCacheKeyset resource: - 'projects/project/locations/global/edgeCacheKeysets/yourKeyset' - 'yourKeyset' This must be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified. This field may not be specified otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#keyset NetworkServicesEdgeCacheService#keyset}
        :param token_query_parameter: The query parameter in which to put the generated token. If not specified, defaults to 'edge-cache-token'. If specified, the name must be 1-64 characters long and match the regular expression '`a-zA-Z <%5Ba-zA-Z0-9_-%5D>`_*' which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. This field may only be set when the GENERATE_TOKEN_HLS_COOKIELESS or PROPAGATE_TOKEN_HLS_COOKIELESS actions are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#token_query_parameter NetworkServicesEdgeCacheService#token_query_parameter}
        :param token_ttl: The duration the token is valid starting from the moment the token is first generated. Defaults to '86400s' (1 day). The TTL must be >= 0 and <= 604,800 seconds (1 week). This field may only be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#token_ttl NetworkServicesEdgeCacheService#token_ttl}
        '''
        value = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures(
            actions=actions,
            copied_parameters=copied_parameters,
            keyset=keyset,
            token_query_parameter=token_query_parameter,
            token_ttl=token_ttl,
        )

        return typing.cast(None, jsii.invoke(self, "putAddSignatures", [value]))

    @jsii.member(jsii_name="putCacheKeyPolicy")
    def put_cache_key_policy(
        self,
        *,
        excluded_query_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_host: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_query_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        included_cookie_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_header_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_query_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_protocol: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param excluded_query_parameters: Names of query string parameters to exclude from cache keys. All other parameters will be included. Either specify includedQueryParameters or excludedQueryParameters, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#excluded_query_parameters NetworkServicesEdgeCacheService#excluded_query_parameters}
        :param exclude_host: If true, requests to different hosts will be cached separately. Note: this should only be enabled if hosts share the same origin and content. Removing the host from the cache key may inadvertently result in different objects being cached than intended, depending on which route the first user matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#exclude_host NetworkServicesEdgeCacheService#exclude_host}
        :param exclude_query_string: If true, exclude query string parameters from the cache key. If false (the default), include the query string parameters in the cache key according to includeQueryParameters and excludeQueryParameters. If neither includeQueryParameters nor excludeQueryParameters is set, the entire query string will be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#exclude_query_string NetworkServicesEdgeCacheService#exclude_query_string}
        :param included_cookie_names: Names of Cookies to include in cache keys. The cookie name and cookie value of each cookie named will be used as part of the cache key. Cookie names: - must be valid RFC 6265 "cookie-name" tokens - are case sensitive - cannot start with "Edge-Cache-" (case insensitive) Note that specifying several cookies, and/or cookies that have a large range of values (e.g., per-user) will dramatically impact the cache hit rate, and may result in a higher eviction rate and reduced performance. You may specify up to three cookie names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#included_cookie_names NetworkServicesEdgeCacheService#included_cookie_names}
        :param included_header_names: Names of HTTP request headers to include in cache keys. The value of the header field will be used as part of the cache key. - Header names must be valid HTTP RFC 7230 header field values. - Header field names are case insensitive - To include the HTTP method, use ":method" Note that specifying several headers, and/or headers that have a large range of values (e.g. per-user) will dramatically impact the cache hit rate, and may result in a higher eviction rate and reduced performance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#included_header_names NetworkServicesEdgeCacheService#included_header_names}
        :param included_query_parameters: Names of query string parameters to include in cache keys. All other parameters will be excluded. Either specify includedQueryParameters or excludedQueryParameters, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#included_query_parameters NetworkServicesEdgeCacheService#included_query_parameters}
        :param include_protocol: If true, http and https requests will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#include_protocol NetworkServicesEdgeCacheService#include_protocol}
        '''
        value = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy(
            excluded_query_parameters=excluded_query_parameters,
            exclude_host=exclude_host,
            exclude_query_string=exclude_query_string,
            included_cookie_names=included_cookie_names,
            included_header_names=included_header_names,
            included_query_parameters=included_query_parameters,
            include_protocol=include_protocol,
        )

        return typing.cast(None, jsii.invoke(self, "putCacheKeyPolicy", [value]))

    @jsii.member(jsii_name="putSignedTokenOptions")
    def put_signed_token_options(
        self,
        *,
        allowed_signature_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        token_query_parameter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_signature_algorithms: The allowed signature algorithms to use. Defaults to using only ED25519. You may specify up to 3 signature algorithms to use. Possible values: ["ED25519", "HMAC_SHA_256", "HMAC_SHA1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allowed_signature_algorithms NetworkServicesEdgeCacheService#allowed_signature_algorithms}
        :param token_query_parameter: The query parameter in which to find the token. The name must be 1-64 characters long and match the regular expression '`a-zA-Z <%5Ba-zA-Z0-9_-%5D>`_*' which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Defaults to 'edge-cache-token'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#token_query_parameter NetworkServicesEdgeCacheService#token_query_parameter}
        '''
        value = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions(
            allowed_signature_algorithms=allowed_signature_algorithms,
            token_query_parameter=token_query_parameter,
        )

        return typing.cast(None, jsii.invoke(self, "putSignedTokenOptions", [value]))

    @jsii.member(jsii_name="resetAddSignatures")
    def reset_add_signatures(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddSignatures", []))

    @jsii.member(jsii_name="resetCacheKeyPolicy")
    def reset_cache_key_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheKeyPolicy", []))

    @jsii.member(jsii_name="resetCacheMode")
    def reset_cache_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheMode", []))

    @jsii.member(jsii_name="resetClientTtl")
    def reset_client_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientTtl", []))

    @jsii.member(jsii_name="resetDefaultTtl")
    def reset_default_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTtl", []))

    @jsii.member(jsii_name="resetMaxTtl")
    def reset_max_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxTtl", []))

    @jsii.member(jsii_name="resetNegativeCaching")
    def reset_negative_caching(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegativeCaching", []))

    @jsii.member(jsii_name="resetNegativeCachingPolicy")
    def reset_negative_caching_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegativeCachingPolicy", []))

    @jsii.member(jsii_name="resetSignedRequestKeyset")
    def reset_signed_request_keyset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignedRequestKeyset", []))

    @jsii.member(jsii_name="resetSignedRequestMaximumExpirationTtl")
    def reset_signed_request_maximum_expiration_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignedRequestMaximumExpirationTtl", []))

    @jsii.member(jsii_name="resetSignedRequestMode")
    def reset_signed_request_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignedRequestMode", []))

    @jsii.member(jsii_name="resetSignedTokenOptions")
    def reset_signed_token_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignedTokenOptions", []))

    @builtins.property
    @jsii.member(jsii_name="addSignatures")
    def add_signatures(
        self,
    ) -> NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignaturesOutputReference:
        return typing.cast(NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignaturesOutputReference, jsii.get(self, "addSignatures"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyPolicy")
    def cache_key_policy(
        self,
    ) -> NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicyOutputReference:
        return typing.cast(NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicyOutputReference, jsii.get(self, "cacheKeyPolicy"))

    @builtins.property
    @jsii.member(jsii_name="signedTokenOptions")
    def signed_token_options(
        self,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptionsOutputReference":
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptionsOutputReference", jsii.get(self, "signedTokenOptions"))

    @builtins.property
    @jsii.member(jsii_name="addSignaturesInput")
    def add_signatures_input(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures], jsii.get(self, "addSignaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyPolicyInput")
    def cache_key_policy_input(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy], jsii.get(self, "cacheKeyPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheModeInput")
    def cache_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheModeInput"))

    @builtins.property
    @jsii.member(jsii_name="clientTtlInput")
    def client_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTtlInput")
    def default_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTtlInput")
    def max_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="negativeCachingInput")
    def negative_caching_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negativeCachingInput"))

    @builtins.property
    @jsii.member(jsii_name="negativeCachingPolicyInput")
    def negative_caching_policy_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "negativeCachingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="signedRequestKeysetInput")
    def signed_request_keyset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signedRequestKeysetInput"))

    @builtins.property
    @jsii.member(jsii_name="signedRequestMaximumExpirationTtlInput")
    def signed_request_maximum_expiration_ttl_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signedRequestMaximumExpirationTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="signedRequestModeInput")
    def signed_request_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signedRequestModeInput"))

    @builtins.property
    @jsii.member(jsii_name="signedTokenOptionsInput")
    def signed_token_options_input(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions"]:
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions"], jsii.get(self, "signedTokenOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheMode")
    def cache_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheMode"))

    @cache_mode.setter
    def cache_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f5dfa75be7f1fb5300d9cf25fbb9ed5049dfd0722569c508c0a3b1444474ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTtl")
    def client_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientTtl"))

    @client_ttl.setter
    def client_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eada20514cb5d2ad5e82f937676cd726fc291e08bdb4e9a88405dead24969c31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0edc4fc2970f94ce35161392f8155570c5dbb4a213f87f3a99421fe042a1231d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTtl")
    def max_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxTtl"))

    @max_ttl.setter
    def max_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf37e598ccfb964e5bf2b9ed46a2db1611a1f3f6b21f9227f4d3e256f4263fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negativeCaching")
    def negative_caching(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negativeCaching"))

    @negative_caching.setter
    def negative_caching(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5791c20cac217c2a1ed2fc8cf3b84ad1d0f293f47e611e7ca2e612283bdd51cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negativeCaching", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negativeCachingPolicy")
    def negative_caching_policy(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "negativeCachingPolicy"))

    @negative_caching_policy.setter
    def negative_caching_policy(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d48db6d821749ae010bc5c0754da3c38202d4fd127c0c58076f0aeceed1179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negativeCachingPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signedRequestKeyset")
    def signed_request_keyset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signedRequestKeyset"))

    @signed_request_keyset.setter
    def signed_request_keyset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e80383dd59cea648c1db1aad0ed796930a097bb628a6539c4adb5dce99e4db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signedRequestKeyset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signedRequestMaximumExpirationTtl")
    def signed_request_maximum_expiration_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signedRequestMaximumExpirationTtl"))

    @signed_request_maximum_expiration_ttl.setter
    def signed_request_maximum_expiration_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ec65091556b55bf969ea42dcc21fe2e9212036ffe5c4d56adc7581c0c41973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signedRequestMaximumExpirationTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signedRequestMode")
    def signed_request_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signedRequestMode"))

    @signed_request_mode.setter
    def signed_request_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85f857a1ff65cb9b9db6f58296a1266f1488344f5177607367c40b28b2d1e67f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signedRequestMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924bea5b689cec06e369422160139a21125c5096175dd53b4dc978c26c22583f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_signature_algorithms": "allowedSignatureAlgorithms",
        "token_query_parameter": "tokenQueryParameter",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions:
    def __init__(
        self,
        *,
        allowed_signature_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        token_query_parameter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_signature_algorithms: The allowed signature algorithms to use. Defaults to using only ED25519. You may specify up to 3 signature algorithms to use. Possible values: ["ED25519", "HMAC_SHA_256", "HMAC_SHA1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allowed_signature_algorithms NetworkServicesEdgeCacheService#allowed_signature_algorithms}
        :param token_query_parameter: The query parameter in which to find the token. The name must be 1-64 characters long and match the regular expression '`a-zA-Z <%5Ba-zA-Z0-9_-%5D>`_*' which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Defaults to 'edge-cache-token'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#token_query_parameter NetworkServicesEdgeCacheService#token_query_parameter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e6f74096f703c33ee1e1b0638ae2b556dc155eafa36b4c464f376654e61b1f)
            check_type(argname="argument allowed_signature_algorithms", value=allowed_signature_algorithms, expected_type=type_hints["allowed_signature_algorithms"])
            check_type(argname="argument token_query_parameter", value=token_query_parameter, expected_type=type_hints["token_query_parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_signature_algorithms is not None:
            self._values["allowed_signature_algorithms"] = allowed_signature_algorithms
        if token_query_parameter is not None:
            self._values["token_query_parameter"] = token_query_parameter

    @builtins.property
    def allowed_signature_algorithms(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The allowed signature algorithms to use.

        Defaults to using only ED25519.

        You may specify up to 3 signature algorithms to use. Possible values: ["ED25519", "HMAC_SHA_256", "HMAC_SHA1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allowed_signature_algorithms NetworkServicesEdgeCacheService#allowed_signature_algorithms}
        '''
        result = self._values.get("allowed_signature_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def token_query_parameter(self) -> typing.Optional[builtins.str]:
        '''The query parameter in which to find the token.

        The name must be 1-64 characters long and match the regular expression '`a-zA-Z <%5Ba-zA-Z0-9_-%5D>`_*' which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit.

        Defaults to 'edge-cache-token'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#token_query_parameter NetworkServicesEdgeCacheService#token_query_parameter}
        '''
        result = self._values.get("token_query_parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23d32a9ced718192e3c405b79a857539432967cc5c0722a91c9209a477ba45d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedSignatureAlgorithms")
    def reset_allowed_signature_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedSignatureAlgorithms", []))

    @jsii.member(jsii_name="resetTokenQueryParameter")
    def reset_token_query_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenQueryParameter", []))

    @builtins.property
    @jsii.member(jsii_name="allowedSignatureAlgorithmsInput")
    def allowed_signature_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedSignatureAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenQueryParameterInput")
    def token_query_parameter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenQueryParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedSignatureAlgorithms")
    def allowed_signature_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedSignatureAlgorithms"))

    @allowed_signature_algorithms.setter
    def allowed_signature_algorithms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b840933fd3b43f2b15d053e1acb8907041c25570fd4989f1d3f465ce7d7321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedSignatureAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenQueryParameter")
    def token_query_parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenQueryParameter"))

    @token_query_parameter.setter
    def token_query_parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918eaacae1037cca0fc9edf73a8a02ebe890fcab8ea184038e5def9eb6514b23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenQueryParameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1687147fa516a258dac15342140f7a046bb09f6fac3a876df6f1f14aafca9919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_age": "maxAge",
        "allow_credentials": "allowCredentials",
        "allow_headers": "allowHeaders",
        "allow_methods": "allowMethods",
        "allow_origins": "allowOrigins",
        "disabled": "disabled",
        "expose_headers": "exposeHeaders",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy:
    def __init__(
        self,
        *,
        max_age: builtins.str,
        allow_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param max_age: Specifies how long results of a preflight request can be cached by a client in seconds. Note that many browser clients enforce a maximum TTL of 600s (10 minutes). - Setting the value to -1 forces a pre-flight check for all requests (not recommended) - A maximum TTL of 86400s can be set, but note that (as above) some clients may force pre-flight checks at a more regular interval. - This translates to the Access-Control-Max-Age header. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#max_age NetworkServicesEdgeCacheService#max_age}
        :param allow_credentials: In response to a preflight request, setting this to true indicates that the actual request can include user credentials. This translates to the Access-Control-Allow-Credentials response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allow_credentials NetworkServicesEdgeCacheService#allow_credentials}
        :param allow_headers: Specifies the content for the Access-Control-Allow-Headers response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allow_headers NetworkServicesEdgeCacheService#allow_headers}
        :param allow_methods: Specifies the content for the Access-Control-Allow-Methods response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allow_methods NetworkServicesEdgeCacheService#allow_methods}
        :param allow_origins: Specifies the list of origins that will be allowed to do CORS requests. This translates to the Access-Control-Allow-Origin response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allow_origins NetworkServicesEdgeCacheService#allow_origins}
        :param disabled: If true, specifies the CORS policy is disabled. The default value is false, which indicates that the CORS policy is in effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#disabled NetworkServicesEdgeCacheService#disabled}
        :param expose_headers: Specifies the content for the Access-Control-Allow-Headers response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#expose_headers NetworkServicesEdgeCacheService#expose_headers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b155d7ab658aa4d8423bc492385f7fd2917a35f27d944099032de9e32a1e591)
            check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
            check_type(argname="argument allow_credentials", value=allow_credentials, expected_type=type_hints["allow_credentials"])
            check_type(argname="argument allow_headers", value=allow_headers, expected_type=type_hints["allow_headers"])
            check_type(argname="argument allow_methods", value=allow_methods, expected_type=type_hints["allow_methods"])
            check_type(argname="argument allow_origins", value=allow_origins, expected_type=type_hints["allow_origins"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument expose_headers", value=expose_headers, expected_type=type_hints["expose_headers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_age": max_age,
        }
        if allow_credentials is not None:
            self._values["allow_credentials"] = allow_credentials
        if allow_headers is not None:
            self._values["allow_headers"] = allow_headers
        if allow_methods is not None:
            self._values["allow_methods"] = allow_methods
        if allow_origins is not None:
            self._values["allow_origins"] = allow_origins
        if disabled is not None:
            self._values["disabled"] = disabled
        if expose_headers is not None:
            self._values["expose_headers"] = expose_headers

    @builtins.property
    def max_age(self) -> builtins.str:
        '''Specifies how long results of a preflight request can be cached by a client in seconds.

        Note that many browser clients enforce a maximum TTL of 600s (10 minutes).

        - Setting the value to -1 forces a pre-flight check for all requests (not recommended)
        - A maximum TTL of 86400s can be set, but note that (as above) some clients may force pre-flight checks at a more regular interval.
        - This translates to the Access-Control-Max-Age header.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#max_age NetworkServicesEdgeCacheService#max_age}
        '''
        result = self._values.get("max_age")
        assert result is not None, "Required property 'max_age' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''In response to a preflight request, setting this to true indicates that the actual request can include user credentials.

        This translates to the Access-Control-Allow-Credentials response header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allow_credentials NetworkServicesEdgeCacheService#allow_credentials}
        '''
        result = self._values.get("allow_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the content for the Access-Control-Allow-Headers response header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allow_headers NetworkServicesEdgeCacheService#allow_headers}
        '''
        result = self._values.get("allow_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the content for the Access-Control-Allow-Methods response header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allow_methods NetworkServicesEdgeCacheService#allow_methods}
        '''
        result = self._values.get("allow_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of origins that will be allowed to do CORS requests.

        This translates to the Access-Control-Allow-Origin response header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allow_origins NetworkServicesEdgeCacheService#allow_origins}
        '''
        result = self._values.get("allow_origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, specifies the CORS policy is disabled.

        The default value is false, which indicates that the CORS policy is in effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#disabled NetworkServicesEdgeCacheService#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the content for the Access-Control-Allow-Headers response header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#expose_headers NetworkServicesEdgeCacheService#expose_headers}
        '''
        result = self._values.get("expose_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7775b64c62adedcb3e20f511f57e9bb9eaa24012913633052f2654d62a8b96fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowCredentials")
    def reset_allow_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowCredentials", []))

    @jsii.member(jsii_name="resetAllowHeaders")
    def reset_allow_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowHeaders", []))

    @jsii.member(jsii_name="resetAllowMethods")
    def reset_allow_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowMethods", []))

    @jsii.member(jsii_name="resetAllowOrigins")
    def reset_allow_origins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowOrigins", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetExposeHeaders")
    def reset_expose_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExposeHeaders", []))

    @builtins.property
    @jsii.member(jsii_name="allowCredentialsInput")
    def allow_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowHeadersInput")
    def allow_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowMethodsInput")
    def allow_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowOriginsInput")
    def allow_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="exposeHeadersInput")
    def expose_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exposeHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeInput")
    def max_age_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowCredentials")
    def allow_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowCredentials"))

    @allow_credentials.setter
    def allow_credentials(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb89dcd2a06918f42c872e3c088e85d40f3180c51c310a78d052ba72dcd4693b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowHeaders")
    def allow_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowHeaders"))

    @allow_headers.setter
    def allow_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b747afd00a73ff213acf0380ed6f5561ce9cf07d2226b73379d2c9360ac783e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowMethods")
    def allow_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowMethods"))

    @allow_methods.setter
    def allow_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b95324d8e4a00d54b514572e8d64e2d65ab3c784da22b39e16e647ffc522a5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowOrigins")
    def allow_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowOrigins"))

    @allow_origins.setter
    def allow_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8890509a03589831c6ba1fdd3cf7f67bd6b4064010e2aa05cde5f39ee777e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59bca629e664e4a3c09383f68db7303d7d9f4464d4aabfff7d99c1b769b8df78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposeHeaders")
    def expose_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exposeHeaders"))

    @expose_headers.setter
    def expose_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe5c0924436b1079d7d1b98475ebec0c37e0327d887e02b3d30cc5c37aaaed1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposeHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAge")
    def max_age(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxAge"))

    @max_age.setter
    def max_age(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0b1b5c3361f35bd75fe6f36c3cd1eee7ff6a7f1bef02bbc3fe6dcb5e898542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666a715fbfec89c0ff7841239bccafa231af1f0234e11523ffd0859f839a4891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7caa2abb664b8edc2964c24d586835d16aba580fd837d060f672f6c02c8569f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCdnPolicy")
    def put_cdn_policy(
        self,
        *,
        add_signatures: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures, typing.Dict[builtins.str, typing.Any]]] = None,
        cache_key_policy: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[builtins.str] = None,
        default_ttl: typing.Optional[builtins.str] = None,
        max_ttl: typing.Optional[builtins.str] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        signed_request_keyset: typing.Optional[builtins.str] = None,
        signed_request_maximum_expiration_ttl: typing.Optional[builtins.str] = None,
        signed_request_mode: typing.Optional[builtins.str] = None,
        signed_token_options: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param add_signatures: add_signatures block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#add_signatures NetworkServicesEdgeCacheService#add_signatures}
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#cache_key_policy NetworkServicesEdgeCacheService#cache_key_policy}
        :param cache_mode: Cache modes allow users to control the behaviour of the cache, what content it should cache automatically, whether to respect origin headers, or whether to unconditionally cache all responses. For all cache modes, Cache-Control headers will be passed to the client. Use clientTtl to override what is sent to the client. Possible values: ["CACHE_ALL_STATIC", "USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "BYPASS_CACHE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#cache_mode NetworkServicesEdgeCacheService#cache_mode}
        :param client_ttl: Specifies a separate client (e.g. browser client) TTL, separate from the TTL used by the edge caches. Leaving this empty will use the same cache TTL for both the CDN and the client-facing response. - The TTL must be > 0 and <= 86400s (1 day) - The clientTtl cannot be larger than the defaultTtl (if set) - Fractions of a second are not allowed. Omit this field to use the defaultTtl, or the max-age set by the origin, as the client-facing TTL. When the cache mode is set to "USE_ORIGIN_HEADERS" or "BYPASS_CACHE", you must omit this field. A duration in seconds terminated by 's'. Example: "3s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#client_ttl NetworkServicesEdgeCacheService#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). Defaults to 3600s (1 hour). - The TTL must be >= 0 and <= 31,536,000 seconds (1 year) - Setting a TTL of "0" means "always revalidate" (equivalent to must-revalidate) - The value of defaultTTL cannot be set to a value greater than that of maxTTL. - Fractions of a second are not allowed. - When the cacheMode is set to FORCE_CACHE_ALL, the defaultTTL will overwrite the TTL set in all responses. Note that infrequently accessed objects may be evicted from the cache before the defined TTL. Objects that expire will be revalidated with the origin. When the cache mode is set to "USE_ORIGIN_HEADERS" or "BYPASS_CACHE", you must omit this field. A duration in seconds terminated by 's'. Example: "3s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#default_ttl NetworkServicesEdgeCacheService#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Defaults to 86400s (1 day). Cache directives that attempt to set a max-age or s-maxage higher than this, or an Expires header more than maxTtl seconds in the future will be capped at the value of maxTTL, as if it were the value of an s-maxage Cache-Control directive. - The TTL must be >= 0 and <= 31,536,000 seconds (1 year) - Setting a TTL of "0" means "always revalidate" - The value of maxTtl must be equal to or greater than defaultTtl. - Fractions of a second are not allowed. When the cache mode is set to "USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", or "BYPASS_CACHE", you must omit this field. A duration in seconds terminated by 's'. Example: "3s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#max_ttl NetworkServicesEdgeCacheService#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. This can reduce the load on your origin and improve end-user experience by reducing response latency. By default, the CDNPolicy will apply the following default TTLs to these status codes: - HTTP 300 (Multiple Choice), 301, 308 (Permanent Redirects): 10m - HTTP 404 (Not Found), 410 (Gone), 451 (Unavailable For Legal Reasons): 120s - HTTP 405 (Method Not Found), 414 (URI Too Long), 501 (Not Implemented): 60s These defaults can be overridden in negativeCachingPolicy Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#negative_caching NetworkServicesEdgeCacheService#negative_caching}
        :param negative_caching_policy: Sets a cache TTL for the specified HTTP status code. negativeCaching must be enabled to configure negativeCachingPolicy. - Omitting the policy and leaving negativeCaching enabled will use the default TTLs for each status code, defined in negativeCaching. - TTLs must be >= 0 (where 0 is "always revalidate") and <= 86400s (1 day) Note that when specifying an explicit negativeCachingPolicy, you should take care to specify a cache TTL for all response codes that you wish to cache. The CDNPolicy will not apply any default negative caching when a policy exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#negative_caching_policy NetworkServicesEdgeCacheService#negative_caching_policy}
        :param signed_request_keyset: The EdgeCacheKeyset containing the set of public keys used to validate signed requests at the edge. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#signed_request_keyset NetworkServicesEdgeCacheService#signed_request_keyset}
        :param signed_request_maximum_expiration_ttl: Limit how far into the future the expiration time of a signed request may be. When set, a signed request is rejected if its expiration time is later than now + signedRequestMaximumExpirationTtl, where now is the time at which the signed request is first handled by the CDN. - The TTL must be > 0. - Fractions of a second are not allowed. By default, signedRequestMaximumExpirationTtl is not set and the expiration time of a signed request may be arbitrarily far into future. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#signed_request_maximum_expiration_ttl NetworkServicesEdgeCacheService#signed_request_maximum_expiration_ttl}
        :param signed_request_mode: Whether to enforce signed requests. The default value is DISABLED, which means all content is public, and does not authorize access. You must also set a signedRequestKeyset to enable signed requests. When set to REQUIRE_SIGNATURES, all matching requests will have their signature validated. Requests that were not signed with the corresponding private key, or that are otherwise invalid (expired, do not match the signature, IP address, or header) will be rejected with a HTTP 403 and (if enabled) logged. Possible values: ["DISABLED", "REQUIRE_SIGNATURES", "REQUIRE_TOKENS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#signed_request_mode NetworkServicesEdgeCacheService#signed_request_mode}
        :param signed_token_options: signed_token_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#signed_token_options NetworkServicesEdgeCacheService#signed_token_options}
        '''
        value = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy(
            add_signatures=add_signatures,
            cache_key_policy=cache_key_policy,
            cache_mode=cache_mode,
            client_ttl=client_ttl,
            default_ttl=default_ttl,
            max_ttl=max_ttl,
            negative_caching=negative_caching,
            negative_caching_policy=negative_caching_policy,
            signed_request_keyset=signed_request_keyset,
            signed_request_maximum_expiration_ttl=signed_request_maximum_expiration_ttl,
            signed_request_mode=signed_request_mode,
            signed_token_options=signed_token_options,
        )

        return typing.cast(None, jsii.invoke(self, "putCdnPolicy", [value]))

    @jsii.member(jsii_name="putCorsPolicy")
    def put_cors_policy(
        self,
        *,
        max_age: builtins.str,
        allow_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param max_age: Specifies how long results of a preflight request can be cached by a client in seconds. Note that many browser clients enforce a maximum TTL of 600s (10 minutes). - Setting the value to -1 forces a pre-flight check for all requests (not recommended) - A maximum TTL of 86400s can be set, but note that (as above) some clients may force pre-flight checks at a more regular interval. - This translates to the Access-Control-Max-Age header. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#max_age NetworkServicesEdgeCacheService#max_age}
        :param allow_credentials: In response to a preflight request, setting this to true indicates that the actual request can include user credentials. This translates to the Access-Control-Allow-Credentials response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allow_credentials NetworkServicesEdgeCacheService#allow_credentials}
        :param allow_headers: Specifies the content for the Access-Control-Allow-Headers response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allow_headers NetworkServicesEdgeCacheService#allow_headers}
        :param allow_methods: Specifies the content for the Access-Control-Allow-Methods response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allow_methods NetworkServicesEdgeCacheService#allow_methods}
        :param allow_origins: Specifies the list of origins that will be allowed to do CORS requests. This translates to the Access-Control-Allow-Origin response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allow_origins NetworkServicesEdgeCacheService#allow_origins}
        :param disabled: If true, specifies the CORS policy is disabled. The default value is false, which indicates that the CORS policy is in effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#disabled NetworkServicesEdgeCacheService#disabled}
        :param expose_headers: Specifies the content for the Access-Control-Allow-Headers response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#expose_headers NetworkServicesEdgeCacheService#expose_headers}
        '''
        value = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy(
            max_age=max_age,
            allow_credentials=allow_credentials,
            allow_headers=allow_headers,
            allow_methods=allow_methods,
            allow_origins=allow_origins,
            disabled=disabled,
            expose_headers=expose_headers,
        )

        return typing.cast(None, jsii.invoke(self, "putCorsPolicy", [value]))

    @jsii.member(jsii_name="putUrlRewrite")
    def put_url_rewrite(
        self,
        *,
        host_rewrite: typing.Optional[builtins.str] = None,
        path_prefix_rewrite: typing.Optional[builtins.str] = None,
        path_template_rewrite: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_rewrite: Prior to forwarding the request to the selected origin, the request's host header is replaced with contents of hostRewrite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#host_rewrite NetworkServicesEdgeCacheService#host_rewrite}
        :param path_prefix_rewrite: Prior to forwarding the request to the selected origin, the matching portion of the request's path is replaced by pathPrefixRewrite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_prefix_rewrite NetworkServicesEdgeCacheService#path_prefix_rewrite}
        :param path_template_rewrite: Prior to forwarding the request to the selected origin, if the request matched a pathTemplateMatch, the matching portion of the request's path is replaced re-written using the pattern specified by pathTemplateRewrite. pathTemplateRewrite must be between 1 and 255 characters (inclusive), must start with a '/', and must only use variables captured by the route's pathTemplate matchers. pathTemplateRewrite may only be used when all of a route's MatchRules specify pathTemplate. Only one of pathPrefixRewrite and pathTemplateRewrite may be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_template_rewrite NetworkServicesEdgeCacheService#path_template_rewrite}
        '''
        value = NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite(
            host_rewrite=host_rewrite,
            path_prefix_rewrite=path_prefix_rewrite,
            path_template_rewrite=path_template_rewrite,
        )

        return typing.cast(None, jsii.invoke(self, "putUrlRewrite", [value]))

    @jsii.member(jsii_name="resetCdnPolicy")
    def reset_cdn_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCdnPolicy", []))

    @jsii.member(jsii_name="resetCompressionMode")
    def reset_compression_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompressionMode", []))

    @jsii.member(jsii_name="resetCorsPolicy")
    def reset_cors_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsPolicy", []))

    @jsii.member(jsii_name="resetUrlRewrite")
    def reset_url_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlRewrite", []))

    @builtins.property
    @jsii.member(jsii_name="cdnPolicy")
    def cdn_policy(
        self,
    ) -> NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyOutputReference:
        return typing.cast(NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyOutputReference, jsii.get(self, "cdnPolicy"))

    @builtins.property
    @jsii.member(jsii_name="corsPolicy")
    def cors_policy(
        self,
    ) -> NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicyOutputReference:
        return typing.cast(NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicyOutputReference, jsii.get(self, "corsPolicy"))

    @builtins.property
    @jsii.member(jsii_name="urlRewrite")
    def url_rewrite(
        self,
    ) -> "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewriteOutputReference":
        return typing.cast("NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewriteOutputReference", jsii.get(self, "urlRewrite"))

    @builtins.property
    @jsii.member(jsii_name="cdnPolicyInput")
    def cdn_policy_input(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy], jsii.get(self, "cdnPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionModeInput")
    def compression_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="corsPolicyInput")
    def cors_policy_input(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy], jsii.get(self, "corsPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRewriteInput")
    def url_rewrite_input(
        self,
    ) -> typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite"]:
        return typing.cast(typing.Optional["NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite"], jsii.get(self, "urlRewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionMode")
    def compression_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionMode"))

    @compression_mode.setter
    def compression_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__991a33020792ee25d2ab68b288ace98e0d4f10a5937724c62ab2201b5d427840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e242b96c6eeb95a162fc34c0b50e6cb15376523f50f270407cb6dfb121c16365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite",
    jsii_struct_bases=[],
    name_mapping={
        "host_rewrite": "hostRewrite",
        "path_prefix_rewrite": "pathPrefixRewrite",
        "path_template_rewrite": "pathTemplateRewrite",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite:
    def __init__(
        self,
        *,
        host_rewrite: typing.Optional[builtins.str] = None,
        path_prefix_rewrite: typing.Optional[builtins.str] = None,
        path_template_rewrite: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_rewrite: Prior to forwarding the request to the selected origin, the request's host header is replaced with contents of hostRewrite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#host_rewrite NetworkServicesEdgeCacheService#host_rewrite}
        :param path_prefix_rewrite: Prior to forwarding the request to the selected origin, the matching portion of the request's path is replaced by pathPrefixRewrite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_prefix_rewrite NetworkServicesEdgeCacheService#path_prefix_rewrite}
        :param path_template_rewrite: Prior to forwarding the request to the selected origin, if the request matched a pathTemplateMatch, the matching portion of the request's path is replaced re-written using the pattern specified by pathTemplateRewrite. pathTemplateRewrite must be between 1 and 255 characters (inclusive), must start with a '/', and must only use variables captured by the route's pathTemplate matchers. pathTemplateRewrite may only be used when all of a route's MatchRules specify pathTemplate. Only one of pathPrefixRewrite and pathTemplateRewrite may be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_template_rewrite NetworkServicesEdgeCacheService#path_template_rewrite}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9bfe01e62ccc1fadee57a8dd32925175a2c93bf2a0cf411de81af08e3ada39c)
            check_type(argname="argument host_rewrite", value=host_rewrite, expected_type=type_hints["host_rewrite"])
            check_type(argname="argument path_prefix_rewrite", value=path_prefix_rewrite, expected_type=type_hints["path_prefix_rewrite"])
            check_type(argname="argument path_template_rewrite", value=path_template_rewrite, expected_type=type_hints["path_template_rewrite"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host_rewrite is not None:
            self._values["host_rewrite"] = host_rewrite
        if path_prefix_rewrite is not None:
            self._values["path_prefix_rewrite"] = path_prefix_rewrite
        if path_template_rewrite is not None:
            self._values["path_template_rewrite"] = path_template_rewrite

    @builtins.property
    def host_rewrite(self) -> typing.Optional[builtins.str]:
        '''Prior to forwarding the request to the selected origin, the request's host header is replaced with contents of hostRewrite.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#host_rewrite NetworkServicesEdgeCacheService#host_rewrite}
        '''
        result = self._values.get("host_rewrite")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_prefix_rewrite(self) -> typing.Optional[builtins.str]:
        '''Prior to forwarding the request to the selected origin, the matching portion of the request's path is replaced by pathPrefixRewrite.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_prefix_rewrite NetworkServicesEdgeCacheService#path_prefix_rewrite}
        '''
        result = self._values.get("path_prefix_rewrite")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_template_rewrite(self) -> typing.Optional[builtins.str]:
        '''Prior to forwarding the request to the selected origin, if the request matched a pathTemplateMatch, the matching portion of the request's path is replaced re-written using the pattern specified by pathTemplateRewrite.

        pathTemplateRewrite must be between 1 and 255 characters
        (inclusive), must start with a '/', and must only use variables
        captured by the route's pathTemplate matchers.

        pathTemplateRewrite may only be used when all of a route's
        MatchRules specify pathTemplate.

        Only one of pathPrefixRewrite and pathTemplateRewrite may be
        specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_template_rewrite NetworkServicesEdgeCacheService#path_template_rewrite}
        '''
        result = self._values.get("path_template_rewrite")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewriteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewriteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60759fc4b2b2b9f14306abdd17d11d26f33e6e917bce6faccfd4944124af7662)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHostRewrite")
    def reset_host_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostRewrite", []))

    @jsii.member(jsii_name="resetPathPrefixRewrite")
    def reset_path_prefix_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathPrefixRewrite", []))

    @jsii.member(jsii_name="resetPathTemplateRewrite")
    def reset_path_template_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathTemplateRewrite", []))

    @builtins.property
    @jsii.member(jsii_name="hostRewriteInput")
    def host_rewrite_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostRewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="pathPrefixRewriteInput")
    def path_prefix_rewrite_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathPrefixRewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="pathTemplateRewriteInput")
    def path_template_rewrite_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathTemplateRewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="hostRewrite")
    def host_rewrite(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostRewrite"))

    @host_rewrite.setter
    def host_rewrite(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d1becfdf28608f6e71d4ee8a1d184013cd38b27a092049362bc6f43dc0cd2a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathPrefixRewrite")
    def path_prefix_rewrite(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathPrefixRewrite"))

    @path_prefix_rewrite.setter
    def path_prefix_rewrite(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78189461605ea44afd0037eb368aee5cf762cfd674f61bd23fa799e8e38e848c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathPrefixRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathTemplateRewrite")
    def path_template_rewrite(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathTemplateRewrite"))

    @path_template_rewrite.setter
    def path_template_rewrite(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f0ca805690aae5c6231771e84e47ce62828cabf3c3a29164d8a39069bd268d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathTemplateRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab05f57fc4de779db26d895370c2075df8267887b7a64c36c1a896dd1488e3b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods",
    jsii_struct_bases=[],
    name_mapping={"allowed_methods": "allowedMethods"},
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods:
    def __init__(
        self,
        *,
        allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_methods: The non-empty set of HTTP methods that are allowed for this route. Any combination of "GET", "HEAD", "OPTIONS", "PUT", "POST", "DELETE", and "PATCH". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allowed_methods NetworkServicesEdgeCacheService#allowed_methods}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73cc32bfc701a35c41386e6d3abe2ff7623de6f3141a4845151c4c6932a6b400)
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods

    @builtins.property
    def allowed_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The non-empty set of HTTP methods that are allowed for this route.

        Any combination of "GET", "HEAD", "OPTIONS", "PUT", "POST", "DELETE", and "PATCH".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#allowed_methods NetworkServicesEdgeCacheService#allowed_methods}
        '''
        result = self._values.get("allowed_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethodsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethodsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2abd1501f3271312808692b79bd6ca93eb7a91afbb813eab57b8170ab7882fc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedMethods")
    def reset_allowed_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedMethods", []))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1b019be864c4eda2ca33c82925e7b5cc61d772b844e6dc7f9f048d854b0402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3290fa97e21c76012e16b440c4bbf42ce892b6844afb8d91c4c633244cc14f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect",
    jsii_struct_bases=[],
    name_mapping={
        "host_redirect": "hostRedirect",
        "https_redirect": "httpsRedirect",
        "path_redirect": "pathRedirect",
        "prefix_redirect": "prefixRedirect",
        "redirect_response_code": "redirectResponseCode",
        "strip_query": "stripQuery",
    },
)
class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect:
    def __init__(
        self,
        *,
        host_redirect: typing.Optional[builtins.str] = None,
        https_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path_redirect: typing.Optional[builtins.str] = None,
        prefix_redirect: typing.Optional[builtins.str] = None,
        redirect_response_code: typing.Optional[builtins.str] = None,
        strip_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param host_redirect: The host that will be used in the redirect response instead of the one that was supplied in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#host_redirect NetworkServicesEdgeCacheService#host_redirect}
        :param https_redirect: If set to true, the URL scheme in the redirected request is set to https. If set to false, the URL scheme of the redirected request will remain the same as that of the request. This can only be set if there is at least one (1) edgeSslCertificate set on the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#https_redirect NetworkServicesEdgeCacheService#https_redirect}
        :param path_redirect: The path that will be used in the redirect response instead of the one that was supplied in the request. pathRedirect cannot be supplied together with prefixRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect. The path value must be between 1 and 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_redirect NetworkServicesEdgeCacheService#path_redirect}
        :param prefix_redirect: The prefix that replaces the prefixMatch specified in the routeRule, retaining the remaining portion of the URL before redirecting the request. prefixRedirect cannot be supplied together with pathRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#prefix_redirect NetworkServicesEdgeCacheService#prefix_redirect}
        :param redirect_response_code: The HTTP Status code to use for this RedirectAction. The supported values are: - 'MOVED_PERMANENTLY_DEFAULT', which is the default value and corresponds to 301. - 'FOUND', which corresponds to 302. - 'SEE_OTHER' which corresponds to 303. - 'TEMPORARY_REDIRECT', which corresponds to 307. in this case, the request method will be retained. - 'PERMANENT_REDIRECT', which corresponds to 308. in this case, the request method will be retained. Possible values: ["MOVED_PERMANENTLY_DEFAULT", "FOUND", "SEE_OTHER", "TEMPORARY_REDIRECT", "PERMANENT_REDIRECT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#redirect_response_code NetworkServicesEdgeCacheService#redirect_response_code}
        :param strip_query: If set to true, any accompanying query portion of the original URL is removed prior to redirecting the request. If set to false, the query portion of the original URL is retained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#strip_query NetworkServicesEdgeCacheService#strip_query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb22338bd293a412862dfd078500520266a9c778b7d29180388003b2eb26b7b)
            check_type(argname="argument host_redirect", value=host_redirect, expected_type=type_hints["host_redirect"])
            check_type(argname="argument https_redirect", value=https_redirect, expected_type=type_hints["https_redirect"])
            check_type(argname="argument path_redirect", value=path_redirect, expected_type=type_hints["path_redirect"])
            check_type(argname="argument prefix_redirect", value=prefix_redirect, expected_type=type_hints["prefix_redirect"])
            check_type(argname="argument redirect_response_code", value=redirect_response_code, expected_type=type_hints["redirect_response_code"])
            check_type(argname="argument strip_query", value=strip_query, expected_type=type_hints["strip_query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host_redirect is not None:
            self._values["host_redirect"] = host_redirect
        if https_redirect is not None:
            self._values["https_redirect"] = https_redirect
        if path_redirect is not None:
            self._values["path_redirect"] = path_redirect
        if prefix_redirect is not None:
            self._values["prefix_redirect"] = prefix_redirect
        if redirect_response_code is not None:
            self._values["redirect_response_code"] = redirect_response_code
        if strip_query is not None:
            self._values["strip_query"] = strip_query

    @builtins.property
    def host_redirect(self) -> typing.Optional[builtins.str]:
        '''The host that will be used in the redirect response instead of the one that was supplied in the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#host_redirect NetworkServicesEdgeCacheService#host_redirect}
        '''
        result = self._values.get("host_redirect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_redirect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the URL scheme in the redirected request is set to https.

        If set to false, the URL scheme of the redirected request will remain the same as that of the request.

        This can only be set if there is at least one (1) edgeSslCertificate set on the service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#https_redirect NetworkServicesEdgeCacheService#https_redirect}
        '''
        result = self._values.get("https_redirect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path_redirect(self) -> typing.Optional[builtins.str]:
        '''The path that will be used in the redirect response instead of the one that was supplied in the request.

        pathRedirect cannot be supplied together with prefixRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect.

        The path value must be between 1 and 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#path_redirect NetworkServicesEdgeCacheService#path_redirect}
        '''
        result = self._values.get("path_redirect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix_redirect(self) -> typing.Optional[builtins.str]:
        '''The prefix that replaces the prefixMatch specified in the routeRule, retaining the remaining portion of the URL before redirecting the request.

        prefixRedirect cannot be supplied together with pathRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#prefix_redirect NetworkServicesEdgeCacheService#prefix_redirect}
        '''
        result = self._values.get("prefix_redirect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_response_code(self) -> typing.Optional[builtins.str]:
        '''The HTTP Status code to use for this RedirectAction.

        The supported values are:

        - 'MOVED_PERMANENTLY_DEFAULT', which is the default value and corresponds to 301.
        - 'FOUND', which corresponds to 302.
        - 'SEE_OTHER' which corresponds to 303.
        - 'TEMPORARY_REDIRECT', which corresponds to 307. in this case, the request method will be retained.
        - 'PERMANENT_REDIRECT', which corresponds to 308. in this case, the request method will be retained. Possible values: ["MOVED_PERMANENTLY_DEFAULT", "FOUND", "SEE_OTHER", "TEMPORARY_REDIRECT", "PERMANENT_REDIRECT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#redirect_response_code NetworkServicesEdgeCacheService#redirect_response_code}
        '''
        result = self._values.get("redirect_response_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strip_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, any accompanying query portion of the original URL is removed prior to redirecting the request.

        If set to false, the query portion of the original URL is retained.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#strip_query NetworkServicesEdgeCacheService#strip_query}
        '''
        result = self._values.get("strip_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__843765f3f131ba6ce0210ac9ac10a5840695d68942d259892f10bc59d12a9556)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHostRedirect")
    def reset_host_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostRedirect", []))

    @jsii.member(jsii_name="resetHttpsRedirect")
    def reset_https_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsRedirect", []))

    @jsii.member(jsii_name="resetPathRedirect")
    def reset_path_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathRedirect", []))

    @jsii.member(jsii_name="resetPrefixRedirect")
    def reset_prefix_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixRedirect", []))

    @jsii.member(jsii_name="resetRedirectResponseCode")
    def reset_redirect_response_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectResponseCode", []))

    @jsii.member(jsii_name="resetStripQuery")
    def reset_strip_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStripQuery", []))

    @builtins.property
    @jsii.member(jsii_name="hostRedirectInput")
    def host_redirect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsRedirectInput")
    def https_redirect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpsRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="pathRedirectInput")
    def path_redirect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixRedirectInput")
    def prefix_redirect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectResponseCodeInput")
    def redirect_response_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectResponseCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="stripQueryInput")
    def strip_query_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stripQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="hostRedirect")
    def host_redirect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostRedirect"))

    @host_redirect.setter
    def host_redirect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a768b33b7c21e6b9196e6c441ebffae73102db72bfc2e848214eeba723ec61f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsRedirect")
    def https_redirect(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "httpsRedirect"))

    @https_redirect.setter
    def https_redirect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb0778245e2e32fc054d6d8dff6e0ad70019b84cf73a6bc536311dc5812633b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathRedirect")
    def path_redirect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathRedirect"))

    @path_redirect.setter
    def path_redirect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7811f054cf57f0262515b3c3499374ffb7bc8a6081170ec024f251be2554863c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixRedirect")
    def prefix_redirect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixRedirect"))

    @prefix_redirect.setter
    def prefix_redirect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36e02ec6611cbca4dedc9d9da53d0e91939205d2651a363b0c6bd9eabc1a4563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectResponseCode")
    def redirect_response_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectResponseCode"))

    @redirect_response_code.setter
    def redirect_response_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5bc348119acccd54dd7b2700d877dfc9c2a76d5fc5834fc6021e5b161f39d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectResponseCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stripQuery")
    def strip_query(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stripQuery"))

    @strip_query.setter
    def strip_query(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13f12ebea6717ee3ce7c7824dec038b565a117a6a752087676e66e1ee06800e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stripQuery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect]:
        return typing.cast(typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__159cf9d00e3eda47bc9d8a16c27f4af28bf152827839b3df854cc5c3a0f73545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkServicesEdgeCacheServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#create NetworkServicesEdgeCacheService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#delete NetworkServicesEdgeCacheService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#update NetworkServicesEdgeCacheService#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85239f6f8126a02d5d2193d99f72ee1bc132941d3a69dbc90954730f029091a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#create NetworkServicesEdgeCacheService#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#delete NetworkServicesEdgeCacheService#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_edge_cache_service#update NetworkServicesEdgeCacheService#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesEdgeCacheServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesEdgeCacheServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesEdgeCacheService.NetworkServicesEdgeCacheServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22d157b26705d4850dbbb34c16059656c4518970ccc6465f84564fa37da8f646)
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
            type_hints = typing.get_type_hints(_typecheckingstub__758cf784de29c87634f260abc39c7411c5edc3d4bb53d687f438de066b09fd9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b79c0292e165293db04857b959c68bff4c8b44ab4a0fbe594735ca8257801ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92071a9e02d8ce39861ae898ae6776c5151d99088231b1d862097d8d8ad09240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0041fd28813a1fbb4eb7d520e80d54c007d9839eb93ab3b76f4b78dc70e0610f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkServicesEdgeCacheService",
    "NetworkServicesEdgeCacheServiceConfig",
    "NetworkServicesEdgeCacheServiceLogConfig",
    "NetworkServicesEdgeCacheServiceLogConfigOutputReference",
    "NetworkServicesEdgeCacheServiceRouting",
    "NetworkServicesEdgeCacheServiceRoutingHostRule",
    "NetworkServicesEdgeCacheServiceRoutingHostRuleList",
    "NetworkServicesEdgeCacheServiceRoutingHostRuleOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcher",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherList",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddList",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveList",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddList",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveList",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleList",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchList",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleList",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchList",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignaturesOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicyOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptionsOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicyOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewriteOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethodsOutputReference",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect",
    "NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirectOutputReference",
    "NetworkServicesEdgeCacheServiceTimeouts",
    "NetworkServicesEdgeCacheServiceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3c189ce9f2f0edc8557df9fa311275589f2f85e6da60f36319b147ea830e81d9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    routing: typing.Union[NetworkServicesEdgeCacheServiceRouting, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    disable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_quic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    edge_security_policy: typing.Optional[builtins.str] = None,
    edge_ssl_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    log_config: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    require_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_policy: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5f0543362cf0da1418bf7e335365741313092838d0980df1fd202bc741a272a8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5237a4cd503468b2efaf9f972f8c127ee8df9aa809d7fd7dc59ef9a341dfd5c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba254a32d9b6de9b38ebfccc58bc781d21e73916cec9da1e77fc201f09625d1c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__023beb1a3ab192b7116ff0dac46fd7df2156d8309cb9f2e93f8fcf57ba24b2f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fffcab658cfac0b7ffc23826649a3c7cc14487c8595f2f163d4b301321e3cf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561b16f03147a6ca98de48312767475cb07e83a0d53ca85b8851766c4944ac07(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1b2577a2bf25ba54293bcb7bb2774ef56a47b5cbbb97e64b9ac648edc8548c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344f2211bf2bb2da43910a4d9449580e0f647251f3a5a76ea0841cc2c8bd6e6f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413ac45f174a414dbdab18e7da7923ea7727dad86851caf91a942c550804f690(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28ced80e8b06c6f05ed11cc0147e95f299a956ee23dc6c968714fb9f5e3df3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726fd79fbcbaa387f427cb90512b61b33f26bbd13c6b4fbb2ff393917b051724(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6caaef78ffa3bc830d92f958f2db8c7a4ce2b89a58735ae408ba2a117820a6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23c824d6b2fc0cc291b63f5cf85727d33edeabc5a1c053f6fe7c4d2141ca616(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    routing: typing.Union[NetworkServicesEdgeCacheServiceRouting, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    disable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_quic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    edge_security_policy: typing.Optional[builtins.str] = None,
    edge_ssl_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    log_config: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    require_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_policy: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24bf96c419c7a1aaa097e44cb87ed443ece20868a763d5a0a69409de387c0186(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sample_rate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe48a9465b864fe8b8b9c107acb35c0edfa4dbd2c470f06454d2c825703b4b36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0bc94c6b40bee41240453372594f946a03a91fe762937601d891d9e08c56f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9003533898c3b3f95c03ed3f8d2c16905677e07f081891dbedc6ad158892d2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6fbedd7e394a13bbfdf52149cc103b1175b9200ff627565d60894f788a4b63(
    value: typing.Optional[NetworkServicesEdgeCacheServiceLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99302cd2b69b5c4b19d2bb86974718dce24810545d19f5b7b1f47da3df2b4bb2(
    *,
    host_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingHostRule, typing.Dict[builtins.str, typing.Any]]]],
    path_matcher: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcher, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb772e4b0e3dc48ab8398a1f20b9067583a83d7e624bb0267617a3d115b139a(
    *,
    hosts: typing.Sequence[builtins.str],
    path_matcher: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30fd8452cf25e0479d4b9405e19d354a5a85535603cfa4091c3569d8b4e7746(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08504028ffc3d42338552313f918cb0f70be395dcc57d3050cf46a3903b5d9a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea9b488e0c33099c57f1f6081a7c60869080ad25441d6d3b7501e3111fb38d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c38ab4c63dd6a4036c7b12a8a76e1fe5d3aeecd38b3fdca81a4fe9f9a7a613e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c8e1c6c7f1cb75b2e70d539c117878a53004724bcf170e2b9093406e7a8d1b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daff4507db37c0ab1e9cec4de25ebfc7ea39cb9e59c775ff235d7b75af1e8a73(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingHostRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30bcc6e3a994d7ce342d49090809af1d9008b3ac5634c6aa5e5000f0d9910ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e7170132d67a5ecebc5100b3e7c397ccbfa8d2ee8bcf851392f026aae8f3f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7429e4bce302bb6540b92d62a6b68f3f78f7bc3ddbf64e949763adf7af1c97(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed96b080a67927aefeae2b371afea91bc963e20fc2a085d493db243909f0e84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0fd75ad3bc2a13609fe8c8a25c51c0da8afb180a2d448f22ed4ca889b25af4f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingHostRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918eedc821b777af34ff39cf0503061381a925af1049cb8c5fd90e090488e1bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00620d5a10148bcdd4a7a8b55a162be7d9cba72ad26c2ca6b9760b2c28df933(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingHostRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d0d3f33625fa80513874d18f5a13743f09be3f7ec381f9231ae150c3319efe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcher, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87218fb13ef40f678085331c7abc0a627cef52d585f6824f2a93a22273b91185(
    value: typing.Optional[NetworkServicesEdgeCacheServiceRouting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6cb0f753c4ca807820f3b9433e845e39a8921ef0b7f75377ab568ab3b94cb3(
    *,
    name: builtins.str,
    route_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517c9484327a765f87b19289ddc983ed2f250b62239101fc6f39c03f08ba7d35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e045f2a4598196d9cc896c119a724a32e18602da47ef2c822d10ca088bd36263(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e5e0f5fa893e24b00b6865938a3de257d07d1a1045faa6c5176b78291a3f048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d2f45d32e019d711959aa3a8efb951466ec660885b33c3b6da6f364e2d5231(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7171b1a46b38a8c57a64881491960a0f11b5a731053b91e947cf10b96b3926(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5974a3f6f03ce7d3cb0178ba63f11885f4ec90133feb882070685457b58b3031(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcher]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c8203c1e3cbc7dbdd2a38a21c668bd44c6658573f218a1b4577c16accdbf24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e28fda8c3477d39559f59a4175a6c399e904aa835512e8309bd57c9f9d91b16d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917026d5ff718141511c11fb32fc536ada7399fbbd9dacd170747fac9e1b2433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ef776287c8f3e39d5b73b53b562657f408387958f99065cb854fc53f563089(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7d592b542040e1613c123c94b7639ab60b1d3fd4bed4c1795cf2d9197b26e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcher]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8af122e01125ab832afd1dbb02d367da3450fb20680c135ef4e64158c598804(
    *,
    match_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule, typing.Dict[builtins.str, typing.Any]]]],
    priority: builtins.str,
    description: typing.Optional[builtins.str] = None,
    header_action: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction, typing.Dict[builtins.str, typing.Any]]] = None,
    origin: typing.Optional[builtins.str] = None,
    route_action: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction, typing.Dict[builtins.str, typing.Any]]] = None,
    route_methods: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods, typing.Dict[builtins.str, typing.Any]]] = None,
    url_redirect: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f637391c08bf429fdfc24bc064db9f4fb9b3bb4f581bd3c7a09d36f316e87d5(
    *,
    request_header_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_header_to_remove: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove, typing.Dict[builtins.str, typing.Any]]]]] = None,
    response_header_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    response_header_to_remove: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c96cae6de6c1330040b8a02933456d5bffa00e94915e114e9a6281af24e308(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f924f03ab07956fce69fd4e09e885215fe276236f74c74103f269fcd30c3506(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5b123842356c17d308c0965a305029bb6d1a5405b5499ddfe4bf081f4bf8d0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceab87f56ed76ce8dc6dd8f6dec8a8dd09938aa61dc37b318a7a96fc3802ea18(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ebd5720021cc377a54ba0ed8587f3d5a09632dc13444471c568d2268bbd1f02(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48044d073518fb41d86e18ca91ae45e745230876fbc588542c597735882c7258(
    value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a5087c3afeca67a550086289add98e04216a8d68bc295a8530f7226bc6d0e2(
    *,
    header_name: builtins.str,
    header_value: builtins.str,
    replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6e08027b2d4504d76892e2e0215a7cdb7ca8f87ab27467220d67dccdb66cbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a763d12e4ff031866f28f1714efd83d8e2ea068534de6e4b9a4d38e67c4e9c57(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd0e8fe589a5fe4cab9aaf7b3f315bbb89d3e521765ab48b80db7b8ac005c20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ce188e5107f9e2e8049716c465bbb27054b20fa810435dc008dbbd0ff99d6c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35090e3884f21106b7b8025652f4122f2224ba04c49bc092655549abc9b0381e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300c1d28d9e6d68966475112c0d1555a1620504ab0fed20828c3c1f6ad1c1e98(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74e8639faead4c6044091c86c340b5976a3aa517d1e251d4418ce7f81be43e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e219295554c22ae72ff3a41a840d8c91c7a61e90b83b3e60a0ee974c9f520da8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405711b9c5046eaff1aed4a37fa96e66df0d5bd3f2d7f770f0632f0a0d46ff38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3fa2449ca7e806adb35a8e79f89e2e696bf7fc54c3fbdab3c5a9de0b80a4659(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb67704211244ab352abfc271f3577b94b2fea1a34fefe6d0c20da4d02835efd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17f72559031c443cc5718f51d310e5a51485fcbc40362e618c01550136bca3e(
    *,
    header_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d1c78ced6a35a43be762826ca75eee4ab115307b3a2b02fd0dd490035ff7a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61808d18afe2e7e1e37ebb88dbdb3f3a779be7fe54a0b0debb7c83b5f44af8c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9334a3725b6d7a2d9fd0facd0e29a4b0d3b049cda008295124eb33c1fef324(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82dab592af6ee65808b4c1c1e74bc70a750bd4a5dc3610c035de122f2aceb430(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb3289622cad770ee6e41592bb38e30461c1337e075741feb34633752532b4b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b123b3def0b0c6fc9bb90464511b1405f574e885be8fdaf584cfa4ec3633ffd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9728f4e095403a4cc53fd51a8c9d55f2712da3e02d0e0daef661065961ecb823(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddefdf8be13009d5f6a60c41384a5e2913290ce7b8312bd295edbedf9427f919(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb09fa8f59aa9413cbef5ff54b9f464ca96d86e26ba007f09c959fd543a8f46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b143df35b98a8e3622dd89bcc6b066981bbe5f751a030f9e84e075a3ee725de(
    *,
    header_name: builtins.str,
    header_value: builtins.str,
    replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6306525ca5605ee3518ab74019925dd2df7a662e3f8b703a3a050889c66c1173(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aaf2f32eb05bbd6cf934bac2d8e91c35c473333b7f503011455f9a717fa326e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca4d05fce52e862db29dbdf40cfd6103da16c26d1d12abd64dabf63a0901544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40cf2e9dae902375904f6944dca79da5ecda140e56fc20967aaaa6cb36c91b10(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29086fc5d28b8001d5d2d4288892d326f8fab9e4b17eb8c7e6a1a524418f48b4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f168b0b0a9b11839c6509bb3585530685b0413a30d699b3d9e63544df29687c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf15a00300822f14b29860ce581b02f2983881c86c7a30e448730629bd6e59d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963e7014330980fe3952756ea4e5db0f52c36bf0b17e3dc47909f57d45630035(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599373d63bff6fd23ebb5ea9d7462eeb22780727a7b69ebe77c7c75d25c8fd4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6a28536ff48f999cb583cb78c357c4d593b820f8ab1b04f7d4201abd079c09(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26d176d30d74fe13954379e3f33b1843b551c779db9a1d60d3ad2060255c35d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee0dc305d54c969ada4dc762399ee404307dc35f20eef380674c96cd5faab0d(
    *,
    header_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7737999c05a23161fb22e6713ed1ca34c05d79b4c0890b396c4951808b70e3b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15443eae981309556d27416b63842ddfe45d37d43f620ec0bdb1c69eef5dfed1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad5debca30ff31f7cc3203511ee02db4b8dddeee0d3c5fc177600daed92b73f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7983d0ee872cf90c69a53bef3b3d90f4131b375625ddac9e5ee0327bff7fafcd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3012081a3dc3f5d2319ad6f494ccd437c2df95f1d376ff2e38c2dd41084707(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb8067a6e5b370033c5323711128fdee683c9a6baf611ba68d77cb816e13a21(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7877c85c26c8cf9e60e48c1d2619bd7295913cba924427e93aeca415720b902(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d070283ea9074ffea87ed9e0f885e70137bd76974b693e3302a6ee2cdf71588(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7dca1d0cde0d4637df7e974bcada2dee08b7802e2922b883caa741d278e5ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc898715ed8e0f0af8ea342040c06be9e1d988e801c119621a0aa71265b6e37a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8264533b95d5dfd08f40c1c7bcd58bfea6dc464b426bca383048612c8fc8b84f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7026162ba1d97935f371a0bcae1168dec4b20c0ed216bf3460964ac7ada7d10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b8545dbe6e5bd8e186769023b5c7a43b440e03b31a4ec67592bdd44f56b7f6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd7e9a45f21caeae679bf310910802622e1e6b1888eecce40a33eb04f3a9b31(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e387aeba87c6680bc789b8e6b9f3dfecd7c3710ec34cf34e6f471b81fd722012(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18878045e76155bc406b1a671c0c2c9027adb40dd142e1854316eb7d8852cae8(
    *,
    full_path_match: typing.Optional[builtins.str] = None,
    header_match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path_template_match: typing.Optional[builtins.str] = None,
    prefix_match: typing.Optional[builtins.str] = None,
    query_parameter_match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8dfecd7c8b832b2debd0be864c2b42d98e62bb7fc8ee93ab991acfff0d69f66(
    *,
    header_name: builtins.str,
    exact_match: typing.Optional[builtins.str] = None,
    invert_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix_match: typing.Optional[builtins.str] = None,
    present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suffix_match: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629daa08cbaf8f4aea74734ff4a9949a309aa4df575173324a1a184acb89a939(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da5552f202155e249ea80608dd26ce5c10378fd1b377a018395f19f337e634a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69fd0e422a0bc119acf0ae095f021811d0cd8974c3a1190f8a000413ea6bb23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e25666493aebcc28fdd3049fec7751ca8c0c843b5d2e4bc1f4d71805bfd7ef4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f3d89eb38beadf1c9f1463ee7f962f8382e8b2169541484c8cfea2d717de0a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92d2aa8baeae231a9c55de144f14dde6fc1c63d0e70370b2a596e92b3f99e49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b337855d3db2780533a9abbc11f59752c60bee07867eec3a9a92f1fc79cf0776(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3adaaac0454eb0ba7b1520a618f7dd7d00f4f6c44d19b57622707b33b6e65b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b788459afb28db0af440abec93005f1e7efba0e397c49bee265fc7f2d2fd496(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b11c2799628f71ae0ef410d713bc94797cbc2357d45605f1685fabebef71470(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ffb266c39b714e2832118228efeb7c08ae36d7758220403371e3f4e5d83339(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc4f93b6fb0f2e82811f1885150bc63f70f73439ea5d089ca9af213b1bb241e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97dbe2b9dd76d2f9f2e63d0ff3ce28dba7e559c6b1ae9e6d4901d58786a92b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4adfa5e90581973b58cf79149ff3a2a8efacd5ece21f6dcbca3411bae0cf78a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0250dbab483ac3f27145066341d65e63be82c5f894488e5211d8f6aea74a69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c9c5522176ea1040980cbd99ee4bf757d9516b44a6a705c97742d1c62f2a3f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef389801c2b9c85e834985f05f4d04130f7a4023ad393d66963dcff849b539c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55fce2dde1c4392183f70736006227ac9b1e46d8b3c67e775a85d54a4eac990d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da51e70cedd59038c7ff37146a2ea3907cca3a2131dea230a5f093e4f84b1fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf471188280722e75bbca9362638dee70d1ddf83cd01e7bab8c5f5d0086cc34(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1573d79eb927e64f72bb56ec948d860e5e7239d294d7842426ec42abe6172fe1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aceaab46c4cbb4a3021e0e79df6bb4ea56f10d159f81a391ef035034c706cfbe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf9a1c0b74076439dc1cf9ec06d79cf3eca0c01fc1fd05941d0cc08eb240d47(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace81f9c78b3ca8ce0331672eeee1b9f90fcc861f5d6802649b5d87c242e0615(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d36d1a3e620a04d0b4c3e64edb57409af274f18fdf9611bce0ac396584acdd2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f3e95077514a1bebef169418b01399d08a5673f1fc02c040d3c227ee33e81c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408fc004e6ef9e06a87a2e2ed07d4e3e9519534b3a818cb80ec670eefe63b5e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c29fe3b6866d4dc38dab5d9df5fd5bd93f66bcaf733f79b74a067fe4000326(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606afefc0e88cb34b8de3640d4351a930d33358522bb80cc672f6b560b53c03e(
    *,
    name: builtins.str,
    exact_match: typing.Optional[builtins.str] = None,
    present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3beabaa153c79555409332fdda87ba765a68db1df1359606d10d4b88f8fc7752(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a29bbeb8c4cda4f402633977a06a35e4b624d26cc69470fabdd889347018baa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25b5e8738e740136997dff2ebc3e44d7ad43f86e2486d4120f6f29010815919(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8bd717a0d35e3fc3a7188b73d857e5241ddcb6ab785ad73ab9d89b975874e4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87373c6bcdc031ec66bacb9e289aa82edecd8e30255d4d46796bed42c8eff0c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17107b30a2adcbfbdee30328dcbec6b576c923495a4fd857c3e61de4583645e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aee0bca3219e5ffa79dae90736184f415e248b819c7803f800d8cfd836fe1c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004a6ba330e2af89c104a778f6cd1299522b66f34cfdd3ebce95b1ddefb136e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e4767f42122a61c7c2368f6892606a3d9eb68471276bbff16b507ba3411d06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663d22a99b22d43d6ac100e41291ec6fa9b4ffb3aaf4399e283139d1b5cb8e50(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ce9c2c112f40b0a35fb1252bed4741a6779e7907a8095ae794d42f8b3e87df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2114c1d9609df0fd3d4c2f0222ef3a4ce89637761846dabd76aa6387b7834045(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f99f199439fffc8e1c779d1efb6e7187500eb786043bfdc9f9f9e549db2600(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151a3a6c35f4ecb381dd08c46afcbfed7eb98fff53031ae4fd6eaa06841cc3e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453fab5a3e4a2161385866d23e32747b3958c291ea079c9488b3b248b59a3e1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77493902bfb6c0af047a83b453eed95c7ad0c4c443fa46321e9843d093e7146(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb04ff6b6cc9ec36ea41788fb61dfb665806372cb3a959b44ce28b65e664119(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3bf4b2751a9fd04694026fa3ab613987e3e66ab8d5f501a4c0112449aad3482(
    *,
    cdn_policy: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    compression_mode: typing.Optional[builtins.str] = None,
    cors_policy: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    url_rewrite: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7664c3e48a20a800949f8d9c133627ad6fc1a8615b84ba9eaea0965356e53a7(
    *,
    add_signatures: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures, typing.Dict[builtins.str, typing.Any]]] = None,
    cache_key_policy: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    cache_mode: typing.Optional[builtins.str] = None,
    client_ttl: typing.Optional[builtins.str] = None,
    default_ttl: typing.Optional[builtins.str] = None,
    max_ttl: typing.Optional[builtins.str] = None,
    negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    negative_caching_policy: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    signed_request_keyset: typing.Optional[builtins.str] = None,
    signed_request_maximum_expiration_ttl: typing.Optional[builtins.str] = None,
    signed_request_mode: typing.Optional[builtins.str] = None,
    signed_token_options: typing.Optional[typing.Union[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b980123062746615f13eb149865e6f34cc0f70820ed2f8820d3756f701b476a(
    *,
    actions: typing.Sequence[builtins.str],
    copied_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    keyset: typing.Optional[builtins.str] = None,
    token_query_parameter: typing.Optional[builtins.str] = None,
    token_ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5311a17b402cd62c5c5f6a99ae76c2f3c7684d278ef204e19dd4495162105922(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125c719eb11a1b25de6302927b9353c10a4a301c9748f71c7f191befc8827238(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1027c610fb7b540146e7eece8867e24465939e42feeb199e93af67d6e2e42484(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860e43618b572d9afb76f32bf66eaf6bffd6f84616416485b8129febe63cb0fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6b1b9783133bdd7ed0946769c3738cec2b470bb81a2f676e990aace2a01170(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1ab974aa5a7948e2d62f39d0c15c89d206952ad6854f045fc3fc72f1ee650b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c84defea692aabeaf70f5f9b772fff24bc71b82758749e69e24c07265b9015(
    value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7465134225dc6ae5a4c76cd85977fbdceaa20bf4ac369ebac8fc4b3639971b25(
    *,
    excluded_query_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_host: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclude_query_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    included_cookie_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_header_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_query_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_protocol: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f183c1f80f6043e5d84f75d482b42963bc229c5dbbb3f6664c8db78d9f17f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60700932dbfedc2860f2512736a48ec2e2e05bb57bbd03f5bf453e439badb45d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf916f377947762ee047f19f40a57dd3fc680483e4d3ed21c02c0d285a9acfab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d83e215ce126ab343480aed02c47436711f777952b9b108294a17a3c0e7d8cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__110fbfb389fcd463bd523decd1531ea3d28a40c6bca465549d541682afd30797(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1dc63e176cfef1c4b356e9de5bb5241c25fba459e044721be7b351b4b24edd2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0c053737e014dbbe3d1b34022f5c33f83f6a27dbc2175405696e9c133b0a83(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9106c1bb5aff398d692bf3a9605aa6f79f3b377918c30aa78f31f4996a0a6fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a524aa55daa5d9de91c44e5e42135b4ed4a3c8c5ba42d8945c526bf068607c5(
    value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec6669d6053c357ce7d7c5f12ffa4cc51e418039ced836003225328b4283488(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f5dfa75be7f1fb5300d9cf25fbb9ed5049dfd0722569c508c0a3b1444474ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eada20514cb5d2ad5e82f937676cd726fc291e08bdb4e9a88405dead24969c31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0edc4fc2970f94ce35161392f8155570c5dbb4a213f87f3a99421fe042a1231d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf37e598ccfb964e5bf2b9ed46a2db1611a1f3f6b21f9227f4d3e256f4263fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5791c20cac217c2a1ed2fc8cf3b84ad1d0f293f47e611e7ca2e612283bdd51cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d48db6d821749ae010bc5c0754da3c38202d4fd127c0c58076f0aeceed1179(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e80383dd59cea648c1db1aad0ed796930a097bb628a6539c4adb5dce99e4db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ec65091556b55bf969ea42dcc21fe2e9212036ffe5c4d56adc7581c0c41973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f857a1ff65cb9b9db6f58296a1266f1488344f5177607367c40b28b2d1e67f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924bea5b689cec06e369422160139a21125c5096175dd53b4dc978c26c22583f(
    value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e6f74096f703c33ee1e1b0638ae2b556dc155eafa36b4c464f376654e61b1f(
    *,
    allowed_signature_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    token_query_parameter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d32a9ced718192e3c405b79a857539432967cc5c0722a91c9209a477ba45d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b840933fd3b43f2b15d053e1acb8907041c25570fd4989f1d3f465ce7d7321(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918eaacae1037cca0fc9edf73a8a02ebe890fcab8ea184038e5def9eb6514b23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1687147fa516a258dac15342140f7a046bb09f6fac3a876df6f1f14aafca9919(
    value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b155d7ab658aa4d8423bc492385f7fd2917a35f27d944099032de9e32a1e591(
    *,
    max_age: builtins.str,
    allow_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7775b64c62adedcb3e20f511f57e9bb9eaa24012913633052f2654d62a8b96fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb89dcd2a06918f42c872e3c088e85d40f3180c51c310a78d052ba72dcd4693b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b747afd00a73ff213acf0380ed6f5561ce9cf07d2226b73379d2c9360ac783e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b95324d8e4a00d54b514572e8d64e2d65ab3c784da22b39e16e647ffc522a5b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8890509a03589831c6ba1fdd3cf7f67bd6b4064010e2aa05cde5f39ee777e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59bca629e664e4a3c09383f68db7303d7d9f4464d4aabfff7d99c1b769b8df78(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe5c0924436b1079d7d1b98475ebec0c37e0327d887e02b3d30cc5c37aaaed1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0b1b5c3361f35bd75fe6f36c3cd1eee7ff6a7f1bef02bbc3fe6dcb5e898542(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666a715fbfec89c0ff7841239bccafa231af1f0234e11523ffd0859f839a4891(
    value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7caa2abb664b8edc2964c24d586835d16aba580fd837d060f672f6c02c8569f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991a33020792ee25d2ab68b288ace98e0d4f10a5937724c62ab2201b5d427840(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e242b96c6eeb95a162fc34c0b50e6cb15376523f50f270407cb6dfb121c16365(
    value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9bfe01e62ccc1fadee57a8dd32925175a2c93bf2a0cf411de81af08e3ada39c(
    *,
    host_rewrite: typing.Optional[builtins.str] = None,
    path_prefix_rewrite: typing.Optional[builtins.str] = None,
    path_template_rewrite: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60759fc4b2b2b9f14306abdd17d11d26f33e6e917bce6faccfd4944124af7662(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1becfdf28608f6e71d4ee8a1d184013cd38b27a092049362bc6f43dc0cd2a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78189461605ea44afd0037eb368aee5cf762cfd674f61bd23fa799e8e38e848c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f0ca805690aae5c6231771e84e47ce62828cabf3c3a29164d8a39069bd268d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab05f57fc4de779db26d895370c2075df8267887b7a64c36c1a896dd1488e3b3(
    value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73cc32bfc701a35c41386e6d3abe2ff7623de6f3141a4845151c4c6932a6b400(
    *,
    allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2abd1501f3271312808692b79bd6ca93eb7a91afbb813eab57b8170ab7882fc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1b019be864c4eda2ca33c82925e7b5cc61d772b844e6dc7f9f048d854b0402(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3290fa97e21c76012e16b440c4bbf42ce892b6844afb8d91c4c633244cc14f7(
    value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb22338bd293a412862dfd078500520266a9c778b7d29180388003b2eb26b7b(
    *,
    host_redirect: typing.Optional[builtins.str] = None,
    https_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path_redirect: typing.Optional[builtins.str] = None,
    prefix_redirect: typing.Optional[builtins.str] = None,
    redirect_response_code: typing.Optional[builtins.str] = None,
    strip_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843765f3f131ba6ce0210ac9ac10a5840695d68942d259892f10bc59d12a9556(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a768b33b7c21e6b9196e6c441ebffae73102db72bfc2e848214eeba723ec61f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb0778245e2e32fc054d6d8dff6e0ad70019b84cf73a6bc536311dc5812633b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7811f054cf57f0262515b3c3499374ffb7bc8a6081170ec024f251be2554863c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e02ec6611cbca4dedc9d9da53d0e91939205d2651a363b0c6bd9eabc1a4563(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5bc348119acccd54dd7b2700d877dfc9c2a76d5fc5834fc6021e5b161f39d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f12ebea6717ee3ce7c7824dec038b565a117a6a752087676e66e1ee06800e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159cf9d00e3eda47bc9d8a16c27f4af28bf152827839b3df854cc5c3a0f73545(
    value: typing.Optional[NetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85239f6f8126a02d5d2193d99f72ee1bc132941d3a69dbc90954730f029091a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d157b26705d4850dbbb34c16059656c4518970ccc6465f84564fa37da8f646(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758cf784de29c87634f260abc39c7411c5edc3d4bb53d687f438de066b09fd9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b79c0292e165293db04857b959c68bff4c8b44ab4a0fbe594735ca8257801ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92071a9e02d8ce39861ae898ae6776c5151d99088231b1d862097d8d8ad09240(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0041fd28813a1fbb4eb7d520e80d54c007d9839eb93ab3b76f4b78dc70e0610f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesEdgeCacheServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
