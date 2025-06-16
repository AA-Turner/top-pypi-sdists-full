r'''
# `google_network_services_edge_cache_service`

Refer to the Terraform Registry for docs: [`google_network_services_edge_cache_service`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service).
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


class GoogleNetworkServicesEdgeCacheService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service google_network_services_edge_cache_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        routing: typing.Union["GoogleNetworkServicesEdgeCacheServiceRouting", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        disable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_quic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        edge_security_policy: typing.Optional[builtins.str] = None,
        edge_ssl_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_config: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        require_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service google_network_services_edge_cache_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#name GoogleNetworkServicesEdgeCacheService#name}
        :param routing: routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#routing GoogleNetworkServicesEdgeCacheService#routing}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#description GoogleNetworkServicesEdgeCacheService#description}
        :param disable_http2: Disables HTTP/2. HTTP/2 (h2) is enabled by default and recommended for performance. HTTP/2 improves connection re-use and reduces connection setup overhead by sending multiple streams over the same connection. Some legacy HTTP clients may have issues with HTTP/2 connections due to broken HTTP/2 implementations. Setting this to true will prevent HTTP/2 from being advertised and negotiated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#disable_http2 GoogleNetworkServicesEdgeCacheService#disable_http2}
        :param disable_quic: HTTP/3 (IETF QUIC) and Google QUIC are enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#disable_quic GoogleNetworkServicesEdgeCacheService#disable_quic}
        :param edge_security_policy: Resource URL that points at the Cloud Armor edge security policy that is applied on each request against the EdgeCacheService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#edge_security_policy GoogleNetworkServicesEdgeCacheService#edge_security_policy}
        :param edge_ssl_certificates: URLs to sslCertificate resources that are used to authenticate connections between users and the EdgeCacheService. Note that only "global" certificates with a "scope" of "EDGE_CACHE" can be attached to an EdgeCacheService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#edge_ssl_certificates GoogleNetworkServicesEdgeCacheService#edge_ssl_certificates}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#id GoogleNetworkServicesEdgeCacheService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the EdgeCache resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#labels GoogleNetworkServicesEdgeCacheService#labels}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#log_config GoogleNetworkServicesEdgeCacheService#log_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#project GoogleNetworkServicesEdgeCacheService#project}.
        :param require_tls: Require TLS (HTTPS) for all clients connecting to this service. Clients who connect over HTTP (port 80) will receive a HTTP 301 to the same URL over HTTPS (port 443). You must have at least one (1) edgeSslCertificate specified to enable this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#require_tls GoogleNetworkServicesEdgeCacheService#require_tls}
        :param ssl_policy: URL of the SslPolicy resource that will be associated with the EdgeCacheService. If not set, the EdgeCacheService has no SSL policy configured, and will default to the "COMPATIBLE" policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#ssl_policy GoogleNetworkServicesEdgeCacheService#ssl_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#timeouts GoogleNetworkServicesEdgeCacheService#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dfab8066fe15f24966bad7ae6a41615b995c0a15a32aa06c62b5370c9379f51)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetworkServicesEdgeCacheServiceConfig(
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
        '''Generates CDKTF code for importing a GoogleNetworkServicesEdgeCacheService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetworkServicesEdgeCacheService to import.
        :param import_from_id: The id of the existing GoogleNetworkServicesEdgeCacheService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetworkServicesEdgeCacheService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4788096400681ad9841d9557e99430787bac146ca096c93f09ff57943d31ff93)
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
        :param enable: Specifies whether to enable logging for traffic served by this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#enable GoogleNetworkServicesEdgeCacheService#enable}
        :param sample_rate: Configures the sampling rate of requests, where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0, and the value of the field must be in [0, 1]. This field can only be specified if logging is enabled for this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#sample_rate GoogleNetworkServicesEdgeCacheService#sample_rate}
        '''
        value = GoogleNetworkServicesEdgeCacheServiceLogConfig(
            enable=enable, sample_rate=sample_rate
        )

        return typing.cast(None, jsii.invoke(self, "putLogConfig", [value]))

    @jsii.member(jsii_name="putRouting")
    def put_routing(
        self,
        *,
        host_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingHostRule", typing.Dict[builtins.str, typing.Any]]]],
        path_matcher: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param host_rule: host_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#host_rule GoogleNetworkServicesEdgeCacheService#host_rule}
        :param path_matcher: path_matcher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_matcher GoogleNetworkServicesEdgeCacheService#path_matcher}
        '''
        value = GoogleNetworkServicesEdgeCacheServiceRouting(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#create GoogleNetworkServicesEdgeCacheService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#delete GoogleNetworkServicesEdgeCacheService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#update GoogleNetworkServicesEdgeCacheService#update}.
        '''
        value = GoogleNetworkServicesEdgeCacheServiceTimeouts(
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
    def log_config(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheServiceLogConfigOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="routing")
    def routing(self) -> "GoogleNetworkServicesEdgeCacheServiceRoutingOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingOutputReference", jsii.get(self, "routing"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheServiceTimeoutsOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceLogConfig"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceLogConfig"], jsii.get(self, "logConfigInput"))

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
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRouting"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRouting"], jsii.get(self, "routingInput"))

    @builtins.property
    @jsii.member(jsii_name="sslPolicyInput")
    def ssl_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkServicesEdgeCacheServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkServicesEdgeCacheServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80acdf34fa7f61d82faa48267b66e20cfd1c031e1f2672b916fddf93a047408c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaeb64c600e2a50b589a3c274387e5bd57266cdc9391d1f3fc874a542fc680a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f9199c24674c6794826d0eba1c89a846e5e1681067e0ceadefae1a4149bd609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableQuic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeSecurityPolicy")
    def edge_security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeSecurityPolicy"))

    @edge_security_policy.setter
    def edge_security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfaea435f9caf601bf5186c998bc580f1693edbededc01655510a5357af8a151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeSecurityPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeSslCertificates")
    def edge_ssl_certificates(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "edgeSslCertificates"))

    @edge_ssl_certificates.setter
    def edge_ssl_certificates(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5e54a3c075ca64f9dccc3f3f23e517bfceea86b7fb460c7822254e94048b05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeSslCertificates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3b1889a0a567022404ed85d26ca08f214691bd17bb5e2217d327f356e7d7d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__038b207717a403404cb9d8ea33f320ef275efe113de0c65bcbed1455e8d653d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806151dbefb706afbc0c2b53952d986d33626ad53c76509e2a469af4c07e72e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a78d96b9aef3e1d95165e90a711eaf500f177960d46ec8e828d6c2333884456)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b14f53d194d7245a04c3ab58e05602d5091550224228f8448da48c89e905e7f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireTls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslPolicy")
    def ssl_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslPolicy"))

    @ssl_policy.setter
    def ssl_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb94f89d98dd34093429790dff67070288190a50d2abd5ff4d0f944036131f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslPolicy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceConfig",
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
class GoogleNetworkServicesEdgeCacheServiceConfig(
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
        name: builtins.str,
        routing: typing.Union["GoogleNetworkServicesEdgeCacheServiceRouting", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        disable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_quic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        edge_security_policy: typing.Optional[builtins.str] = None,
        edge_ssl_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_config: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        require_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#name GoogleNetworkServicesEdgeCacheService#name}
        :param routing: routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#routing GoogleNetworkServicesEdgeCacheService#routing}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#description GoogleNetworkServicesEdgeCacheService#description}
        :param disable_http2: Disables HTTP/2. HTTP/2 (h2) is enabled by default and recommended for performance. HTTP/2 improves connection re-use and reduces connection setup overhead by sending multiple streams over the same connection. Some legacy HTTP clients may have issues with HTTP/2 connections due to broken HTTP/2 implementations. Setting this to true will prevent HTTP/2 from being advertised and negotiated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#disable_http2 GoogleNetworkServicesEdgeCacheService#disable_http2}
        :param disable_quic: HTTP/3 (IETF QUIC) and Google QUIC are enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#disable_quic GoogleNetworkServicesEdgeCacheService#disable_quic}
        :param edge_security_policy: Resource URL that points at the Cloud Armor edge security policy that is applied on each request against the EdgeCacheService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#edge_security_policy GoogleNetworkServicesEdgeCacheService#edge_security_policy}
        :param edge_ssl_certificates: URLs to sslCertificate resources that are used to authenticate connections between users and the EdgeCacheService. Note that only "global" certificates with a "scope" of "EDGE_CACHE" can be attached to an EdgeCacheService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#edge_ssl_certificates GoogleNetworkServicesEdgeCacheService#edge_ssl_certificates}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#id GoogleNetworkServicesEdgeCacheService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the EdgeCache resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#labels GoogleNetworkServicesEdgeCacheService#labels}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#log_config GoogleNetworkServicesEdgeCacheService#log_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#project GoogleNetworkServicesEdgeCacheService#project}.
        :param require_tls: Require TLS (HTTPS) for all clients connecting to this service. Clients who connect over HTTP (port 80) will receive a HTTP 301 to the same URL over HTTPS (port 443). You must have at least one (1) edgeSslCertificate specified to enable this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#require_tls GoogleNetworkServicesEdgeCacheService#require_tls}
        :param ssl_policy: URL of the SslPolicy resource that will be associated with the EdgeCacheService. If not set, the EdgeCacheService has no SSL policy configured, and will default to the "COMPATIBLE" policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#ssl_policy GoogleNetworkServicesEdgeCacheService#ssl_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#timeouts GoogleNetworkServicesEdgeCacheService#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(routing, dict):
            routing = GoogleNetworkServicesEdgeCacheServiceRouting(**routing)
        if isinstance(log_config, dict):
            log_config = GoogleNetworkServicesEdgeCacheServiceLogConfig(**log_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetworkServicesEdgeCacheServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51ff3fa5fb3c377e869ab6a4f6d0e69545867a0acf7f3336bc0a0d5826b5e074)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#name GoogleNetworkServicesEdgeCacheService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routing(self) -> "GoogleNetworkServicesEdgeCacheServiceRouting":
        '''routing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#routing GoogleNetworkServicesEdgeCacheService#routing}
        '''
        result = self._values.get("routing")
        assert result is not None, "Required property 'routing' is missing"
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRouting", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#description GoogleNetworkServicesEdgeCacheService#description}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#disable_http2 GoogleNetworkServicesEdgeCacheService#disable_http2}
        '''
        result = self._values.get("disable_http2")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_quic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''HTTP/3 (IETF QUIC) and Google QUIC are enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#disable_quic GoogleNetworkServicesEdgeCacheService#disable_quic}
        '''
        result = self._values.get("disable_quic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def edge_security_policy(self) -> typing.Optional[builtins.str]:
        '''Resource URL that points at the Cloud Armor edge security policy that is applied on each request against the EdgeCacheService.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#edge_security_policy GoogleNetworkServicesEdgeCacheService#edge_security_policy}
        '''
        result = self._values.get("edge_security_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_ssl_certificates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URLs to sslCertificate resources that are used to authenticate connections between users and the EdgeCacheService.

        Note that only "global" certificates with a "scope" of "EDGE_CACHE" can be attached to an EdgeCacheService.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#edge_ssl_certificates GoogleNetworkServicesEdgeCacheService#edge_ssl_certificates}
        '''
        result = self._values.get("edge_ssl_certificates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#id GoogleNetworkServicesEdgeCacheService#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#labels GoogleNetworkServicesEdgeCacheService#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def log_config(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#log_config GoogleNetworkServicesEdgeCacheService#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceLogConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#project GoogleNetworkServicesEdgeCacheService#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require TLS (HTTPS) for all clients connecting to this service.

        Clients who connect over HTTP (port 80) will receive a HTTP 301 to the same URL over HTTPS (port 443).
        You must have at least one (1) edgeSslCertificate specified to enable this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#require_tls GoogleNetworkServicesEdgeCacheService#require_tls}
        '''
        result = self._values.get("require_tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssl_policy(self) -> typing.Optional[builtins.str]:
        '''URL of the SslPolicy resource that will be associated with the EdgeCacheService.

        If not set, the EdgeCacheService has no SSL policy configured, and will default to the "COMPATIBLE" policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#ssl_policy GoogleNetworkServicesEdgeCacheService#ssl_policy}
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#timeouts GoogleNetworkServicesEdgeCacheService#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceLogConfig",
    jsii_struct_bases=[],
    name_mapping={"enable": "enable", "sample_rate": "sampleRate"},
)
class GoogleNetworkServicesEdgeCacheServiceLogConfig:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sample_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable: Specifies whether to enable logging for traffic served by this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#enable GoogleNetworkServicesEdgeCacheService#enable}
        :param sample_rate: Configures the sampling rate of requests, where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0, and the value of the field must be in [0, 1]. This field can only be specified if logging is enabled for this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#sample_rate GoogleNetworkServicesEdgeCacheService#sample_rate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a99bdabb9013c88ed8c296474bf571f9d8043ea272131aef92d51da66beb33e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#enable GoogleNetworkServicesEdgeCacheService#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sample_rate(self) -> typing.Optional[jsii.Number]:
        '''Configures the sampling rate of requests, where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0, and the value of the field must be in [0, 1].

        This field can only be specified if logging is enabled for this service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#sample_rate GoogleNetworkServicesEdgeCacheService#sample_rate}
        '''
        result = self._values.get("sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__769fb073babdeebd252fef038bfd2ff869aca879982aca6762b67ddaf765c851)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85d1dff863557ad1ff252d7bb454557df0920c5d12612bcdc94d134f53c2ce19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRate")
    def sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRate"))

    @sample_rate.setter
    def sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a63d9a2386f4a84e7dfb4acd7fc1f79b5bc40d44eac2f473cadd3c2bae3a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceLogConfig]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48b2475c7ad69a0e02db4effd5154a908b1be10fa57bdad1397532eb9100cbe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRouting",
    jsii_struct_bases=[],
    name_mapping={"host_rule": "hostRule", "path_matcher": "pathMatcher"},
)
class GoogleNetworkServicesEdgeCacheServiceRouting:
    def __init__(
        self,
        *,
        host_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingHostRule", typing.Dict[builtins.str, typing.Any]]]],
        path_matcher: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param host_rule: host_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#host_rule GoogleNetworkServicesEdgeCacheService#host_rule}
        :param path_matcher: path_matcher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_matcher GoogleNetworkServicesEdgeCacheService#path_matcher}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec23ca5a963054a34110a084f33ed1f472372407b587e933e7efe8060b04a95)
            check_type(argname="argument host_rule", value=host_rule, expected_type=type_hints["host_rule"])
            check_type(argname="argument path_matcher", value=path_matcher, expected_type=type_hints["path_matcher"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_rule": host_rule,
            "path_matcher": path_matcher,
        }

    @builtins.property
    def host_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingHostRule"]]:
        '''host_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#host_rule GoogleNetworkServicesEdgeCacheService#host_rule}
        '''
        result = self._values.get("host_rule")
        assert result is not None, "Required property 'host_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingHostRule"]], result)

    @builtins.property
    def path_matcher(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher"]]:
        '''path_matcher block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_matcher GoogleNetworkServicesEdgeCacheService#path_matcher}
        '''
        result = self._values.get("path_matcher")
        assert result is not None, "Required property 'path_matcher' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingHostRule",
    jsii_struct_bases=[],
    name_mapping={
        "hosts": "hosts",
        "path_matcher": "pathMatcher",
        "description": "description",
    },
)
class GoogleNetworkServicesEdgeCacheServiceRoutingHostRule:
    def __init__(
        self,
        *,
        hosts: typing.Sequence[builtins.str],
        path_matcher: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hosts: The list of host patterns to match. Host patterns must be valid hostnames. Ports are not allowed. Wildcard hosts are supported in the suffix or prefix form. * matches any string of ([a-z0-9-.]*). It does not match the empty string. When multiple hosts are specified, hosts are matched in the following priority: 1. Exact domain names: ''www.foo.com''. 2. Suffix domain wildcards: ''*.foo.com'' or ''*-bar.foo.com''. 3. Prefix domain wildcards: ''foo.*'' or ''foo-*''. 4. Special wildcard ''*'' matching any domain. Notes:: The wildcard will not match the empty string. e.g. ''*-bar.foo.com'' will match ''baz-bar.foo.com'' but not ''-bar.foo.com''. The longest wildcards match first. Only a single host in the entire service can match on ''*''. A domain must be unique across all configured hosts within a service. Hosts are matched against the HTTP Host header, or for HTTP/2 and HTTP/3, the ":authority" header, from the incoming request. You may specify up to 10 hosts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#hosts GoogleNetworkServicesEdgeCacheService#hosts}
        :param path_matcher: The name of the pathMatcher associated with this hostRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_matcher GoogleNetworkServicesEdgeCacheService#path_matcher}
        :param description: A human-readable description of the hostRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#description GoogleNetworkServicesEdgeCacheService#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c087355f057727a95835ca7287bfe9cdd44242e692c1a25aad2b6aeea3eefc23)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#hosts GoogleNetworkServicesEdgeCacheService#hosts}
        '''
        result = self._values.get("hosts")
        assert result is not None, "Required property 'hosts' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def path_matcher(self) -> builtins.str:
        '''The name of the pathMatcher associated with this hostRule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_matcher GoogleNetworkServicesEdgeCacheService#path_matcher}
        '''
        result = self._values.get("path_matcher")
        assert result is not None, "Required property 'path_matcher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the hostRule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#description GoogleNetworkServicesEdgeCacheService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingHostRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingHostRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingHostRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c62d9ef04b9bc61fc91bc97e294e5d1c73f0f18e6b721619d170b8e4e4550e10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingHostRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61416c9c2644e5efcc7328899811608b51f7c832b4976d314e4f4408837b4380)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingHostRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4bde08cd630c968c1cdc12e7f1f2d50c24224603ed478b4bb4a2bd10de0c72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__385de99a03e4c3239fc6b35ee5431def0e5b42a825f4043cc3d951607fde2322)
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
            type_hints = typing.get_type_hints(_typecheckingstub__896f7a7049572a428649193081455dc15ff34730ac6c0f8ddf0b8119634bc603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingHostRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingHostRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingHostRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14be2a4169cd579ca90369237a4abee075f39a0067733256d9c829675cf96fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingHostRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingHostRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18702e3335e4e6b7b6426ecdeff8c1921ebcfcf75b0dfcd1c3e3bad3a7eb46bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1577441283d7da576ced83d7f93603ffae5e98fb80c58ac9de44e85007c7cb09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hosts")
    def hosts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hosts"))

    @hosts.setter
    def hosts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55b4125a4d8c828a635d1a2c8a52838b76098e64cc68fbac3cf6609e04e18059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hosts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathMatcher")
    def path_matcher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathMatcher"))

    @path_matcher.setter
    def path_matcher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c870d6c2eaf9e91be03d397c861c034f07af42a75a769b9b0d6316ed1ef0e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathMatcher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingHostRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingHostRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingHostRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48199a92e3951ac714d0073bf6fa5e8542acb252cb1110c691fa011b06643034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ceff50cc426d94a516334ac02ae76a49302e4b2aa4062886a18e015acace369)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHostRule")
    def put_host_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingHostRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc3cca0874ff2fae1f6dbcf61a16c763c0ffa3b2d6dff44ec057b066f427aeeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHostRule", [value]))

    @jsii.member(jsii_name="putPathMatcher")
    def put_path_matcher(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4409c145767550c32e188f83c322fe881862599c1a98e41390eda20e777a5cd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPathMatcher", [value]))

    @builtins.property
    @jsii.member(jsii_name="hostRule")
    def host_rule(self) -> GoogleNetworkServicesEdgeCacheServiceRoutingHostRuleList:
        return typing.cast(GoogleNetworkServicesEdgeCacheServiceRoutingHostRuleList, jsii.get(self, "hostRule"))

    @builtins.property
    @jsii.member(jsii_name="pathMatcher")
    def path_matcher(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherList":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherList", jsii.get(self, "pathMatcher"))

    @builtins.property
    @jsii.member(jsii_name="hostRuleInput")
    def host_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingHostRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingHostRule]]], jsii.get(self, "hostRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="pathMatcherInput")
    def path_matcher_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher"]]], jsii.get(self, "pathMatcherInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRouting]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRouting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRouting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66f990fc9f7a0d715db380b0b94216d38d84d85493216e6a929cf5a1883b696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "route_rule": "routeRule",
        "description": "description",
    },
)
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher:
    def __init__(
        self,
        *,
        name: builtins.str,
        route_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name to which this PathMatcher is referred by the HostRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#name GoogleNetworkServicesEdgeCacheService#name}
        :param route_rule: route_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#route_rule GoogleNetworkServicesEdgeCacheService#route_rule}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#description GoogleNetworkServicesEdgeCacheService#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175f17cb973185d3d0d60849422a2dff58d18eeef4c9f28414790da57c69d5ef)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#name GoogleNetworkServicesEdgeCacheService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def route_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule"]]:
        '''route_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#route_rule GoogleNetworkServicesEdgeCacheService#route_rule}
        '''
        result = self._values.get("route_rule")
        assert result is not None, "Required property 'route_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#description GoogleNetworkServicesEdgeCacheService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f49f94b9e76c7ca6c9fb68553d01f3298591da02259efc3cfbec9263c1f444f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68f1e51cda75dff7824df1743665952b191fac1a4aa80dbd685c5b3c71d1cf7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398f7922b54a2c72d8242e3d42cab65f82178bb1c17948b48d79abc366bc60f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3b097b6618011b87f0b94ff4610022b479e53bce384671d842a58b4e4ff9c07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa386c850c0ca894bbd3f664537837513378e9a8cead2f4470448d2e9aa218f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff97cd798941c4e7fd300ddb7bb7c52cc9dcf78b76c887103d947fad39d0d52e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c15baf4b27b0e11f7d61191b42846f7a63d5369400dcb6c725baf1a979846c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRouteRule")
    def put_route_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f04dd28eef328dc196425c2bb6934fffb8cd4747fda45ff0e31e3cd794b4e382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRouteRule", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="routeRule")
    def route_rule(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleList":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleList", jsii.get(self, "routeRule"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule"]]], jsii.get(self, "routeRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f115ff40cd493e2d5f525bb9f96db2e06ea48254dc4e8d4d708e16119ff483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61147423fd41008eb4d9774c08675bd9b34214c0180578b3c548f47acb1e83ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078caa42d18ff980ca8808b4e2dfb684b9bc5e7590e9933b75108a5ba13451ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule",
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
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule:
    def __init__(
        self,
        *,
        match_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule", typing.Dict[builtins.str, typing.Any]]]],
        priority: builtins.str,
        description: typing.Optional[builtins.str] = None,
        header_action: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction", typing.Dict[builtins.str, typing.Any]]] = None,
        origin: typing.Optional[builtins.str] = None,
        route_action: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction", typing.Dict[builtins.str, typing.Any]]] = None,
        route_methods: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods", typing.Dict[builtins.str, typing.Any]]] = None,
        url_redirect: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param match_rule: match_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#match_rule GoogleNetworkServicesEdgeCacheService#match_rule}
        :param priority: The priority of this route rule, where 1 is the highest priority. You cannot configure two or more routeRules with the same priority. Priority for each rule must be set to a number between 1 and 999 inclusive. Priority numbers can have gaps, which enable you to add or remove rules in the future without affecting the rest of the rules. For example, 1, 2, 3, 4, 5, 9, 12, 16 is a valid series of priority numbers to which you could add rules numbered from 6 to 8, 10 to 11, and 13 to 15 in the future without any impact on existing rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#priority GoogleNetworkServicesEdgeCacheService#priority}
        :param description: A human-readable description of the routeRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#description GoogleNetworkServicesEdgeCacheService#description}
        :param header_action: header_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_action GoogleNetworkServicesEdgeCacheService#header_action}
        :param origin: The Origin resource that requests to this route should fetch from when a matching response is not in cache. Origins can be defined as short names ("my-origin") or fully-qualified resource URLs - e.g. "networkservices.googleapis.com/projects/my-project/global/edgecacheorigins/my-origin" Only one of origin or urlRedirect can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#origin GoogleNetworkServicesEdgeCacheService#origin}
        :param route_action: route_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#route_action GoogleNetworkServicesEdgeCacheService#route_action}
        :param route_methods: route_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#route_methods GoogleNetworkServicesEdgeCacheService#route_methods}
        :param url_redirect: url_redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#url_redirect GoogleNetworkServicesEdgeCacheService#url_redirect}
        '''
        if isinstance(header_action, dict):
            header_action = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction(**header_action)
        if isinstance(route_action, dict):
            route_action = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction(**route_action)
        if isinstance(route_methods, dict):
            route_methods = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods(**route_methods)
        if isinstance(url_redirect, dict):
            url_redirect = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect(**url_redirect)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e70ae1b8b611efc876eb81b0a46ccc4115c33b530c3f1cf386f7e0a98355a8d)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule"]]:
        '''match_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#match_rule GoogleNetworkServicesEdgeCacheService#match_rule}
        '''
        result = self._values.get("match_rule")
        assert result is not None, "Required property 'match_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule"]], result)

    @builtins.property
    def priority(self) -> builtins.str:
        '''The priority of this route rule, where 1 is the highest priority.

        You cannot configure two or more routeRules with the same priority. Priority for each rule must be set to a number between 1 and 999 inclusive.

        Priority numbers can have gaps, which enable you to add or remove rules in the future without affecting the rest of the rules. For example, 1, 2, 3, 4, 5, 9, 12, 16 is a valid series of priority numbers
        to which you could add rules numbered from 6 to 8, 10 to 11, and 13 to 15 in the future without any impact on existing rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#priority GoogleNetworkServicesEdgeCacheService#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the routeRule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#description GoogleNetworkServicesEdgeCacheService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_action(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction"]:
        '''header_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_action GoogleNetworkServicesEdgeCacheService#header_action}
        '''
        result = self._values.get("header_action")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction"], result)

    @builtins.property
    def origin(self) -> typing.Optional[builtins.str]:
        '''The Origin resource that requests to this route should fetch from when a matching response is not in cache.

        Origins can be defined as short names ("my-origin") or fully-qualified resource URLs - e.g. "networkservices.googleapis.com/projects/my-project/global/edgecacheorigins/my-origin"

        Only one of origin or urlRedirect can be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#origin GoogleNetworkServicesEdgeCacheService#origin}
        '''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_action(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction"]:
        '''route_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#route_action GoogleNetworkServicesEdgeCacheService#route_action}
        '''
        result = self._values.get("route_action")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction"], result)

    @builtins.property
    def route_methods(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods"]:
        '''route_methods block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#route_methods GoogleNetworkServicesEdgeCacheService#route_methods}
        '''
        result = self._values.get("route_methods")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods"], result)

    @builtins.property
    def url_redirect(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect"]:
        '''url_redirect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#url_redirect GoogleNetworkServicesEdgeCacheService#url_redirect}
        '''
        result = self._values.get("url_redirect")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction",
    jsii_struct_bases=[],
    name_mapping={
        "request_header_to_add": "requestHeaderToAdd",
        "request_header_to_remove": "requestHeaderToRemove",
        "response_header_to_add": "responseHeaderToAdd",
        "response_header_to_remove": "responseHeaderToRemove",
    },
)
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction:
    def __init__(
        self,
        *,
        request_header_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header_to_remove: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove", typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_header_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd", typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_header_to_remove: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_header_to_add: request_header_to_add block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#request_header_to_add GoogleNetworkServicesEdgeCacheService#request_header_to_add}
        :param request_header_to_remove: request_header_to_remove block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#request_header_to_remove GoogleNetworkServicesEdgeCacheService#request_header_to_remove}
        :param response_header_to_add: response_header_to_add block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#response_header_to_add GoogleNetworkServicesEdgeCacheService#response_header_to_add}
        :param response_header_to_remove: response_header_to_remove block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#response_header_to_remove GoogleNetworkServicesEdgeCacheService#response_header_to_remove}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad259d2080b31de0d8e423f060b440da84673b560a19cf09c4d45471ac04954)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd"]]]:
        '''request_header_to_add block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#request_header_to_add GoogleNetworkServicesEdgeCacheService#request_header_to_add}
        '''
        result = self._values.get("request_header_to_add")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd"]]], result)

    @builtins.property
    def request_header_to_remove(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove"]]]:
        '''request_header_to_remove block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#request_header_to_remove GoogleNetworkServicesEdgeCacheService#request_header_to_remove}
        '''
        result = self._values.get("request_header_to_remove")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove"]]], result)

    @builtins.property
    def response_header_to_add(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd"]]]:
        '''response_header_to_add block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#response_header_to_add GoogleNetworkServicesEdgeCacheService#response_header_to_add}
        '''
        result = self._values.get("response_header_to_add")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd"]]], result)

    @builtins.property
    def response_header_to_remove(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove"]]]:
        '''response_header_to_remove block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#response_header_to_remove GoogleNetworkServicesEdgeCacheService#response_header_to_remove}
        '''
        result = self._values.get("response_header_to_remove")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77dcbbdb09b0cd54d42d5fffb1a4466b96bccf9926b3dafd8566322a1dc7f049)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequestHeaderToAdd")
    def put_request_header_to_add(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04678cefb7b32d61148555246842f25186e99395a9dd7d75bd4cf492ef888ba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeaderToAdd", [value]))

    @jsii.member(jsii_name="putRequestHeaderToRemove")
    def put_request_header_to_remove(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660ccccf47b2b7c34192002dcb886753a7cf29ceafd47f1ae4f8a41a05ceaf98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeaderToRemove", [value]))

    @jsii.member(jsii_name="putResponseHeaderToAdd")
    def put_response_header_to_add(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cfabb3edf80fbd2fe18ffe23bd342b66906c862f122944d502a3f221e7f1502)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResponseHeaderToAdd", [value]))

    @jsii.member(jsii_name="putResponseHeaderToRemove")
    def put_response_header_to_remove(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6233ec642ebfb9a12bc9682bcae1e8ba0c131ed2458281927c3e55a8e6920fda)
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
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddList":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddList", jsii.get(self, "requestHeaderToAdd"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderToRemove")
    def request_header_to_remove(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveList":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveList", jsii.get(self, "requestHeaderToRemove"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderToAdd")
    def response_header_to_add(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddList":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddList", jsii.get(self, "responseHeaderToAdd"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderToRemove")
    def response_header_to_remove(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveList":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveList", jsii.get(self, "responseHeaderToRemove"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderToAddInput")
    def request_header_to_add_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd"]]], jsii.get(self, "requestHeaderToAddInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderToRemoveInput")
    def request_header_to_remove_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove"]]], jsii.get(self, "requestHeaderToRemoveInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderToAddInput")
    def response_header_to_add_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd"]]], jsii.get(self, "responseHeaderToAddInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderToRemoveInput")
    def response_header_to_remove_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove"]]], jsii.get(self, "responseHeaderToRemoveInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d276293b20840835cacd209b8eac7ebd3ac5d198682cd077a5d8ba3ade095ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd",
    jsii_struct_bases=[],
    name_mapping={
        "header_name": "headerName",
        "header_value": "headerValue",
        "replace": "replace",
    },
)
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        header_value: builtins.str,
        replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param header_name: The name of the header to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_name GoogleNetworkServicesEdgeCacheService#header_name}
        :param header_value: The value of the header to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_value GoogleNetworkServicesEdgeCacheService#header_value}
        :param replace: Whether to replace all existing headers with the same name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#replace GoogleNetworkServicesEdgeCacheService#replace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f693683bd8b5c500da68188d8a38689ed6b5c3b03502840e7077de3726de6528)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_name GoogleNetworkServicesEdgeCacheService#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_value(self) -> builtins.str:
        '''The value of the header to add.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_value GoogleNetworkServicesEdgeCacheService#header_value}
        '''
        result = self._values.get("header_value")
        assert result is not None, "Required property 'header_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to replace all existing headers with the same name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#replace GoogleNetworkServicesEdgeCacheService#replace}
        '''
        result = self._values.get("replace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c5104a959f5666f45ddd7eb9c48e45ae9bb23c59f3ee92ce87c626449084ead)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68d3ad1478144fabd8a418073b30a00b32d484067dce04fec54c124d087ef0b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5db799d4a71450ccb46feb2bd6355cfeb204b6cd1a80c9cbc65f7a2af18b64e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01e1c7a4b48df6f41a8ebf821157da5f560632d09f65775d52a7be55b367ddd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__826cf946997df5bee6f7915f5aed694398bbf814e2632a6763876e5da64bb050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee774c7c391d58c46a382f8e5b34af6fd24a9d1b50cc4d767f73b47cbbe9c9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__135dc6eb97e83c52c9072f7a119e8d6026ed926f74863b8b8b8c436d1782d1ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ef4427ae22ed3dc280b700ba07cafa39d709dc42c09d967ece819064706970f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13904679d2a0f707cf778afdb5fa752c3d569f1cb898e19caee61d226c894407)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9031daeff732c7f672fb42b9ea8a500e35da1f6964d0301131a18d6a21796ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b07448c58c37dac1496b2031892907b71d3b6eb22d85b1de9c5de00e89204f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName"},
)
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove:
    def __init__(self, *, header_name: builtins.str) -> None:
        '''
        :param header_name: The name of the header to remove. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_name GoogleNetworkServicesEdgeCacheService#header_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7e846cd7326fd9582c24078cd12f48eea9b56ddcf44d43650d4b417bb87aafe)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
        }

    @builtins.property
    def header_name(self) -> builtins.str:
        '''The name of the header to remove.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_name GoogleNetworkServicesEdgeCacheService#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7b8779491f3fb815cd0cd42e5651cce3c728ee49f8548c4ca0ecc142934a52c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e5efde5c466dbdd2081d5b7a15228389877130782b40bcbf1ae5c8f0456cd8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__782332cc6784439979c153b29c6bfd5e94aa906ab97ee940d33fdace807274d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5740e20d03c9aa672dd3e1837a563d2ef01e9e9d3523460be8f64f9ad3dc7774)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a79360fafa38b24bca14733f022e06e8333e5722f8ccc9d134cb3f9d55cf6d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4525a9b7807d6a10fa96107580d74dcb585b2fd113243f1a89e0b5e870586fa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe3eb3b594f77147e9ec535a22b84e72d82910dbcd59d3702883006586edea3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdf42bb9770692fa63620e542b93eca766a280f9be526d81ef190d5b01e8e63d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd974c1b8245791b3f07fb3b8efd372a6351a9ec37974fe400035abcde0adb82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd",
    jsii_struct_bases=[],
    name_mapping={
        "header_name": "headerName",
        "header_value": "headerValue",
        "replace": "replace",
    },
)
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        header_value: builtins.str,
        replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param header_name: The name of the header to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_name GoogleNetworkServicesEdgeCacheService#header_name}
        :param header_value: The value of the header to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_value GoogleNetworkServicesEdgeCacheService#header_value}
        :param replace: Whether to replace all existing headers with the same name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#replace GoogleNetworkServicesEdgeCacheService#replace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2b4bce8ca6b97e02bf94844da6b387e1e5a7f0ac2804cc22887e919e570309)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_name GoogleNetworkServicesEdgeCacheService#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_value(self) -> builtins.str:
        '''The value of the header to add.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_value GoogleNetworkServicesEdgeCacheService#header_value}
        '''
        result = self._values.get("header_value")
        assert result is not None, "Required property 'header_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to replace all existing headers with the same name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#replace GoogleNetworkServicesEdgeCacheService#replace}
        '''
        result = self._values.get("replace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c649cf37f32e9cf4c93bb82de60fc9994dfdba26b7b5fd5f5991bd08a5a59fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ffaef2529443a501840ae1a17ab064628f00eef6caffdeb37d007d1520eac4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a8d922c6154105283810a5a8393d0b4a831ea14fbe43fd258257bd11b5178c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a44d0053aafea5591d609cbf4d71278ca421b274fd856da08b3fee4809411483)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b47785f1068889963c13969ad99a23a8708fd546c1d1cd7d2a28f3d24c8ef69b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba43a4ab08f812913a480765b4ee600224f603eb6b8b619bda31245a214b130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8294b5992241045f5acb74ca679629f1f135a8e6ea57a54f3c578433436c9041)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1a4ae3683a09792ae907eba8c4d7aa5a44834405b8ae828f5f4b3fafd9baab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58f9c9d2b3cfdb1dd39ca12b01d6043a86e2a748a0345f9173fc7b63949e7b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74bedc56d4ecae832ec39e2be9201a7720435d64a02e2e9940381391e030f07a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df607ee3b4928a0785a67b0f5aac28c7ef55502175099b0cb71fb77f32e49734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName"},
)
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove:
    def __init__(self, *, header_name: builtins.str) -> None:
        '''
        :param header_name: Headers to remove from the response prior to sending it back to the client. Response headers are only sent to the client, and do not have an effect on the cache serving the response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_name GoogleNetworkServicesEdgeCacheService#header_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51a89624458e263e657c3281a74cb6f0f867c963fc595b0c0b6791aacbd4a602)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
        }

    @builtins.property
    def header_name(self) -> builtins.str:
        '''Headers to remove from the response prior to sending it back to the client.

        Response headers are only sent to the client, and do not have an effect on the cache serving the response.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_name GoogleNetworkServicesEdgeCacheService#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56d5816004cacab4b5919dc6e05515c16a35da1b4553ce3b40e647d29b1270b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b3590fa1c55c14e7e6cd9e51ae70708ac69be1dc4c4c7d154a98c4f400f34d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce5b93df7492db4ca3475992c57ecc457fc558deac215f8c31b7c9fc07ec388b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b493383d6f10b65c99169a983b3fc0003de2b6c242a9b170e0c1e6a427a90a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b045bae5819f4df339d519e68559492844f5aa859ad26f5a65c1c4b36aef6099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bbf301294020949347c33193e7d026fb57072f7cc7d9441b31aadcde6ddddf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34128e4d604d04e753484e9fe1f699f1f007df86ee2dc6a011c9cbd819353212)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93f2aa63904c98c2358a56d0720842657ed24d7eb0c212204583590fd1e1fcf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0332047a750e7181260a20cbb327b84e630e08f482fa457a2b4e9d24f4f10e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c90826e3fdc6aa7a1d9e437acc85842c2340fdc26ffa743abd53b962d232203)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1e218ab12221ee25605d3549a5cff539985af51b6e4b7b88151ffd292238e6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f412730b4feee05115be6624c264ca1051d10faa9f582b1a0a4e006ff39e8d36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd683674b57f142377c651cf995965384e8d3524465822beef88993b9eb964f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f1e43f635833eeddf9616060fca2f86114cb36afb19c2110fe2858e7dd50029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0797c4f77ac9e73a32e160368fc300499e3e3c5bc7180ba82b768c14776c46b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule",
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
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule:
    def __init__(
        self,
        *,
        full_path_match: typing.Optional[builtins.str] = None,
        header_match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path_template_match: typing.Optional[builtins.str] = None,
        prefix_match: typing.Optional[builtins.str] = None,
        query_parameter_match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param full_path_match: For satisfying the matchRule condition, the path of the request must exactly match the value specified in fullPathMatch after removing any query parameters and anchor that may be part of the original URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#full_path_match GoogleNetworkServicesEdgeCacheService#full_path_match}
        :param header_match: header_match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_match GoogleNetworkServicesEdgeCacheService#header_match}
        :param ignore_case: Specifies that prefixMatch and fullPathMatch matches are case sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#ignore_case GoogleNetworkServicesEdgeCacheService#ignore_case}
        :param path_template_match: For satisfying the matchRule condition, the path of the request must match the wildcard pattern specified in pathTemplateMatch after removing any query parameters and anchor that may be part of the original URL. pathTemplateMatch must be between 1 and 255 characters (inclusive). The pattern specified by pathTemplateMatch may have at most 5 wildcard operators and at most 5 variable captures in total. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_template_match GoogleNetworkServicesEdgeCacheService#path_template_match}
        :param prefix_match: For satisfying the matchRule condition, the request's path must begin with the specified prefixMatch. prefixMatch must begin with a /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#prefix_match GoogleNetworkServicesEdgeCacheService#prefix_match}
        :param query_parameter_match: query_parameter_match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#query_parameter_match GoogleNetworkServicesEdgeCacheService#query_parameter_match}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37815bbdac74a4da2e07c88bcdb0c2bbc9e970a331f9db937edf35fa16e7b06)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#full_path_match GoogleNetworkServicesEdgeCacheService#full_path_match}
        '''
        result = self._values.get("full_path_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_match(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch"]]]:
        '''header_match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_match GoogleNetworkServicesEdgeCacheService#header_match}
        '''
        result = self._values.get("header_match")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch"]]], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies that prefixMatch and fullPathMatch matches are case sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#ignore_case GoogleNetworkServicesEdgeCacheService#ignore_case}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_template_match GoogleNetworkServicesEdgeCacheService#path_template_match}
        '''
        result = self._values.get("path_template_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix_match(self) -> typing.Optional[builtins.str]:
        '''For satisfying the matchRule condition, the request's path must begin with the specified prefixMatch.

        prefixMatch must begin with a /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#prefix_match GoogleNetworkServicesEdgeCacheService#prefix_match}
        '''
        result = self._values.get("prefix_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_parameter_match(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch"]]]:
        '''query_parameter_match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#query_parameter_match GoogleNetworkServicesEdgeCacheService#query_parameter_match}
        '''
        result = self._values.get("query_parameter_match")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch",
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
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch:
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
        :param header_name: The header name to match on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_name GoogleNetworkServicesEdgeCacheService#header_name}
        :param exact_match: The value of the header should exactly match contents of exactMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#exact_match GoogleNetworkServicesEdgeCacheService#exact_match}
        :param invert_match: If set to false (default), the headerMatch is considered a match if the match criteria above are met. If set to true, the headerMatch is considered a match if the match criteria above are NOT met. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#invert_match GoogleNetworkServicesEdgeCacheService#invert_match}
        :param prefix_match: The value of the header must start with the contents of prefixMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#prefix_match GoogleNetworkServicesEdgeCacheService#prefix_match}
        :param present_match: A header with the contents of headerName must exist. The match takes place whether or not the request's header has a value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#present_match GoogleNetworkServicesEdgeCacheService#present_match}
        :param suffix_match: The value of the header must end with the contents of suffixMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#suffix_match GoogleNetworkServicesEdgeCacheService#suffix_match}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a16fe890e740ceae6bdec9c383c091338442cefee3425fe16488339df8dc30c7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#header_name GoogleNetworkServicesEdgeCacheService#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exact_match(self) -> typing.Optional[builtins.str]:
        '''The value of the header should exactly match contents of exactMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#exact_match GoogleNetworkServicesEdgeCacheService#exact_match}
        '''
        result = self._values.get("exact_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to false (default), the headerMatch is considered a match if the match criteria above are met.

        If set to true, the headerMatch is considered a match if the match criteria above are NOT met.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#invert_match GoogleNetworkServicesEdgeCacheService#invert_match}
        '''
        result = self._values.get("invert_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix_match(self) -> typing.Optional[builtins.str]:
        '''The value of the header must start with the contents of prefixMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#prefix_match GoogleNetworkServicesEdgeCacheService#prefix_match}
        '''
        result = self._values.get("prefix_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def present_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A header with the contents of headerName must exist.

        The match takes place whether or not the request's header has a value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#present_match GoogleNetworkServicesEdgeCacheService#present_match}
        '''
        result = self._values.get("present_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def suffix_match(self) -> typing.Optional[builtins.str]:
        '''The value of the header must end with the contents of suffixMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#suffix_match GoogleNetworkServicesEdgeCacheService#suffix_match}
        '''
        result = self._values.get("suffix_match")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1d828c5e68baaebfb91c6df5f424f995413d0acdd972dc042646c6caa767894)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ea5b6aa6208976b2b0a4c2c929001804d56f6fe0a441c80415eeb789cc5ea5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f38d95c9aa99fbd552f8c1410533b817d4b38b63eba9caa7fda8228022e18ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c29c331ce8e8ec1aba442f71938e55c04ff8886dabccb350894dee477c42f62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__488804cff9d8d6a3a274ce4adfa2b56623510fb49b7e230b6ec1670e7aaf7848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06eb2dea80a98c528fc061b17384e640123bc66b93c822ff5dbe70e0764520c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c180dcb4383deb19a89a0d9c4e8213a84eebfb83d7ee566d2968dc3438d4a36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4a3c622f5d97804d90db357afa0c9a56173f3ce8d275edca523f42a03d3585b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exactMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16832b3d99d12da6d6d5409b018dd5feef2d47a0fdc217ef6265ae515aea3b24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40fc37b0a4c23431ec81d892e7d1dc5d6356ef491e44b3fcacc4c5b5937300c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixMatch")
    def prefix_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixMatch"))

    @prefix_match.setter
    def prefix_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__093129cb6ae6f2ffffbbd59b8106c035c3f218afd68dd9eb0fa8bbac09ed942a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__116f20dac6d55a87cb82e3c7456d74ea38ab3f8315754c511f5254bd36712481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "presentMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffixMatch")
    def suffix_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffixMatch"))

    @suffix_match.setter
    def suffix_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18f2d9b18f1dd0c4ce067934af93ba563e29a671cb694ec2c324c682d3cee52e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffixMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf08bde1af11afb238290446f4259b4d0ea642895bfabfe328e2aefbf171da90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__261d9567c05b533195f9b394988b58f24f034ef4511ada4db2f1e7562be8c491)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d6f1e6eb0aa0e430e32daabaa16b09596f597ff50f1ddc8d2514a26a71c854d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348afa39271cb759910c88ffd757dcd8d043bac7b64b812857b2ddb8cbc43a81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1251b342822fe518830d715755fa6a8858a2ce66a02d6110515b9297f4365c4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8813d3c1bbf6a2811d7a603eb0b8147c000394d4862bbdf45df9148b7c90466e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c4c6014edd6a83cb9a6e3fce70f46758a09970482a1d97d1df19cb37864e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e2f2aabc8772a90718b0f20ad83d050a24569aeda1ee35af1dee27791be84fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaderMatch")
    def put_header_match(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0af41a12337585aabf1c14a8b809b4511a1fa0dd7c407fd33ee35935177d029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaderMatch", [value]))

    @jsii.member(jsii_name="putQueryParameterMatch")
    def put_query_parameter_match(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d042b40a29f3bc350742e7c3a2534afad9a674020ea6b5f167c7b4fc30b557)
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
    ) -> GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchList:
        return typing.cast(GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchList, jsii.get(self, "headerMatch"))

    @builtins.property
    @jsii.member(jsii_name="queryParameterMatch")
    def query_parameter_match(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchList":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchList", jsii.get(self, "queryParameterMatch"))

    @builtins.property
    @jsii.member(jsii_name="fullPathMatchInput")
    def full_path_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fullPathMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="headerMatchInput")
    def header_match_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]], jsii.get(self, "headerMatchInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch"]]], jsii.get(self, "queryParameterMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="fullPathMatch")
    def full_path_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullPathMatch"))

    @full_path_match.setter
    def full_path_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8594830d505942724f72764182bcd7c65ca7946b7fd368f2de680644a3c6735b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c35d165caeef4cbc51e720a607b308c111f5111602caafdc027a4f90921e6a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathTemplateMatch")
    def path_template_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathTemplateMatch"))

    @path_template_match.setter
    def path_template_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce031371b0f3800656cdfc4491b788d47eabbd29f6ef904999b3f5e89211bb40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathTemplateMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixMatch")
    def prefix_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixMatch"))

    @prefix_match.setter
    def prefix_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b58817ffa45b43ba1c37853253dba1bd371d758697e83b9129270030b92c709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e23a4ee2346be56eb3534741211a891447706534e657c64c51dc828ac71908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "exact_match": "exactMatch",
        "present_match": "presentMatch",
    },
)
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch:
    def __init__(
        self,
        *,
        name: builtins.str,
        exact_match: typing.Optional[builtins.str] = None,
        present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: The name of the query parameter to match. The query parameter must exist in the request, in the absence of which the request match fails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#name GoogleNetworkServicesEdgeCacheService#name}
        :param exact_match: The queryParameterMatch matches if the value of the parameter exactly matches the contents of exactMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#exact_match GoogleNetworkServicesEdgeCacheService#exact_match}
        :param present_match: Specifies that the queryParameterMatch matches if the request contains the query parameter, irrespective of whether the parameter has a value or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#present_match GoogleNetworkServicesEdgeCacheService#present_match}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49feb5985d69c7e57f29075e4d73c2f139072825a1bb8ec31fddbfe51eb7bd99)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#name GoogleNetworkServicesEdgeCacheService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exact_match(self) -> typing.Optional[builtins.str]:
        '''The queryParameterMatch matches if the value of the parameter exactly matches the contents of exactMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#exact_match GoogleNetworkServicesEdgeCacheService#exact_match}
        '''
        result = self._values.get("exact_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def present_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies that the queryParameterMatch matches if the request contains the query parameter, irrespective of whether the parameter has a value or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#present_match GoogleNetworkServicesEdgeCacheService#present_match}
        '''
        result = self._values.get("present_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b112a739e91297a61a3175bcc6fe5ef2bf6db6f8941b346210c4b7c79c310825)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b8cf4a164ef53eed3da6f8da75232016bbffa0eb09e9ad6c6a31b8ec7fc72fb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82eadbbc2e37e10ae87ca1f5a84f7a74b58351f615308764c34e2959605e72b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f11b1b82bb99e7386ae1410bf91da8848278808e2702e54560ca0a7413c8b8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c26d081aa6a238cf5e7b20337d4ea3b9f20b28c3b029ee019593ea429efbd0e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df188a503e1adff2c24a0d0a869380b73e6f6fcec4930ef486180e36797f72c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b62e56d46bf22a58d9376febc5e1a8992b151e3a16ec221bad08ca30b7249b7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54a9efc0374d91dffc7e2168c4dae7feec4ae37fc4371300a2b7f7bfb3c26b10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exactMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e67d73df26c127fed720cebe298554b57a98354f3bb107153a15fbca8f42b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8205757f7ed228a2adbf5465cc36496f0fe7a3a0c1e7df86fa4e27a8865dca06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "presentMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83867eb79bd59a16f6c29ea776df76165f6ef766239d42492b22110be9d55c7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__243f111f680eb53ba4827321115e503e0091caf1723060fdbfb52d09b6e2bcde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaderAction")
    def put_header_action(
        self,
        *,
        request_header_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd, typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header_to_remove: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove, typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_header_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd, typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_header_to_remove: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param request_header_to_add: request_header_to_add block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#request_header_to_add GoogleNetworkServicesEdgeCacheService#request_header_to_add}
        :param request_header_to_remove: request_header_to_remove block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#request_header_to_remove GoogleNetworkServicesEdgeCacheService#request_header_to_remove}
        :param response_header_to_add: response_header_to_add block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#response_header_to_add GoogleNetworkServicesEdgeCacheService#response_header_to_add}
        :param response_header_to_remove: response_header_to_remove block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#response_header_to_remove GoogleNetworkServicesEdgeCacheService#response_header_to_remove}
        '''
        value = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction(
            request_header_to_add=request_header_to_add,
            request_header_to_remove=request_header_to_remove,
            response_header_to_add=response_header_to_add,
            response_header_to_remove=response_header_to_remove,
        )

        return typing.cast(None, jsii.invoke(self, "putHeaderAction", [value]))

    @jsii.member(jsii_name="putMatchRule")
    def put_match_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1360515de542824c104cbf5d438fba2f57eeaaa67bda84ccdeb442aa055adb52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchRule", [value]))

    @jsii.member(jsii_name="putRouteAction")
    def put_route_action(
        self,
        *,
        cdn_policy: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_mode: typing.Optional[builtins.str] = None,
        cors_policy: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        url_rewrite: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#cdn_policy GoogleNetworkServicesEdgeCacheService#cdn_policy}
        :param compression_mode: Setting the compression mode to automatic enables dynamic compression for every eligible response. When dynamic compression is enabled, it is recommended to also set a cache policy to maximize efficiency. Possible values: ["DISABLED", "AUTOMATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#compression_mode GoogleNetworkServicesEdgeCacheService#compression_mode}
        :param cors_policy: cors_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#cors_policy GoogleNetworkServicesEdgeCacheService#cors_policy}
        :param url_rewrite: url_rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#url_rewrite GoogleNetworkServicesEdgeCacheService#url_rewrite}
        '''
        value = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction(
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
        :param allowed_methods: The non-empty set of HTTP methods that are allowed for this route. Any combination of "GET", "HEAD", "OPTIONS", "PUT", "POST", "DELETE", and "PATCH". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allowed_methods GoogleNetworkServicesEdgeCacheService#allowed_methods}
        '''
        value = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods(
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
        :param host_redirect: The host that will be used in the redirect response instead of the one that was supplied in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#host_redirect GoogleNetworkServicesEdgeCacheService#host_redirect}
        :param https_redirect: If set to true, the URL scheme in the redirected request is set to https. If set to false, the URL scheme of the redirected request will remain the same as that of the request. This can only be set if there is at least one (1) edgeSslCertificate set on the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#https_redirect GoogleNetworkServicesEdgeCacheService#https_redirect}
        :param path_redirect: The path that will be used in the redirect response instead of the one that was supplied in the request. pathRedirect cannot be supplied together with prefixRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect. The path value must be between 1 and 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_redirect GoogleNetworkServicesEdgeCacheService#path_redirect}
        :param prefix_redirect: The prefix that replaces the prefixMatch specified in the routeRule, retaining the remaining portion of the URL before redirecting the request. prefixRedirect cannot be supplied together with pathRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#prefix_redirect GoogleNetworkServicesEdgeCacheService#prefix_redirect}
        :param redirect_response_code: The HTTP Status code to use for this RedirectAction. The supported values are: - 'MOVED_PERMANENTLY_DEFAULT', which is the default value and corresponds to 301. - 'FOUND', which corresponds to 302. - 'SEE_OTHER' which corresponds to 303. - 'TEMPORARY_REDIRECT', which corresponds to 307. in this case, the request method will be retained. - 'PERMANENT_REDIRECT', which corresponds to 308. in this case, the request method will be retained. Possible values: ["MOVED_PERMANENTLY_DEFAULT", "FOUND", "SEE_OTHER", "TEMPORARY_REDIRECT", "PERMANENT_REDIRECT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#redirect_response_code GoogleNetworkServicesEdgeCacheService#redirect_response_code}
        :param strip_query: If set to true, any accompanying query portion of the original URL is removed prior to redirecting the request. If set to false, the query portion of the original URL is retained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#strip_query GoogleNetworkServicesEdgeCacheService#strip_query}
        '''
        value = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect(
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
    ) -> GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionOutputReference:
        return typing.cast(GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionOutputReference, jsii.get(self, "headerAction"))

    @builtins.property
    @jsii.member(jsii_name="matchRule")
    def match_rule(
        self,
    ) -> GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleList:
        return typing.cast(GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleList, jsii.get(self, "matchRule"))

    @builtins.property
    @jsii.member(jsii_name="routeAction")
    def route_action(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionOutputReference", jsii.get(self, "routeAction"))

    @builtins.property
    @jsii.member(jsii_name="routeMethods")
    def route_methods(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethodsOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethodsOutputReference", jsii.get(self, "routeMethods"))

    @builtins.property
    @jsii.member(jsii_name="urlRedirect")
    def url_redirect(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirectOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirectOutputReference", jsii.get(self, "urlRedirect"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="headerActionInput")
    def header_action_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction], jsii.get(self, "headerActionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchRuleInput")
    def match_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]], jsii.get(self, "matchRuleInput"))

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
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction"], jsii.get(self, "routeActionInput"))

    @builtins.property
    @jsii.member(jsii_name="routeMethodsInput")
    def route_methods_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods"], jsii.get(self, "routeMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRedirectInput")
    def url_redirect_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect"], jsii.get(self, "urlRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d673df92f7da8700be99c4b2532a34b84026c375315a4c5ac74dfabbf31f8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "origin"))

    @origin.setter
    def origin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__315157c33997c038cff0bb18d05050c1f028adcff4419810da2c119136e405e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "origin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__256415a32135bc3d4a22f335c2aa04aca673c4bd08f4d7dc9a278cb243d0a5f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933fb0e7d018bc41d9d23216d8f1075b307cbb42d390e0c5cd3ea10a0dbb4e0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction",
    jsii_struct_bases=[],
    name_mapping={
        "cdn_policy": "cdnPolicy",
        "compression_mode": "compressionMode",
        "cors_policy": "corsPolicy",
        "url_rewrite": "urlRewrite",
    },
)
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction:
    def __init__(
        self,
        *,
        cdn_policy: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_mode: typing.Optional[builtins.str] = None,
        cors_policy: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        url_rewrite: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#cdn_policy GoogleNetworkServicesEdgeCacheService#cdn_policy}
        :param compression_mode: Setting the compression mode to automatic enables dynamic compression for every eligible response. When dynamic compression is enabled, it is recommended to also set a cache policy to maximize efficiency. Possible values: ["DISABLED", "AUTOMATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#compression_mode GoogleNetworkServicesEdgeCacheService#compression_mode}
        :param cors_policy: cors_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#cors_policy GoogleNetworkServicesEdgeCacheService#cors_policy}
        :param url_rewrite: url_rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#url_rewrite GoogleNetworkServicesEdgeCacheService#url_rewrite}
        '''
        if isinstance(cdn_policy, dict):
            cdn_policy = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy(**cdn_policy)
        if isinstance(cors_policy, dict):
            cors_policy = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy(**cors_policy)
        if isinstance(url_rewrite, dict):
            url_rewrite = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite(**url_rewrite)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36f8c89de1303f2eecdfae1b84e976259c08490b98cb7947b3588aa04549cf5)
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
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy"]:
        '''cdn_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#cdn_policy GoogleNetworkServicesEdgeCacheService#cdn_policy}
        '''
        result = self._values.get("cdn_policy")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy"], result)

    @builtins.property
    def compression_mode(self) -> typing.Optional[builtins.str]:
        '''Setting the compression mode to automatic enables dynamic compression for every eligible response.

        When dynamic compression is enabled, it is recommended to also set a cache policy to maximize efficiency. Possible values: ["DISABLED", "AUTOMATIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#compression_mode GoogleNetworkServicesEdgeCacheService#compression_mode}
        '''
        result = self._values.get("compression_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors_policy(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy"]:
        '''cors_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#cors_policy GoogleNetworkServicesEdgeCacheService#cors_policy}
        '''
        result = self._values.get("cors_policy")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy"], result)

    @builtins.property
    def url_rewrite(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite"]:
        '''url_rewrite block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#url_rewrite GoogleNetworkServicesEdgeCacheService#url_rewrite}
        '''
        result = self._values.get("url_rewrite")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy",
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
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy:
    def __init__(
        self,
        *,
        add_signatures: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_key_policy: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[builtins.str] = None,
        default_ttl: typing.Optional[builtins.str] = None,
        max_ttl: typing.Optional[builtins.str] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        signed_request_keyset: typing.Optional[builtins.str] = None,
        signed_request_maximum_expiration_ttl: typing.Optional[builtins.str] = None,
        signed_request_mode: typing.Optional[builtins.str] = None,
        signed_token_options: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param add_signatures: add_signatures block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#add_signatures GoogleNetworkServicesEdgeCacheService#add_signatures}
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#cache_key_policy GoogleNetworkServicesEdgeCacheService#cache_key_policy}
        :param cache_mode: Cache modes allow users to control the behaviour of the cache, what content it should cache automatically, whether to respect origin headers, or whether to unconditionally cache all responses. For all cache modes, Cache-Control headers will be passed to the client. Use clientTtl to override what is sent to the client. Possible values: ["CACHE_ALL_STATIC", "USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "BYPASS_CACHE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#cache_mode GoogleNetworkServicesEdgeCacheService#cache_mode}
        :param client_ttl: Specifies a separate client (e.g. browser client) TTL, separate from the TTL used by the edge caches. Leaving this empty will use the same cache TTL for both the CDN and the client-facing response. - The TTL must be > 0 and <= 86400s (1 day) - The clientTtl cannot be larger than the defaultTtl (if set) - Fractions of a second are not allowed. Omit this field to use the defaultTtl, or the max-age set by the origin, as the client-facing TTL. When the cache mode is set to "USE_ORIGIN_HEADERS" or "BYPASS_CACHE", you must omit this field. A duration in seconds terminated by 's'. Example: "3s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#client_ttl GoogleNetworkServicesEdgeCacheService#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). Defaults to 3600s (1 hour). - The TTL must be >= 0 and <= 31,536,000 seconds (1 year) - Setting a TTL of "0" means "always revalidate" (equivalent to must-revalidate) - The value of defaultTTL cannot be set to a value greater than that of maxTTL. - Fractions of a second are not allowed. - When the cacheMode is set to FORCE_CACHE_ALL, the defaultTTL will overwrite the TTL set in all responses. Note that infrequently accessed objects may be evicted from the cache before the defined TTL. Objects that expire will be revalidated with the origin. When the cache mode is set to "USE_ORIGIN_HEADERS" or "BYPASS_CACHE", you must omit this field. A duration in seconds terminated by 's'. Example: "3s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#default_ttl GoogleNetworkServicesEdgeCacheService#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Defaults to 86400s (1 day). Cache directives that attempt to set a max-age or s-maxage higher than this, or an Expires header more than maxTtl seconds in the future will be capped at the value of maxTTL, as if it were the value of an s-maxage Cache-Control directive. - The TTL must be >= 0 and <= 31,536,000 seconds (1 year) - Setting a TTL of "0" means "always revalidate" - The value of maxTtl must be equal to or greater than defaultTtl. - Fractions of a second are not allowed. When the cache mode is set to "USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", or "BYPASS_CACHE", you must omit this field. A duration in seconds terminated by 's'. Example: "3s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#max_ttl GoogleNetworkServicesEdgeCacheService#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. This can reduce the load on your origin and improve end-user experience by reducing response latency. By default, the CDNPolicy will apply the following default TTLs to these status codes: - HTTP 300 (Multiple Choice), 301, 308 (Permanent Redirects): 10m - HTTP 404 (Not Found), 410 (Gone), 451 (Unavailable For Legal Reasons): 120s - HTTP 405 (Method Not Found), 414 (URI Too Long), 501 (Not Implemented): 60s These defaults can be overridden in negativeCachingPolicy Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#negative_caching GoogleNetworkServicesEdgeCacheService#negative_caching}
        :param negative_caching_policy: Sets a cache TTL for the specified HTTP status code. negativeCaching must be enabled to configure negativeCachingPolicy. - Omitting the policy and leaving negativeCaching enabled will use the default TTLs for each status code, defined in negativeCaching. - TTLs must be >= 0 (where 0 is "always revalidate") and <= 86400s (1 day) Note that when specifying an explicit negativeCachingPolicy, you should take care to specify a cache TTL for all response codes that you wish to cache. The CDNPolicy will not apply any default negative caching when a policy exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#negative_caching_policy GoogleNetworkServicesEdgeCacheService#negative_caching_policy}
        :param signed_request_keyset: The EdgeCacheKeyset containing the set of public keys used to validate signed requests at the edge. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#signed_request_keyset GoogleNetworkServicesEdgeCacheService#signed_request_keyset}
        :param signed_request_maximum_expiration_ttl: Limit how far into the future the expiration time of a signed request may be. When set, a signed request is rejected if its expiration time is later than now + signedRequestMaximumExpirationTtl, where now is the time at which the signed request is first handled by the CDN. - The TTL must be > 0. - Fractions of a second are not allowed. By default, signedRequestMaximumExpirationTtl is not set and the expiration time of a signed request may be arbitrarily far into future. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#signed_request_maximum_expiration_ttl GoogleNetworkServicesEdgeCacheService#signed_request_maximum_expiration_ttl}
        :param signed_request_mode: Whether to enforce signed requests. The default value is DISABLED, which means all content is public, and does not authorize access. You must also set a signedRequestKeyset to enable signed requests. When set to REQUIRE_SIGNATURES, all matching requests will have their signature validated. Requests that were not signed with the corresponding private key, or that are otherwise invalid (expired, do not match the signature, IP address, or header) will be rejected with a HTTP 403 and (if enabled) logged. Possible values: ["DISABLED", "REQUIRE_SIGNATURES", "REQUIRE_TOKENS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#signed_request_mode GoogleNetworkServicesEdgeCacheService#signed_request_mode}
        :param signed_token_options: signed_token_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#signed_token_options GoogleNetworkServicesEdgeCacheService#signed_token_options}
        '''
        if isinstance(add_signatures, dict):
            add_signatures = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures(**add_signatures)
        if isinstance(cache_key_policy, dict):
            cache_key_policy = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy(**cache_key_policy)
        if isinstance(signed_token_options, dict):
            signed_token_options = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions(**signed_token_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cdadd22ef08d7d0f2c911a9f563af9e1a55a06422c87c5cd832e28b461e2d31)
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
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures"]:
        '''add_signatures block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#add_signatures GoogleNetworkServicesEdgeCacheService#add_signatures}
        '''
        result = self._values.get("add_signatures")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures"], result)

    @builtins.property
    def cache_key_policy(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy"]:
        '''cache_key_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#cache_key_policy GoogleNetworkServicesEdgeCacheService#cache_key_policy}
        '''
        result = self._values.get("cache_key_policy")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy"], result)

    @builtins.property
    def cache_mode(self) -> typing.Optional[builtins.str]:
        '''Cache modes allow users to control the behaviour of the cache, what content it should cache automatically, whether to respect origin headers, or whether to unconditionally cache all responses.

        For all cache modes, Cache-Control headers will be passed to the client. Use clientTtl to override what is sent to the client. Possible values: ["CACHE_ALL_STATIC", "USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "BYPASS_CACHE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#cache_mode GoogleNetworkServicesEdgeCacheService#cache_mode}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#client_ttl GoogleNetworkServicesEdgeCacheService#client_ttl}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#default_ttl GoogleNetworkServicesEdgeCacheService#default_ttl}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#max_ttl GoogleNetworkServicesEdgeCacheService#max_ttl}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#negative_caching GoogleNetworkServicesEdgeCacheService#negative_caching}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#negative_caching_policy GoogleNetworkServicesEdgeCacheService#negative_caching_policy}
        '''
        result = self._values.get("negative_caching_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def signed_request_keyset(self) -> typing.Optional[builtins.str]:
        '''The EdgeCacheKeyset containing the set of public keys used to validate signed requests at the edge.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#signed_request_keyset GoogleNetworkServicesEdgeCacheService#signed_request_keyset}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#signed_request_maximum_expiration_ttl GoogleNetworkServicesEdgeCacheService#signed_request_maximum_expiration_ttl}
        '''
        result = self._values.get("signed_request_maximum_expiration_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signed_request_mode(self) -> typing.Optional[builtins.str]:
        '''Whether to enforce signed requests.

        The default value is DISABLED, which means all content is public, and does not authorize access.

        You must also set a signedRequestKeyset to enable signed requests.

        When set to REQUIRE_SIGNATURES, all matching requests will have their signature validated. Requests that were not signed with the corresponding private key, or that are otherwise invalid (expired, do not match the signature, IP address, or header) will be rejected with a HTTP 403 and (if enabled) logged. Possible values: ["DISABLED", "REQUIRE_SIGNATURES", "REQUIRE_TOKENS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#signed_request_mode GoogleNetworkServicesEdgeCacheService#signed_request_mode}
        '''
        result = self._values.get("signed_request_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signed_token_options(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions"]:
        '''signed_token_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#signed_token_options GoogleNetworkServicesEdgeCacheService#signed_token_options}
        '''
        result = self._values.get("signed_token_options")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "copied_parameters": "copiedParameters",
        "keyset": "keyset",
        "token_query_parameter": "tokenQueryParameter",
        "token_ttl": "tokenTtl",
    },
)
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures:
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
        :param actions: The actions to take to add signatures to responses. Possible values: ["GENERATE_COOKIE", "GENERATE_TOKEN_HLS_COOKIELESS", "PROPAGATE_TOKEN_HLS_COOKIELESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#actions GoogleNetworkServicesEdgeCacheService#actions}
        :param copied_parameters: The parameters to copy from the verified token to the generated token. Only the following parameters may be copied: - 'PathGlobs' - 'paths' - 'acl' - 'URLPrefix' - 'IPRanges' - 'SessionID' - 'id' - 'Data' - 'data' - 'payload' - 'Headers' You may specify up to 6 parameters to copy. A given parameter is be copied only if the parameter exists in the verified token. Parameter names are matched exactly as specified. The order of the parameters does not matter. Duplicates are not allowed. This field may only be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#copied_parameters GoogleNetworkServicesEdgeCacheService#copied_parameters}
        :param keyset: The keyset to use for signature generation. The following are both valid paths to an EdgeCacheKeyset resource: - 'projects/project/locations/global/edgeCacheKeysets/yourKeyset' - 'yourKeyset' This must be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified. This field may not be specified otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#keyset GoogleNetworkServicesEdgeCacheService#keyset}
        :param token_query_parameter: The query parameter in which to put the generated token. If not specified, defaults to 'edge-cache-token'. If specified, the name must be 1-64 characters long and match the regular expression '`a-zA-Z <%5Ba-zA-Z0-9_-%5D>`_*' which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. This field may only be set when the GENERATE_TOKEN_HLS_COOKIELESS or PROPAGATE_TOKEN_HLS_COOKIELESS actions are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#token_query_parameter GoogleNetworkServicesEdgeCacheService#token_query_parameter}
        :param token_ttl: The duration the token is valid starting from the moment the token is first generated. Defaults to '86400s' (1 day). The TTL must be >= 0 and <= 604,800 seconds (1 week). This field may only be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#token_ttl GoogleNetworkServicesEdgeCacheService#token_ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e82300efe148ea95bf5bd37de3b72485f5fec6ada57d1e488745b21b016423c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#actions GoogleNetworkServicesEdgeCacheService#actions}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#copied_parameters GoogleNetworkServicesEdgeCacheService#copied_parameters}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#keyset GoogleNetworkServicesEdgeCacheService#keyset}
        '''
        result = self._values.get("keyset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_query_parameter(self) -> typing.Optional[builtins.str]:
        '''The query parameter in which to put the generated token.

        If not specified, defaults to 'edge-cache-token'.

        If specified, the name must be 1-64 characters long and match the regular expression '`a-zA-Z <%5Ba-zA-Z0-9_-%5D>`_*' which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit.

        This field may only be set when the GENERATE_TOKEN_HLS_COOKIELESS or PROPAGATE_TOKEN_HLS_COOKIELESS actions are specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#token_query_parameter GoogleNetworkServicesEdgeCacheService#token_query_parameter}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#token_ttl GoogleNetworkServicesEdgeCacheService#token_ttl}
        '''
        result = self._values.get("token_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbc75c802e36dfc84ddba72d4fc16f93ba1c1811f763f1efb0174bddb71c15e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4f69598d42a61ff71c754526e0bcbc71a95cf496f23bff556324a45838b28b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="copiedParameters")
    def copied_parameters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "copiedParameters"))

    @copied_parameters.setter
    def copied_parameters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57162ec015ee0e912df6cd91b23dae5272435d9afdd6833bd0084715ebf2d002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copiedParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyset")
    def keyset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyset"))

    @keyset.setter
    def keyset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c6cb89fabe1fa9d3efd9ff98a009b7df29c6993ac82921f1764fd5f22e2735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenQueryParameter")
    def token_query_parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenQueryParameter"))

    @token_query_parameter.setter
    def token_query_parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ef74abf47cee9ce3755ab7cc4292644c1cb4207abcd43be5a5bba6dc00372e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenQueryParameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenTtl")
    def token_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenTtl"))

    @token_ttl.setter
    def token_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e864b2cbf1a984129ff3f575c90d9a6668d9e4b11ac31d8bb7928c653d5ba280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dfacaa84f32d1a7c1eea030efeac04e06c721f1e5917c43afcf5e4eabc88eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy",
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
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy:
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
        :param excluded_query_parameters: Names of query string parameters to exclude from cache keys. All other parameters will be included. Either specify includedQueryParameters or excludedQueryParameters, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#excluded_query_parameters GoogleNetworkServicesEdgeCacheService#excluded_query_parameters}
        :param exclude_host: If true, requests to different hosts will be cached separately. Note: this should only be enabled if hosts share the same origin and content. Removing the host from the cache key may inadvertently result in different objects being cached than intended, depending on which route the first user matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#exclude_host GoogleNetworkServicesEdgeCacheService#exclude_host}
        :param exclude_query_string: If true, exclude query string parameters from the cache key. If false (the default), include the query string parameters in the cache key according to includeQueryParameters and excludeQueryParameters. If neither includeQueryParameters nor excludeQueryParameters is set, the entire query string will be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#exclude_query_string GoogleNetworkServicesEdgeCacheService#exclude_query_string}
        :param included_cookie_names: Names of Cookies to include in cache keys. The cookie name and cookie value of each cookie named will be used as part of the cache key. Cookie names: - must be valid RFC 6265 "cookie-name" tokens - are case sensitive - cannot start with "Edge-Cache-" (case insensitive) Note that specifying several cookies, and/or cookies that have a large range of values (e.g., per-user) will dramatically impact the cache hit rate, and may result in a higher eviction rate and reduced performance. You may specify up to three cookie names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#included_cookie_names GoogleNetworkServicesEdgeCacheService#included_cookie_names}
        :param included_header_names: Names of HTTP request headers to include in cache keys. The value of the header field will be used as part of the cache key. - Header names must be valid HTTP RFC 7230 header field values. - Header field names are case insensitive - To include the HTTP method, use ":method" Note that specifying several headers, and/or headers that have a large range of values (e.g. per-user) will dramatically impact the cache hit rate, and may result in a higher eviction rate and reduced performance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#included_header_names GoogleNetworkServicesEdgeCacheService#included_header_names}
        :param included_query_parameters: Names of query string parameters to include in cache keys. All other parameters will be excluded. Either specify includedQueryParameters or excludedQueryParameters, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#included_query_parameters GoogleNetworkServicesEdgeCacheService#included_query_parameters}
        :param include_protocol: If true, http and https requests will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#include_protocol GoogleNetworkServicesEdgeCacheService#include_protocol}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de9b88fd261e0a4b1e59acd3a380064ab24ce0cfee4d6c1e2441087d213ec54)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#excluded_query_parameters GoogleNetworkServicesEdgeCacheService#excluded_query_parameters}
        '''
        result = self._values.get("excluded_query_parameters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclude_host(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, requests to different hosts will be cached separately.

        Note: this should only be enabled if hosts share the same origin and content. Removing the host from the cache key may inadvertently result in different objects being cached than intended, depending on which route the first user matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#exclude_host GoogleNetworkServicesEdgeCacheService#exclude_host}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#exclude_query_string GoogleNetworkServicesEdgeCacheService#exclude_query_string}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#included_cookie_names GoogleNetworkServicesEdgeCacheService#included_cookie_names}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#included_header_names GoogleNetworkServicesEdgeCacheService#included_header_names}
        '''
        result = self._values.get("included_header_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_query_parameters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of query string parameters to include in cache keys. All other parameters will be excluded.

        Either specify includedQueryParameters or excludedQueryParameters, not both. '&' and '=' will be percent encoded and not treated as delimiters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#included_query_parameters GoogleNetworkServicesEdgeCacheService#included_query_parameters}
        '''
        result = self._values.get("included_query_parameters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, http and https requests will be cached separately.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#include_protocol GoogleNetworkServicesEdgeCacheService#include_protocol}
        '''
        result = self._values.get("include_protocol")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__751658f6e1a260c1379263c2a5379354c3a3521bc26756a966df121d9d37cf02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a7f9de346f04bce230f32e895f0aba2ee55f3814102ce45fa8ad8c10ee11548)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9555b799d293b605efda97f9511399dc9a90f22f29a1e8aa74fb1af4326adf5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62b8e96db956d2e2549a23c11397560e51118cdd91e6ac06a2255a826183526e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeQueryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedCookieNames")
    def included_cookie_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedCookieNames"))

    @included_cookie_names.setter
    def included_cookie_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5242df465aefa14167ecda9b313b612f69cac76a6a11fc08b0c61e99a53eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedCookieNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedHeaderNames")
    def included_header_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedHeaderNames"))

    @included_header_names.setter
    def included_header_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331da7b74806f249a03a216cf3f39fd00ab7ab7c04171ae82551b045936e978c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedHeaderNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedQueryParameters")
    def included_query_parameters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedQueryParameters"))

    @included_query_parameters.setter
    def included_query_parameters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd3d80680eba91e7e0c396514213b1fa573f71ae0b38c25c2f1dc4c63bc7808)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aab34461d7cfab89988d4d92eae6e2196cbe7b4243d75197d945e0c7c1a4846d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8df2c446c640aed1de92e6f08c28e03b298fd97a9b8968695ab226ef26797af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a96d4b6539023c7d3fcb8542a969cf13646f8c57901cccd6f8099deb091a63de)
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
        :param actions: The actions to take to add signatures to responses. Possible values: ["GENERATE_COOKIE", "GENERATE_TOKEN_HLS_COOKIELESS", "PROPAGATE_TOKEN_HLS_COOKIELESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#actions GoogleNetworkServicesEdgeCacheService#actions}
        :param copied_parameters: The parameters to copy from the verified token to the generated token. Only the following parameters may be copied: - 'PathGlobs' - 'paths' - 'acl' - 'URLPrefix' - 'IPRanges' - 'SessionID' - 'id' - 'Data' - 'data' - 'payload' - 'Headers' You may specify up to 6 parameters to copy. A given parameter is be copied only if the parameter exists in the verified token. Parameter names are matched exactly as specified. The order of the parameters does not matter. Duplicates are not allowed. This field may only be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#copied_parameters GoogleNetworkServicesEdgeCacheService#copied_parameters}
        :param keyset: The keyset to use for signature generation. The following are both valid paths to an EdgeCacheKeyset resource: - 'projects/project/locations/global/edgeCacheKeysets/yourKeyset' - 'yourKeyset' This must be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified. This field may not be specified otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#keyset GoogleNetworkServicesEdgeCacheService#keyset}
        :param token_query_parameter: The query parameter in which to put the generated token. If not specified, defaults to 'edge-cache-token'. If specified, the name must be 1-64 characters long and match the regular expression '`a-zA-Z <%5Ba-zA-Z0-9_-%5D>`_*' which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. This field may only be set when the GENERATE_TOKEN_HLS_COOKIELESS or PROPAGATE_TOKEN_HLS_COOKIELESS actions are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#token_query_parameter GoogleNetworkServicesEdgeCacheService#token_query_parameter}
        :param token_ttl: The duration the token is valid starting from the moment the token is first generated. Defaults to '86400s' (1 day). The TTL must be >= 0 and <= 604,800 seconds (1 week). This field may only be specified when the GENERATE_COOKIE or GENERATE_TOKEN_HLS_COOKIELESS actions are specified. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#token_ttl GoogleNetworkServicesEdgeCacheService#token_ttl}
        '''
        value = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures(
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
        :param excluded_query_parameters: Names of query string parameters to exclude from cache keys. All other parameters will be included. Either specify includedQueryParameters or excludedQueryParameters, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#excluded_query_parameters GoogleNetworkServicesEdgeCacheService#excluded_query_parameters}
        :param exclude_host: If true, requests to different hosts will be cached separately. Note: this should only be enabled if hosts share the same origin and content. Removing the host from the cache key may inadvertently result in different objects being cached than intended, depending on which route the first user matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#exclude_host GoogleNetworkServicesEdgeCacheService#exclude_host}
        :param exclude_query_string: If true, exclude query string parameters from the cache key. If false (the default), include the query string parameters in the cache key according to includeQueryParameters and excludeQueryParameters. If neither includeQueryParameters nor excludeQueryParameters is set, the entire query string will be included. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#exclude_query_string GoogleNetworkServicesEdgeCacheService#exclude_query_string}
        :param included_cookie_names: Names of Cookies to include in cache keys. The cookie name and cookie value of each cookie named will be used as part of the cache key. Cookie names: - must be valid RFC 6265 "cookie-name" tokens - are case sensitive - cannot start with "Edge-Cache-" (case insensitive) Note that specifying several cookies, and/or cookies that have a large range of values (e.g., per-user) will dramatically impact the cache hit rate, and may result in a higher eviction rate and reduced performance. You may specify up to three cookie names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#included_cookie_names GoogleNetworkServicesEdgeCacheService#included_cookie_names}
        :param included_header_names: Names of HTTP request headers to include in cache keys. The value of the header field will be used as part of the cache key. - Header names must be valid HTTP RFC 7230 header field values. - Header field names are case insensitive - To include the HTTP method, use ":method" Note that specifying several headers, and/or headers that have a large range of values (e.g. per-user) will dramatically impact the cache hit rate, and may result in a higher eviction rate and reduced performance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#included_header_names GoogleNetworkServicesEdgeCacheService#included_header_names}
        :param included_query_parameters: Names of query string parameters to include in cache keys. All other parameters will be excluded. Either specify includedQueryParameters or excludedQueryParameters, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#included_query_parameters GoogleNetworkServicesEdgeCacheService#included_query_parameters}
        :param include_protocol: If true, http and https requests will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#include_protocol GoogleNetworkServicesEdgeCacheService#include_protocol}
        '''
        value = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy(
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
        :param allowed_signature_algorithms: The allowed signature algorithms to use. Defaults to using only ED25519. You may specify up to 3 signature algorithms to use. Possible values: ["ED25519", "HMAC_SHA_256", "HMAC_SHA1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allowed_signature_algorithms GoogleNetworkServicesEdgeCacheService#allowed_signature_algorithms}
        :param token_query_parameter: The query parameter in which to find the token. The name must be 1-64 characters long and match the regular expression '`a-zA-Z <%5Ba-zA-Z0-9_-%5D>`_*' which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Defaults to 'edge-cache-token'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#token_query_parameter GoogleNetworkServicesEdgeCacheService#token_query_parameter}
        '''
        value = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions(
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
    ) -> GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignaturesOutputReference:
        return typing.cast(GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignaturesOutputReference, jsii.get(self, "addSignatures"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyPolicy")
    def cache_key_policy(
        self,
    ) -> GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicyOutputReference:
        return typing.cast(GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicyOutputReference, jsii.get(self, "cacheKeyPolicy"))

    @builtins.property
    @jsii.member(jsii_name="signedTokenOptions")
    def signed_token_options(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptionsOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptionsOutputReference", jsii.get(self, "signedTokenOptions"))

    @builtins.property
    @jsii.member(jsii_name="addSignaturesInput")
    def add_signatures_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures], jsii.get(self, "addSignaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyPolicyInput")
    def cache_key_policy_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy], jsii.get(self, "cacheKeyPolicyInput"))

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
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions"], jsii.get(self, "signedTokenOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheMode")
    def cache_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheMode"))

    @cache_mode.setter
    def cache_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698f314fc0f9c8c841d94dcb6aa9a86f45f52548e27f1dc725aadf99a13d722b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTtl")
    def client_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientTtl"))

    @client_ttl.setter
    def client_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2ceb107898526249f2a769fd11445baf8757b6d0544b18a566e0803edb19c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25dfa6bffdc277cd628970536237c61aeef85190e9b8b3aec814cc411a7d386f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTtl")
    def max_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxTtl"))

    @max_ttl.setter
    def max_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e3ca7dd70730568af34ec68742cfb74630f16a45a68762970464f5c0267dea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__badd2c9a3e46d69fee4813a19d9bee409dfc78872da2bf5d025ed82c9b06f0dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__445cc7924150e24893f8bebba00ffd89fde5ce2638648b52fc46790d5c95aa54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negativeCachingPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signedRequestKeyset")
    def signed_request_keyset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signedRequestKeyset"))

    @signed_request_keyset.setter
    def signed_request_keyset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3336c0608dc1fc10fa30981cc6e3af7b69c399316e5791facc4eefb5873ef1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signedRequestKeyset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signedRequestMaximumExpirationTtl")
    def signed_request_maximum_expiration_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signedRequestMaximumExpirationTtl"))

    @signed_request_maximum_expiration_ttl.setter
    def signed_request_maximum_expiration_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab86f0db8408291e22884e65899267b8d73e5eccb0d43865cf691eb15beff5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signedRequestMaximumExpirationTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signedRequestMode")
    def signed_request_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signedRequestMode"))

    @signed_request_mode.setter
    def signed_request_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d12213be257053a815b9f440d3d1ff338257fbb8017ff70d11328baeef6b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signedRequestMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0a8b01ed8509d0f688cfe3e0ccdae336079a98ccb30c49fb8228c9dcb011be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_signature_algorithms": "allowedSignatureAlgorithms",
        "token_query_parameter": "tokenQueryParameter",
    },
)
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions:
    def __init__(
        self,
        *,
        allowed_signature_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        token_query_parameter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_signature_algorithms: The allowed signature algorithms to use. Defaults to using only ED25519. You may specify up to 3 signature algorithms to use. Possible values: ["ED25519", "HMAC_SHA_256", "HMAC_SHA1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allowed_signature_algorithms GoogleNetworkServicesEdgeCacheService#allowed_signature_algorithms}
        :param token_query_parameter: The query parameter in which to find the token. The name must be 1-64 characters long and match the regular expression '`a-zA-Z <%5Ba-zA-Z0-9_-%5D>`_*' which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Defaults to 'edge-cache-token'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#token_query_parameter GoogleNetworkServicesEdgeCacheService#token_query_parameter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6d5eeb9de0fe61a4c6cdab2c7e6df117da3b447f3ff04a63e0754b896dd85b5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allowed_signature_algorithms GoogleNetworkServicesEdgeCacheService#allowed_signature_algorithms}
        '''
        result = self._values.get("allowed_signature_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def token_query_parameter(self) -> typing.Optional[builtins.str]:
        '''The query parameter in which to find the token.

        The name must be 1-64 characters long and match the regular expression '`a-zA-Z <%5Ba-zA-Z0-9_-%5D>`_*' which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit.

        Defaults to 'edge-cache-token'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#token_query_parameter GoogleNetworkServicesEdgeCacheService#token_query_parameter}
        '''
        result = self._values.get("token_query_parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__335b31ac1b57179360e5b9b61055ad0b7462c08a305d916d6d4aeae2ebdecdb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38ff97bfc4d0feb3668bd6ca6fd7627374485f74ad767ccd831b770a04b6dd95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedSignatureAlgorithms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenQueryParameter")
    def token_query_parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenQueryParameter"))

    @token_query_parameter.setter
    def token_query_parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c6db54fe7788701c0778ff1282998d9c0dbc804557b18d36f2e90daeef196be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenQueryParameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e909d3859b20f029d51a40c0468564398a4f4dbc3102e83a600a0677ef06d2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy",
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
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy:
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
        :param max_age: Specifies how long results of a preflight request can be cached by a client in seconds. Note that many browser clients enforce a maximum TTL of 600s (10 minutes). - Setting the value to -1 forces a pre-flight check for all requests (not recommended) - A maximum TTL of 86400s can be set, but note that (as above) some clients may force pre-flight checks at a more regular interval. - This translates to the Access-Control-Max-Age header. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#max_age GoogleNetworkServicesEdgeCacheService#max_age}
        :param allow_credentials: In response to a preflight request, setting this to true indicates that the actual request can include user credentials. This translates to the Access-Control-Allow-Credentials response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allow_credentials GoogleNetworkServicesEdgeCacheService#allow_credentials}
        :param allow_headers: Specifies the content for the Access-Control-Allow-Headers response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allow_headers GoogleNetworkServicesEdgeCacheService#allow_headers}
        :param allow_methods: Specifies the content for the Access-Control-Allow-Methods response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allow_methods GoogleNetworkServicesEdgeCacheService#allow_methods}
        :param allow_origins: Specifies the list of origins that will be allowed to do CORS requests. This translates to the Access-Control-Allow-Origin response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allow_origins GoogleNetworkServicesEdgeCacheService#allow_origins}
        :param disabled: If true, specifies the CORS policy is disabled. The default value is false, which indicates that the CORS policy is in effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#disabled GoogleNetworkServicesEdgeCacheService#disabled}
        :param expose_headers: Specifies the content for the Access-Control-Allow-Headers response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#expose_headers GoogleNetworkServicesEdgeCacheService#expose_headers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ed6557af2544a57f91b5a0faf70384db890fe93c241cc90a1f6835bbce6178)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#max_age GoogleNetworkServicesEdgeCacheService#max_age}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allow_credentials GoogleNetworkServicesEdgeCacheService#allow_credentials}
        '''
        result = self._values.get("allow_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the content for the Access-Control-Allow-Headers response header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allow_headers GoogleNetworkServicesEdgeCacheService#allow_headers}
        '''
        result = self._values.get("allow_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the content for the Access-Control-Allow-Methods response header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allow_methods GoogleNetworkServicesEdgeCacheService#allow_methods}
        '''
        result = self._values.get("allow_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of origins that will be allowed to do CORS requests.

        This translates to the Access-Control-Allow-Origin response header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allow_origins GoogleNetworkServicesEdgeCacheService#allow_origins}
        '''
        result = self._values.get("allow_origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, specifies the CORS policy is disabled.

        The default value is false, which indicates that the CORS policy is in effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#disabled GoogleNetworkServicesEdgeCacheService#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the content for the Access-Control-Allow-Headers response header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#expose_headers GoogleNetworkServicesEdgeCacheService#expose_headers}
        '''
        result = self._values.get("expose_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__193832c6b5d8e9cc4af14044273b7e749c7900cb1974b4606440372651e8a76b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66840004ee8b05c4096d376532f9fa039a0e1e86cd7e1f649e5cdf37846ea1c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowHeaders")
    def allow_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowHeaders"))

    @allow_headers.setter
    def allow_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ed1159a17d8480a4f5012515b2e97257b85abc800feba966d9f54d3d4595ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowMethods")
    def allow_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowMethods"))

    @allow_methods.setter
    def allow_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef7b5e66200e55c5ec24b8e5d51f55a639d4c82b1c02bee7375d3c5c329e12a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowOrigins")
    def allow_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowOrigins"))

    @allow_origins.setter
    def allow_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea26e932195715a2cc3fbd11c3398958ae983352501a57358148b6d092b49df2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d55ca3a5c7b1bdadbd3f0a4809807b51fef39c7d244d2a3ca9546a9f4b8283e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposeHeaders")
    def expose_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exposeHeaders"))

    @expose_headers.setter
    def expose_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__768265dd6f65d1027e80307bf36129e76e572750be8f237691bba17838799fa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposeHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAge")
    def max_age(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxAge"))

    @max_age.setter
    def max_age(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f02fb826f39ce601eb2a47afa5b06c4e965ac3c41a3eca92728b5adfaf1b3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d3409492fac3b1290ab4b489ef696c47fe6ac3393c8242d425ea60aae5240c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__792a7856c5833563827483d8cea13aee7c4395d0839e863ead69820a0b4bb801)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCdnPolicy")
    def put_cdn_policy(
        self,
        *,
        add_signatures: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures, typing.Dict[builtins.str, typing.Any]]] = None,
        cache_key_policy: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[builtins.str] = None,
        default_ttl: typing.Optional[builtins.str] = None,
        max_ttl: typing.Optional[builtins.str] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        signed_request_keyset: typing.Optional[builtins.str] = None,
        signed_request_maximum_expiration_ttl: typing.Optional[builtins.str] = None,
        signed_request_mode: typing.Optional[builtins.str] = None,
        signed_token_options: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param add_signatures: add_signatures block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#add_signatures GoogleNetworkServicesEdgeCacheService#add_signatures}
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#cache_key_policy GoogleNetworkServicesEdgeCacheService#cache_key_policy}
        :param cache_mode: Cache modes allow users to control the behaviour of the cache, what content it should cache automatically, whether to respect origin headers, or whether to unconditionally cache all responses. For all cache modes, Cache-Control headers will be passed to the client. Use clientTtl to override what is sent to the client. Possible values: ["CACHE_ALL_STATIC", "USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "BYPASS_CACHE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#cache_mode GoogleNetworkServicesEdgeCacheService#cache_mode}
        :param client_ttl: Specifies a separate client (e.g. browser client) TTL, separate from the TTL used by the edge caches. Leaving this empty will use the same cache TTL for both the CDN and the client-facing response. - The TTL must be > 0 and <= 86400s (1 day) - The clientTtl cannot be larger than the defaultTtl (if set) - Fractions of a second are not allowed. Omit this field to use the defaultTtl, or the max-age set by the origin, as the client-facing TTL. When the cache mode is set to "USE_ORIGIN_HEADERS" or "BYPASS_CACHE", you must omit this field. A duration in seconds terminated by 's'. Example: "3s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#client_ttl GoogleNetworkServicesEdgeCacheService#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). Defaults to 3600s (1 hour). - The TTL must be >= 0 and <= 31,536,000 seconds (1 year) - Setting a TTL of "0" means "always revalidate" (equivalent to must-revalidate) - The value of defaultTTL cannot be set to a value greater than that of maxTTL. - Fractions of a second are not allowed. - When the cacheMode is set to FORCE_CACHE_ALL, the defaultTTL will overwrite the TTL set in all responses. Note that infrequently accessed objects may be evicted from the cache before the defined TTL. Objects that expire will be revalidated with the origin. When the cache mode is set to "USE_ORIGIN_HEADERS" or "BYPASS_CACHE", you must omit this field. A duration in seconds terminated by 's'. Example: "3s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#default_ttl GoogleNetworkServicesEdgeCacheService#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Defaults to 86400s (1 day). Cache directives that attempt to set a max-age or s-maxage higher than this, or an Expires header more than maxTtl seconds in the future will be capped at the value of maxTTL, as if it were the value of an s-maxage Cache-Control directive. - The TTL must be >= 0 and <= 31,536,000 seconds (1 year) - Setting a TTL of "0" means "always revalidate" - The value of maxTtl must be equal to or greater than defaultTtl. - Fractions of a second are not allowed. When the cache mode is set to "USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", or "BYPASS_CACHE", you must omit this field. A duration in seconds terminated by 's'. Example: "3s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#max_ttl GoogleNetworkServicesEdgeCacheService#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. This can reduce the load on your origin and improve end-user experience by reducing response latency. By default, the CDNPolicy will apply the following default TTLs to these status codes: - HTTP 300 (Multiple Choice), 301, 308 (Permanent Redirects): 10m - HTTP 404 (Not Found), 410 (Gone), 451 (Unavailable For Legal Reasons): 120s - HTTP 405 (Method Not Found), 414 (URI Too Long), 501 (Not Implemented): 60s These defaults can be overridden in negativeCachingPolicy Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#negative_caching GoogleNetworkServicesEdgeCacheService#negative_caching}
        :param negative_caching_policy: Sets a cache TTL for the specified HTTP status code. negativeCaching must be enabled to configure negativeCachingPolicy. - Omitting the policy and leaving negativeCaching enabled will use the default TTLs for each status code, defined in negativeCaching. - TTLs must be >= 0 (where 0 is "always revalidate") and <= 86400s (1 day) Note that when specifying an explicit negativeCachingPolicy, you should take care to specify a cache TTL for all response codes that you wish to cache. The CDNPolicy will not apply any default negative caching when a policy exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#negative_caching_policy GoogleNetworkServicesEdgeCacheService#negative_caching_policy}
        :param signed_request_keyset: The EdgeCacheKeyset containing the set of public keys used to validate signed requests at the edge. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#signed_request_keyset GoogleNetworkServicesEdgeCacheService#signed_request_keyset}
        :param signed_request_maximum_expiration_ttl: Limit how far into the future the expiration time of a signed request may be. When set, a signed request is rejected if its expiration time is later than now + signedRequestMaximumExpirationTtl, where now is the time at which the signed request is first handled by the CDN. - The TTL must be > 0. - Fractions of a second are not allowed. By default, signedRequestMaximumExpirationTtl is not set and the expiration time of a signed request may be arbitrarily far into future. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#signed_request_maximum_expiration_ttl GoogleNetworkServicesEdgeCacheService#signed_request_maximum_expiration_ttl}
        :param signed_request_mode: Whether to enforce signed requests. The default value is DISABLED, which means all content is public, and does not authorize access. You must also set a signedRequestKeyset to enable signed requests. When set to REQUIRE_SIGNATURES, all matching requests will have their signature validated. Requests that were not signed with the corresponding private key, or that are otherwise invalid (expired, do not match the signature, IP address, or header) will be rejected with a HTTP 403 and (if enabled) logged. Possible values: ["DISABLED", "REQUIRE_SIGNATURES", "REQUIRE_TOKENS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#signed_request_mode GoogleNetworkServicesEdgeCacheService#signed_request_mode}
        :param signed_token_options: signed_token_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#signed_token_options GoogleNetworkServicesEdgeCacheService#signed_token_options}
        '''
        value = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy(
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
        :param max_age: Specifies how long results of a preflight request can be cached by a client in seconds. Note that many browser clients enforce a maximum TTL of 600s (10 minutes). - Setting the value to -1 forces a pre-flight check for all requests (not recommended) - A maximum TTL of 86400s can be set, but note that (as above) some clients may force pre-flight checks at a more regular interval. - This translates to the Access-Control-Max-Age header. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#max_age GoogleNetworkServicesEdgeCacheService#max_age}
        :param allow_credentials: In response to a preflight request, setting this to true indicates that the actual request can include user credentials. This translates to the Access-Control-Allow-Credentials response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allow_credentials GoogleNetworkServicesEdgeCacheService#allow_credentials}
        :param allow_headers: Specifies the content for the Access-Control-Allow-Headers response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allow_headers GoogleNetworkServicesEdgeCacheService#allow_headers}
        :param allow_methods: Specifies the content for the Access-Control-Allow-Methods response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allow_methods GoogleNetworkServicesEdgeCacheService#allow_methods}
        :param allow_origins: Specifies the list of origins that will be allowed to do CORS requests. This translates to the Access-Control-Allow-Origin response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allow_origins GoogleNetworkServicesEdgeCacheService#allow_origins}
        :param disabled: If true, specifies the CORS policy is disabled. The default value is false, which indicates that the CORS policy is in effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#disabled GoogleNetworkServicesEdgeCacheService#disabled}
        :param expose_headers: Specifies the content for the Access-Control-Allow-Headers response header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#expose_headers GoogleNetworkServicesEdgeCacheService#expose_headers}
        '''
        value = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy(
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
        :param host_rewrite: Prior to forwarding the request to the selected origin, the request's host header is replaced with contents of hostRewrite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#host_rewrite GoogleNetworkServicesEdgeCacheService#host_rewrite}
        :param path_prefix_rewrite: Prior to forwarding the request to the selected origin, the matching portion of the request's path is replaced by pathPrefixRewrite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_prefix_rewrite GoogleNetworkServicesEdgeCacheService#path_prefix_rewrite}
        :param path_template_rewrite: Prior to forwarding the request to the selected origin, if the request matched a pathTemplateMatch, the matching portion of the request's path is replaced re-written using the pattern specified by pathTemplateRewrite. pathTemplateRewrite must be between 1 and 255 characters (inclusive), must start with a '/', and must only use variables captured by the route's pathTemplate matchers. pathTemplateRewrite may only be used when all of a route's MatchRules specify pathTemplate. Only one of pathPrefixRewrite and pathTemplateRewrite may be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_template_rewrite GoogleNetworkServicesEdgeCacheService#path_template_rewrite}
        '''
        value = GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite(
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
    ) -> GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyOutputReference:
        return typing.cast(GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyOutputReference, jsii.get(self, "cdnPolicy"))

    @builtins.property
    @jsii.member(jsii_name="corsPolicy")
    def cors_policy(
        self,
    ) -> GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicyOutputReference:
        return typing.cast(GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicyOutputReference, jsii.get(self, "corsPolicy"))

    @builtins.property
    @jsii.member(jsii_name="urlRewrite")
    def url_rewrite(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewriteOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewriteOutputReference", jsii.get(self, "urlRewrite"))

    @builtins.property
    @jsii.member(jsii_name="cdnPolicyInput")
    def cdn_policy_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy], jsii.get(self, "cdnPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionModeInput")
    def compression_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="corsPolicyInput")
    def cors_policy_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy], jsii.get(self, "corsPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRewriteInput")
    def url_rewrite_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite"], jsii.get(self, "urlRewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionMode")
    def compression_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionMode"))

    @compression_mode.setter
    def compression_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f428ebed05ad1965812b9a2184ef7a8cef855dc2c634750b32de2bf5de29338a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653a5b37047e9740efd641176c6a1f00a72c4d976e693a84e6bce5969d4da7f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite",
    jsii_struct_bases=[],
    name_mapping={
        "host_rewrite": "hostRewrite",
        "path_prefix_rewrite": "pathPrefixRewrite",
        "path_template_rewrite": "pathTemplateRewrite",
    },
)
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite:
    def __init__(
        self,
        *,
        host_rewrite: typing.Optional[builtins.str] = None,
        path_prefix_rewrite: typing.Optional[builtins.str] = None,
        path_template_rewrite: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_rewrite: Prior to forwarding the request to the selected origin, the request's host header is replaced with contents of hostRewrite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#host_rewrite GoogleNetworkServicesEdgeCacheService#host_rewrite}
        :param path_prefix_rewrite: Prior to forwarding the request to the selected origin, the matching portion of the request's path is replaced by pathPrefixRewrite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_prefix_rewrite GoogleNetworkServicesEdgeCacheService#path_prefix_rewrite}
        :param path_template_rewrite: Prior to forwarding the request to the selected origin, if the request matched a pathTemplateMatch, the matching portion of the request's path is replaced re-written using the pattern specified by pathTemplateRewrite. pathTemplateRewrite must be between 1 and 255 characters (inclusive), must start with a '/', and must only use variables captured by the route's pathTemplate matchers. pathTemplateRewrite may only be used when all of a route's MatchRules specify pathTemplate. Only one of pathPrefixRewrite and pathTemplateRewrite may be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_template_rewrite GoogleNetworkServicesEdgeCacheService#path_template_rewrite}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d48925c97e70c5672b2621b4cbbfc287a5195d138eed31e7a326581727d34d6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#host_rewrite GoogleNetworkServicesEdgeCacheService#host_rewrite}
        '''
        result = self._values.get("host_rewrite")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_prefix_rewrite(self) -> typing.Optional[builtins.str]:
        '''Prior to forwarding the request to the selected origin, the matching portion of the request's path is replaced by pathPrefixRewrite.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_prefix_rewrite GoogleNetworkServicesEdgeCacheService#path_prefix_rewrite}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_template_rewrite GoogleNetworkServicesEdgeCacheService#path_template_rewrite}
        '''
        result = self._values.get("path_template_rewrite")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewriteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewriteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa8afe302fc427c7c25999c223dfbd294dc727b5ba11cc7d02d55085be28ff49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91fc3bc3ed0782c9aa5f43973e8414581d4a2b96655c7e8624561dd0c1a3dd0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathPrefixRewrite")
    def path_prefix_rewrite(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathPrefixRewrite"))

    @path_prefix_rewrite.setter
    def path_prefix_rewrite(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29eccd9aa90ab84a681e182db6d6dec828d7ab73c156505f5b4b9a6f7d3dcdee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathPrefixRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathTemplateRewrite")
    def path_template_rewrite(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathTemplateRewrite"))

    @path_template_rewrite.setter
    def path_template_rewrite(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb90d73dabf4c9f772a44f29164898be4f99902b9558809a5882c3fa1ecf154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathTemplateRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd241d2992b3e53bd6df4f3fb72df6e75107216ebe10d1762af9e8122024be51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods",
    jsii_struct_bases=[],
    name_mapping={"allowed_methods": "allowedMethods"},
)
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods:
    def __init__(
        self,
        *,
        allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_methods: The non-empty set of HTTP methods that are allowed for this route. Any combination of "GET", "HEAD", "OPTIONS", "PUT", "POST", "DELETE", and "PATCH". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allowed_methods GoogleNetworkServicesEdgeCacheService#allowed_methods}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59a8dbc3ed3465c230fcfc15b886b83f2e08adbbb82e3d8c11645d85c47c2b5)
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods

    @builtins.property
    def allowed_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The non-empty set of HTTP methods that are allowed for this route.

        Any combination of "GET", "HEAD", "OPTIONS", "PUT", "POST", "DELETE", and "PATCH".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#allowed_methods GoogleNetworkServicesEdgeCacheService#allowed_methods}
        '''
        result = self._values.get("allowed_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethodsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethodsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1b44cfc1f719b50d6fb43b5265ab82af96723196f1b7a84930d93b311308159)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d225f9f593ceeb802d38a957ba086bd4e6aae8c1b63602c07b9a8d86753a468e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca83f9d8ac6d418df34690baa9b04e57400dfb0b2655bb7aeaa34aa55d136b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect",
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
class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect:
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
        :param host_redirect: The host that will be used in the redirect response instead of the one that was supplied in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#host_redirect GoogleNetworkServicesEdgeCacheService#host_redirect}
        :param https_redirect: If set to true, the URL scheme in the redirected request is set to https. If set to false, the URL scheme of the redirected request will remain the same as that of the request. This can only be set if there is at least one (1) edgeSslCertificate set on the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#https_redirect GoogleNetworkServicesEdgeCacheService#https_redirect}
        :param path_redirect: The path that will be used in the redirect response instead of the one that was supplied in the request. pathRedirect cannot be supplied together with prefixRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect. The path value must be between 1 and 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_redirect GoogleNetworkServicesEdgeCacheService#path_redirect}
        :param prefix_redirect: The prefix that replaces the prefixMatch specified in the routeRule, retaining the remaining portion of the URL before redirecting the request. prefixRedirect cannot be supplied together with pathRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#prefix_redirect GoogleNetworkServicesEdgeCacheService#prefix_redirect}
        :param redirect_response_code: The HTTP Status code to use for this RedirectAction. The supported values are: - 'MOVED_PERMANENTLY_DEFAULT', which is the default value and corresponds to 301. - 'FOUND', which corresponds to 302. - 'SEE_OTHER' which corresponds to 303. - 'TEMPORARY_REDIRECT', which corresponds to 307. in this case, the request method will be retained. - 'PERMANENT_REDIRECT', which corresponds to 308. in this case, the request method will be retained. Possible values: ["MOVED_PERMANENTLY_DEFAULT", "FOUND", "SEE_OTHER", "TEMPORARY_REDIRECT", "PERMANENT_REDIRECT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#redirect_response_code GoogleNetworkServicesEdgeCacheService#redirect_response_code}
        :param strip_query: If set to true, any accompanying query portion of the original URL is removed prior to redirecting the request. If set to false, the query portion of the original URL is retained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#strip_query GoogleNetworkServicesEdgeCacheService#strip_query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb6cfbc71f97a59676ff77905d823ed348a36e3ebc297f6ab33d65ce7a2e4f3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#host_redirect GoogleNetworkServicesEdgeCacheService#host_redirect}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#https_redirect GoogleNetworkServicesEdgeCacheService#https_redirect}
        '''
        result = self._values.get("https_redirect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path_redirect(self) -> typing.Optional[builtins.str]:
        '''The path that will be used in the redirect response instead of the one that was supplied in the request.

        pathRedirect cannot be supplied together with prefixRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect.

        The path value must be between 1 and 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#path_redirect GoogleNetworkServicesEdgeCacheService#path_redirect}
        '''
        result = self._values.get("path_redirect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix_redirect(self) -> typing.Optional[builtins.str]:
        '''The prefix that replaces the prefixMatch specified in the routeRule, retaining the remaining portion of the URL before redirecting the request.

        prefixRedirect cannot be supplied together with pathRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#prefix_redirect GoogleNetworkServicesEdgeCacheService#prefix_redirect}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#redirect_response_code GoogleNetworkServicesEdgeCacheService#redirect_response_code}
        '''
        result = self._values.get("redirect_response_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strip_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, any accompanying query portion of the original URL is removed prior to redirecting the request.

        If set to false, the query portion of the original URL is retained.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#strip_query GoogleNetworkServicesEdgeCacheService#strip_query}
        '''
        result = self._values.get("strip_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c705f6be4ae0916a9a36a9c62f506bcdd4be9ab6ab6737224352a64b1c385d72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__764335ce93c076ff89c3e2842bf129eac48822d9f2f62b02f900797f5d955784)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d68959660448ddf02f8fe069b500a52f5ea428f352dd57e3a03ab026cde1e9a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathRedirect")
    def path_redirect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathRedirect"))

    @path_redirect.setter
    def path_redirect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7885518cce40a6c8e36cd12da1a51feb0a4fbe8517b4d9007bd7907af374b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixRedirect")
    def prefix_redirect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixRedirect"))

    @prefix_redirect.setter
    def prefix_redirect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5787bee05c0949798574b9b911a54bdf153337372162b602054424380d7db97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectResponseCode")
    def redirect_response_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectResponseCode"))

    @redirect_response_code.setter
    def redirect_response_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeaf8b28274bdd04f965aaef7e33cfd15104185c3d4c1ca33f31762cc87f3745)
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
            type_hints = typing.get_type_hints(_typecheckingstub__820f6edf197e31d5dbd2e874f2cf074ef85d0f1398b22649635597bf906642fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stripQuery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect]:
        return typing.cast(typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__270461706ad69b4b90064264680ebe8d69e8637e0cc1b4c82b6b48217e46f92a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetworkServicesEdgeCacheServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#create GoogleNetworkServicesEdgeCacheService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#delete GoogleNetworkServicesEdgeCacheService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#update GoogleNetworkServicesEdgeCacheService#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5179b815ef9b7083cf47b37dc8c9695a3b16d7f02183aaa2ed196115df2c3d0f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#create GoogleNetworkServicesEdgeCacheService#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#delete GoogleNetworkServicesEdgeCacheService#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_edge_cache_service#update GoogleNetworkServicesEdgeCacheService#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheService.GoogleNetworkServicesEdgeCacheServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5166f1207f4ed2298bfa3160182b0729bdfa7f5eb6c01813e5b1dd7719ed9595)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9b857901780e1540f4f88757c1f5af93d09ef7b09b339b05c57d02fe7ea29e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa3069db29d9149aa2a4202f17e8cd8cb5e90fd574c4f299bc2990246a109b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de77bb26f9811938e194b8f2deb41eaa12e2cc74b5ac7b22227a7e399ec16ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4924864744e22e0c9cfe7e555c75c16e028e4631b4624a43cd399881af439c67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetworkServicesEdgeCacheService",
    "GoogleNetworkServicesEdgeCacheServiceConfig",
    "GoogleNetworkServicesEdgeCacheServiceLogConfig",
    "GoogleNetworkServicesEdgeCacheServiceLogConfigOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRouting",
    "GoogleNetworkServicesEdgeCacheServiceRoutingHostRule",
    "GoogleNetworkServicesEdgeCacheServiceRoutingHostRuleList",
    "GoogleNetworkServicesEdgeCacheServiceRoutingHostRuleOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherList",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddList",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAddOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveList",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemoveOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddList",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAddOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveList",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemoveOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleList",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchList",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatchOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleList",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchList",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatchOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignaturesOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicyOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptionsOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicyOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewriteOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethodsOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect",
    "GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirectOutputReference",
    "GoogleNetworkServicesEdgeCacheServiceTimeouts",
    "GoogleNetworkServicesEdgeCacheServiceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6dfab8066fe15f24966bad7ae6a41615b995c0a15a32aa06c62b5370c9379f51(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    routing: typing.Union[GoogleNetworkServicesEdgeCacheServiceRouting, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    disable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_quic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    edge_security_policy: typing.Optional[builtins.str] = None,
    edge_ssl_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    log_config: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    require_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_policy: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4788096400681ad9841d9557e99430787bac146ca096c93f09ff57943d31ff93(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80acdf34fa7f61d82faa48267b66e20cfd1c031e1f2672b916fddf93a047408c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaeb64c600e2a50b589a3c274387e5bd57266cdc9391d1f3fc874a542fc680a0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9199c24674c6794826d0eba1c89a846e5e1681067e0ceadefae1a4149bd609(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfaea435f9caf601bf5186c998bc580f1693edbededc01655510a5357af8a151(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5e54a3c075ca64f9dccc3f3f23e517bfceea86b7fb460c7822254e94048b05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3b1889a0a567022404ed85d26ca08f214691bd17bb5e2217d327f356e7d7d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038b207717a403404cb9d8ea33f320ef275efe113de0c65bcbed1455e8d653d1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806151dbefb706afbc0c2b53952d986d33626ad53c76509e2a469af4c07e72e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a78d96b9aef3e1d95165e90a711eaf500f177960d46ec8e828d6c2333884456(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14f53d194d7245a04c3ab58e05602d5091550224228f8448da48c89e905e7f9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb94f89d98dd34093429790dff67070288190a50d2abd5ff4d0f944036131f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ff3fa5fb3c377e869ab6a4f6d0e69545867a0acf7f3336bc0a0d5826b5e074(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    routing: typing.Union[GoogleNetworkServicesEdgeCacheServiceRouting, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    disable_http2: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_quic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    edge_security_policy: typing.Optional[builtins.str] = None,
    edge_ssl_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    log_config: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    require_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssl_policy: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a99bdabb9013c88ed8c296474bf571f9d8043ea272131aef92d51da66beb33e(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sample_rate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769fb073babdeebd252fef038bfd2ff869aca879982aca6762b67ddaf765c851(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d1dff863557ad1ff252d7bb454557df0920c5d12612bcdc94d134f53c2ce19(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a63d9a2386f4a84e7dfb4acd7fc1f79b5bc40d44eac2f473cadd3c2bae3a4a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b2475c7ad69a0e02db4effd5154a908b1be10fa57bdad1397532eb9100cbe4(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec23ca5a963054a34110a084f33ed1f472372407b587e933e7efe8060b04a95(
    *,
    host_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingHostRule, typing.Dict[builtins.str, typing.Any]]]],
    path_matcher: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c087355f057727a95835ca7287bfe9cdd44242e692c1a25aad2b6aeea3eefc23(
    *,
    hosts: typing.Sequence[builtins.str],
    path_matcher: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62d9ef04b9bc61fc91bc97e294e5d1c73f0f18e6b721619d170b8e4e4550e10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61416c9c2644e5efcc7328899811608b51f7c832b4976d314e4f4408837b4380(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4bde08cd630c968c1cdc12e7f1f2d50c24224603ed478b4bb4a2bd10de0c72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385de99a03e4c3239fc6b35ee5431def0e5b42a825f4043cc3d951607fde2322(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896f7a7049572a428649193081455dc15ff34730ac6c0f8ddf0b8119634bc603(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14be2a4169cd579ca90369237a4abee075f39a0067733256d9c829675cf96fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingHostRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18702e3335e4e6b7b6426ecdeff8c1921ebcfcf75b0dfcd1c3e3bad3a7eb46bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1577441283d7da576ced83d7f93603ffae5e98fb80c58ac9de44e85007c7cb09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b4125a4d8c828a635d1a2c8a52838b76098e64cc68fbac3cf6609e04e18059(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c870d6c2eaf9e91be03d397c861c034f07af42a75a769b9b0d6316ed1ef0e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48199a92e3951ac714d0073bf6fa5e8542acb252cb1110c691fa011b06643034(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingHostRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ceff50cc426d94a516334ac02ae76a49302e4b2aa4062886a18e015acace369(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3cca0874ff2fae1f6dbcf61a16c763c0ffa3b2d6dff44ec057b066f427aeeb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingHostRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4409c145767550c32e188f83c322fe881862599c1a98e41390eda20e777a5cd7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66f990fc9f7a0d715db380b0b94216d38d84d85493216e6a929cf5a1883b696(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRouting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175f17cb973185d3d0d60849422a2dff58d18eeef4c9f28414790da57c69d5ef(
    *,
    name: builtins.str,
    route_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49f94b9e76c7ca6c9fb68553d01f3298591da02259efc3cfbec9263c1f444f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68f1e51cda75dff7824df1743665952b191fac1a4aa80dbd685c5b3c71d1cf7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398f7922b54a2c72d8242e3d42cab65f82178bb1c17948b48d79abc366bc60f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b097b6618011b87f0b94ff4610022b479e53bce384671d842a58b4e4ff9c07(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa386c850c0ca894bbd3f664537837513378e9a8cead2f4470448d2e9aa218f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff97cd798941c4e7fd300ddb7bb7c52cc9dcf78b76c887103d947fad39d0d52e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c15baf4b27b0e11f7d61191b42846f7a63d5369400dcb6c725baf1a979846c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04dd28eef328dc196425c2bb6934fffb8cd4747fda45ff0e31e3cd794b4e382(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f115ff40cd493e2d5f525bb9f96db2e06ea48254dc4e8d4d708e16119ff483(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61147423fd41008eb4d9774c08675bd9b34214c0180578b3c548f47acb1e83ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078caa42d18ff980ca8808b4e2dfb684b9bc5e7590e9933b75108a5ba13451ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcher]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e70ae1b8b611efc876eb81b0a46ccc4115c33b530c3f1cf386f7e0a98355a8d(
    *,
    match_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule, typing.Dict[builtins.str, typing.Any]]]],
    priority: builtins.str,
    description: typing.Optional[builtins.str] = None,
    header_action: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction, typing.Dict[builtins.str, typing.Any]]] = None,
    origin: typing.Optional[builtins.str] = None,
    route_action: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction, typing.Dict[builtins.str, typing.Any]]] = None,
    route_methods: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods, typing.Dict[builtins.str, typing.Any]]] = None,
    url_redirect: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad259d2080b31de0d8e423f060b440da84673b560a19cf09c4d45471ac04954(
    *,
    request_header_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_header_to_remove: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove, typing.Dict[builtins.str, typing.Any]]]]] = None,
    response_header_to_add: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    response_header_to_remove: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77dcbbdb09b0cd54d42d5fffb1a4466b96bccf9926b3dafd8566322a1dc7f049(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04678cefb7b32d61148555246842f25186e99395a9dd7d75bd4cf492ef888ba8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660ccccf47b2b7c34192002dcb886753a7cf29ceafd47f1ae4f8a41a05ceaf98(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cfabb3edf80fbd2fe18ffe23bd342b66906c862f122944d502a3f221e7f1502(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6233ec642ebfb9a12bc9682bcae1e8ba0c131ed2458281927c3e55a8e6920fda(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d276293b20840835cacd209b8eac7ebd3ac5d198682cd077a5d8ba3ade095ac(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f693683bd8b5c500da68188d8a38689ed6b5c3b03502840e7077de3726de6528(
    *,
    header_name: builtins.str,
    header_value: builtins.str,
    replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5104a959f5666f45ddd7eb9c48e45ae9bb23c59f3ee92ce87c626449084ead(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68d3ad1478144fabd8a418073b30a00b32d484067dce04fec54c124d087ef0b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5db799d4a71450ccb46feb2bd6355cfeb204b6cd1a80c9cbc65f7a2af18b64e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e1c7a4b48df6f41a8ebf821157da5f560632d09f65775d52a7be55b367ddd5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826cf946997df5bee6f7915f5aed694398bbf814e2632a6763876e5da64bb050(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee774c7c391d58c46a382f8e5b34af6fd24a9d1b50cc4d767f73b47cbbe9c9b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135dc6eb97e83c52c9072f7a119e8d6026ed926f74863b8b8b8c436d1782d1ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef4427ae22ed3dc280b700ba07cafa39d709dc42c09d967ece819064706970f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13904679d2a0f707cf778afdb5fa752c3d569f1cb898e19caee61d226c894407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9031daeff732c7f672fb42b9ea8a500e35da1f6964d0301131a18d6a21796ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b07448c58c37dac1496b2031892907b71d3b6eb22d85b1de9c5de00e89204f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToAdd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7e846cd7326fd9582c24078cd12f48eea9b56ddcf44d43650d4b417bb87aafe(
    *,
    header_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b8779491f3fb815cd0cd42e5651cce3c728ee49f8548c4ca0ecc142934a52c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5efde5c466dbdd2081d5b7a15228389877130782b40bcbf1ae5c8f0456cd8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782332cc6784439979c153b29c6bfd5e94aa906ab97ee940d33fdace807274d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5740e20d03c9aa672dd3e1837a563d2ef01e9e9d3523460be8f64f9ad3dc7774(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a79360fafa38b24bca14733f022e06e8333e5722f8ccc9d134cb3f9d55cf6d9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4525a9b7807d6a10fa96107580d74dcb585b2fd113243f1a89e0b5e870586fa8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3eb3b594f77147e9ec535a22b84e72d82910dbcd59d3702883006586edea3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf42bb9770692fa63620e542b93eca766a280f9be526d81ef190d5b01e8e63d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd974c1b8245791b3f07fb3b8efd372a6351a9ec37974fe400035abcde0adb82(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionRequestHeaderToRemove]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2b4bce8ca6b97e02bf94844da6b387e1e5a7f0ac2804cc22887e919e570309(
    *,
    header_name: builtins.str,
    header_value: builtins.str,
    replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c649cf37f32e9cf4c93bb82de60fc9994dfdba26b7b5fd5f5991bd08a5a59fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ffaef2529443a501840ae1a17ab064628f00eef6caffdeb37d007d1520eac4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a8d922c6154105283810a5a8393d0b4a831ea14fbe43fd258257bd11b5178c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44d0053aafea5591d609cbf4d71278ca421b274fd856da08b3fee4809411483(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47785f1068889963c13969ad99a23a8708fd546c1d1cd7d2a28f3d24c8ef69b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba43a4ab08f812913a480765b4ee600224f603eb6b8b619bda31245a214b130(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8294b5992241045f5acb74ca679629f1f135a8e6ea57a54f3c578433436c9041(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a4ae3683a09792ae907eba8c4d7aa5a44834405b8ae828f5f4b3fafd9baab2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58f9c9d2b3cfdb1dd39ca12b01d6043a86e2a748a0345f9173fc7b63949e7b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74bedc56d4ecae832ec39e2be9201a7720435d64a02e2e9940381391e030f07a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df607ee3b4928a0785a67b0f5aac28c7ef55502175099b0cb71fb77f32e49734(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToAdd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a89624458e263e657c3281a74cb6f0f867c963fc595b0c0b6791aacbd4a602(
    *,
    header_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d5816004cacab4b5919dc6e05515c16a35da1b4553ce3b40e647d29b1270b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b3590fa1c55c14e7e6cd9e51ae70708ac69be1dc4c4c7d154a98c4f400f34d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5b93df7492db4ca3475992c57ecc457fc558deac215f8c31b7c9fc07ec388b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b493383d6f10b65c99169a983b3fc0003de2b6c242a9b170e0c1e6a427a90a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b045bae5819f4df339d519e68559492844f5aa859ad26f5a65c1c4b36aef6099(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bbf301294020949347c33193e7d026fb57072f7cc7d9441b31aadcde6ddddf3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34128e4d604d04e753484e9fe1f699f1f007df86ee2dc6a011c9cbd819353212(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f2aa63904c98c2358a56d0720842657ed24d7eb0c212204583590fd1e1fcf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0332047a750e7181260a20cbb327b84e630e08f482fa457a2b4e9d24f4f10e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleHeaderActionResponseHeaderToRemove]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c90826e3fdc6aa7a1d9e437acc85842c2340fdc26ffa743abd53b962d232203(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1e218ab12221ee25605d3549a5cff539985af51b6e4b7b88151ffd292238e6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f412730b4feee05115be6624c264ca1051d10faa9f582b1a0a4e006ff39e8d36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd683674b57f142377c651cf995965384e8d3524465822beef88993b9eb964f8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1e43f635833eeddf9616060fca2f86114cb36afb19c2110fe2858e7dd50029(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0797c4f77ac9e73a32e160368fc300499e3e3c5bc7180ba82b768c14776c46b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37815bbdac74a4da2e07c88bcdb0c2bbc9e970a331f9db937edf35fa16e7b06(
    *,
    full_path_match: typing.Optional[builtins.str] = None,
    header_match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path_template_match: typing.Optional[builtins.str] = None,
    prefix_match: typing.Optional[builtins.str] = None,
    query_parameter_match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16fe890e740ceae6bdec9c383c091338442cefee3425fe16488339df8dc30c7(
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

def _typecheckingstub__d1d828c5e68baaebfb91c6df5f424f995413d0acdd972dc042646c6caa767894(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ea5b6aa6208976b2b0a4c2c929001804d56f6fe0a441c80415eeb789cc5ea5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f38d95c9aa99fbd552f8c1410533b817d4b38b63eba9caa7fda8228022e18ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c29c331ce8e8ec1aba442f71938e55c04ff8886dabccb350894dee477c42f62(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488804cff9d8d6a3a274ce4adfa2b56623510fb49b7e230b6ec1670e7aaf7848(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06eb2dea80a98c528fc061b17384e640123bc66b93c822ff5dbe70e0764520c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c180dcb4383deb19a89a0d9c4e8213a84eebfb83d7ee566d2968dc3438d4a36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a3c622f5d97804d90db357afa0c9a56173f3ce8d275edca523f42a03d3585b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16832b3d99d12da6d6d5409b018dd5feef2d47a0fdc217ef6265ae515aea3b24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40fc37b0a4c23431ec81d892e7d1dc5d6356ef491e44b3fcacc4c5b5937300c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__093129cb6ae6f2ffffbbd59b8106c035c3f218afd68dd9eb0fa8bbac09ed942a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__116f20dac6d55a87cb82e3c7456d74ea38ab3f8315754c511f5254bd36712481(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f2d9b18f1dd0c4ce067934af93ba563e29a671cb694ec2c324c682d3cee52e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf08bde1af11afb238290446f4259b4d0ea642895bfabfe328e2aefbf171da90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261d9567c05b533195f9b394988b58f24f034ef4511ada4db2f1e7562be8c491(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6f1e6eb0aa0e430e32daabaa16b09596f597ff50f1ddc8d2514a26a71c854d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348afa39271cb759910c88ffd757dcd8d043bac7b64b812857b2ddb8cbc43a81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1251b342822fe518830d715755fa6a8858a2ce66a02d6110515b9297f4365c4c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8813d3c1bbf6a2811d7a603eb0b8147c000394d4862bbdf45df9148b7c90466e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c4c6014edd6a83cb9a6e3fce70f46758a09970482a1d97d1df19cb37864e0b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2f2aabc8772a90718b0f20ad83d050a24569aeda1ee35af1dee27791be84fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0af41a12337585aabf1c14a8b809b4511a1fa0dd7c407fd33ee35935177d029(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleHeaderMatch, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d042b40a29f3bc350742e7c3a2534afad9a674020ea6b5f167c7b4fc30b557(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8594830d505942724f72764182bcd7c65ca7946b7fd368f2de680644a3c6735b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c35d165caeef4cbc51e720a607b308c111f5111602caafdc027a4f90921e6a8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce031371b0f3800656cdfc4491b788d47eabbd29f6ef904999b3f5e89211bb40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b58817ffa45b43ba1c37853253dba1bd371d758697e83b9129270030b92c709(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e23a4ee2346be56eb3534741211a891447706534e657c64c51dc828ac71908(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49feb5985d69c7e57f29075e4d73c2f139072825a1bb8ec31fddbfe51eb7bd99(
    *,
    name: builtins.str,
    exact_match: typing.Optional[builtins.str] = None,
    present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b112a739e91297a61a3175bcc6fe5ef2bf6db6f8941b346210c4b7c79c310825(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8cf4a164ef53eed3da6f8da75232016bbffa0eb09e9ad6c6a31b8ec7fc72fb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82eadbbc2e37e10ae87ca1f5a84f7a74b58351f615308764c34e2959605e72b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f11b1b82bb99e7386ae1410bf91da8848278808e2702e54560ca0a7413c8b8a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26d081aa6a238cf5e7b20337d4ea3b9f20b28c3b029ee019593ea429efbd0e7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df188a503e1adff2c24a0d0a869380b73e6f6fcec4930ef486180e36797f72c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62e56d46bf22a58d9376febc5e1a8992b151e3a16ec221bad08ca30b7249b7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a9efc0374d91dffc7e2168c4dae7feec4ae37fc4371300a2b7f7bfb3c26b10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e67d73df26c127fed720cebe298554b57a98354f3bb107153a15fbca8f42b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8205757f7ed228a2adbf5465cc36496f0fe7a3a0c1e7df86fa4e27a8865dca06(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83867eb79bd59a16f6c29ea776df76165f6ef766239d42492b22110be9d55c7f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRuleQueryParameterMatch]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243f111f680eb53ba4827321115e503e0091caf1723060fdbfb52d09b6e2bcde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1360515de542824c104cbf5d438fba2f57eeaaa67bda84ccdeb442aa055adb52(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleMatchRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d673df92f7da8700be99c4b2532a34b84026c375315a4c5ac74dfabbf31f8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315157c33997c038cff0bb18d05050c1f028adcff4419810da2c119136e405e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256415a32135bc3d4a22f335c2aa04aca673c4bd08f4d7dc9a278cb243d0a5f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933fb0e7d018bc41d9d23216d8f1075b307cbb42d390e0c5cd3ea10a0dbb4e0e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36f8c89de1303f2eecdfae1b84e976259c08490b98cb7947b3588aa04549cf5(
    *,
    cdn_policy: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    compression_mode: typing.Optional[builtins.str] = None,
    cors_policy: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    url_rewrite: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cdadd22ef08d7d0f2c911a9f563af9e1a55a06422c87c5cd832e28b461e2d31(
    *,
    add_signatures: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures, typing.Dict[builtins.str, typing.Any]]] = None,
    cache_key_policy: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    cache_mode: typing.Optional[builtins.str] = None,
    client_ttl: typing.Optional[builtins.str] = None,
    default_ttl: typing.Optional[builtins.str] = None,
    max_ttl: typing.Optional[builtins.str] = None,
    negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    negative_caching_policy: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    signed_request_keyset: typing.Optional[builtins.str] = None,
    signed_request_maximum_expiration_ttl: typing.Optional[builtins.str] = None,
    signed_request_mode: typing.Optional[builtins.str] = None,
    signed_token_options: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e82300efe148ea95bf5bd37de3b72485f5fec6ada57d1e488745b21b016423c(
    *,
    actions: typing.Sequence[builtins.str],
    copied_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    keyset: typing.Optional[builtins.str] = None,
    token_query_parameter: typing.Optional[builtins.str] = None,
    token_ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc75c802e36dfc84ddba72d4fc16f93ba1c1811f763f1efb0174bddb71c15e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f69598d42a61ff71c754526e0bcbc71a95cf496f23bff556324a45838b28b6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57162ec015ee0e912df6cd91b23dae5272435d9afdd6833bd0084715ebf2d002(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c6cb89fabe1fa9d3efd9ff98a009b7df29c6993ac82921f1764fd5f22e2735(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ef74abf47cee9ce3755ab7cc4292644c1cb4207abcd43be5a5bba6dc00372e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e864b2cbf1a984129ff3f575c90d9a6668d9e4b11ac31d8bb7928c653d5ba280(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dfacaa84f32d1a7c1eea030efeac04e06c721f1e5917c43afcf5e4eabc88eb6(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyAddSignatures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de9b88fd261e0a4b1e59acd3a380064ab24ce0cfee4d6c1e2441087d213ec54(
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

def _typecheckingstub__751658f6e1a260c1379263c2a5379354c3a3521bc26756a966df121d9d37cf02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a7f9de346f04bce230f32e895f0aba2ee55f3814102ce45fa8ad8c10ee11548(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9555b799d293b605efda97f9511399dc9a90f22f29a1e8aa74fb1af4326adf5d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b8e96db956d2e2549a23c11397560e51118cdd91e6ac06a2255a826183526e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5242df465aefa14167ecda9b313b612f69cac76a6a11fc08b0c61e99a53eb2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331da7b74806f249a03a216cf3f39fd00ab7ab7c04171ae82551b045936e978c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd3d80680eba91e7e0c396514213b1fa573f71ae0b38c25c2f1dc4c63bc7808(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab34461d7cfab89988d4d92eae6e2196cbe7b4243d75197d945e0c7c1a4846d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8df2c446c640aed1de92e6f08c28e03b298fd97a9b8968695ab226ef26797af(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicyCacheKeyPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96d4b6539023c7d3fcb8542a969cf13646f8c57901cccd6f8099deb091a63de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698f314fc0f9c8c841d94dcb6aa9a86f45f52548e27f1dc725aadf99a13d722b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2ceb107898526249f2a769fd11445baf8757b6d0544b18a566e0803edb19c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25dfa6bffdc277cd628970536237c61aeef85190e9b8b3aec814cc411a7d386f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e3ca7dd70730568af34ec68742cfb74630f16a45a68762970464f5c0267dea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__badd2c9a3e46d69fee4813a19d9bee409dfc78872da2bf5d025ed82c9b06f0dc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445cc7924150e24893f8bebba00ffd89fde5ce2638648b52fc46790d5c95aa54(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3336c0608dc1fc10fa30981cc6e3af7b69c399316e5791facc4eefb5873ef1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab86f0db8408291e22884e65899267b8d73e5eccb0d43865cf691eb15beff5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d12213be257053a815b9f440d3d1ff338257fbb8017ff70d11328baeef6b3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0a8b01ed8509d0f688cfe3e0ccdae336079a98ccb30c49fb8228c9dcb011be(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d5eeb9de0fe61a4c6cdab2c7e6df117da3b447f3ff04a63e0754b896dd85b5(
    *,
    allowed_signature_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    token_query_parameter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335b31ac1b57179360e5b9b61055ad0b7462c08a305d916d6d4aeae2ebdecdb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ff97bfc4d0feb3668bd6ca6fd7627374485f74ad767ccd831b770a04b6dd95(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6db54fe7788701c0778ff1282998d9c0dbc804557b18d36f2e90daeef196be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e909d3859b20f029d51a40c0468564398a4f4dbc3102e83a600a0677ef06d2b(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCdnPolicySignedTokenOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ed6557af2544a57f91b5a0faf70384db890fe93c241cc90a1f6835bbce6178(
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

def _typecheckingstub__193832c6b5d8e9cc4af14044273b7e749c7900cb1974b4606440372651e8a76b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66840004ee8b05c4096d376532f9fa039a0e1e86cd7e1f649e5cdf37846ea1c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ed1159a17d8480a4f5012515b2e97257b85abc800feba966d9f54d3d4595ed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7b5e66200e55c5ec24b8e5d51f55a639d4c82b1c02bee7375d3c5c329e12a5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea26e932195715a2cc3fbd11c3398958ae983352501a57358148b6d092b49df2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d55ca3a5c7b1bdadbd3f0a4809807b51fef39c7d244d2a3ca9546a9f4b8283e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__768265dd6f65d1027e80307bf36129e76e572750be8f237691bba17838799fa6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f02fb826f39ce601eb2a47afa5b06c4e965ac3c41a3eca92728b5adfaf1b3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d3409492fac3b1290ab4b489ef696c47fe6ac3393c8242d425ea60aae5240c4(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionCorsPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792a7856c5833563827483d8cea13aee7c4395d0839e863ead69820a0b4bb801(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f428ebed05ad1965812b9a2184ef7a8cef855dc2c634750b32de2bf5de29338a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653a5b37047e9740efd641176c6a1f00a72c4d976e693a84e6bce5969d4da7f2(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d48925c97e70c5672b2621b4cbbfc287a5195d138eed31e7a326581727d34d6(
    *,
    host_rewrite: typing.Optional[builtins.str] = None,
    path_prefix_rewrite: typing.Optional[builtins.str] = None,
    path_template_rewrite: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8afe302fc427c7c25999c223dfbd294dc727b5ba11cc7d02d55085be28ff49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91fc3bc3ed0782c9aa5f43973e8414581d4a2b96655c7e8624561dd0c1a3dd0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29eccd9aa90ab84a681e182db6d6dec828d7ab73c156505f5b4b9a6f7d3dcdee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb90d73dabf4c9f772a44f29164898be4f99902b9558809a5882c3fa1ecf154(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd241d2992b3e53bd6df4f3fb72df6e75107216ebe10d1762af9e8122024be51(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteActionUrlRewrite],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59a8dbc3ed3465c230fcfc15b886b83f2e08adbbb82e3d8c11645d85c47c2b5(
    *,
    allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b44cfc1f719b50d6fb43b5265ab82af96723196f1b7a84930d93b311308159(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d225f9f593ceeb802d38a957ba086bd4e6aae8c1b63602c07b9a8d86753a468e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca83f9d8ac6d418df34690baa9b04e57400dfb0b2655bb7aeaa34aa55d136b3(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleRouteMethods],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb6cfbc71f97a59676ff77905d823ed348a36e3ebc297f6ab33d65ce7a2e4f3(
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

def _typecheckingstub__c705f6be4ae0916a9a36a9c62f506bcdd4be9ab6ab6737224352a64b1c385d72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764335ce93c076ff89c3e2842bf129eac48822d9f2f62b02f900797f5d955784(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68959660448ddf02f8fe069b500a52f5ea428f352dd57e3a03ab026cde1e9a8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7885518cce40a6c8e36cd12da1a51feb0a4fbe8517b4d9007bd7907af374b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5787bee05c0949798574b9b911a54bdf153337372162b602054424380d7db97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeaf8b28274bdd04f965aaef7e33cfd15104185c3d4c1ca33f31762cc87f3745(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820f6edf197e31d5dbd2e874f2cf074ef85d0f1398b22649635597bf906642fe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270461706ad69b4b90064264680ebe8d69e8637e0cc1b4c82b6b48217e46f92a(
    value: typing.Optional[GoogleNetworkServicesEdgeCacheServiceRoutingPathMatcherRouteRuleUrlRedirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5179b815ef9b7083cf47b37dc8c9695a3b16d7f02183aaa2ed196115df2c3d0f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5166f1207f4ed2298bfa3160182b0729bdfa7f5eb6c01813e5b1dd7719ed9595(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b857901780e1540f4f88757c1f5af93d09ef7b09b339b05c57d02fe7ea29e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa3069db29d9149aa2a4202f17e8cd8cb5e90fd574c4f299bc2990246a109b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de77bb26f9811938e194b8f2deb41eaa12e2cc74b5ac7b22227a7e399ec16ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4924864744e22e0c9cfe7e555c75c16e028e4631b4624a43cd399881af439c67(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesEdgeCacheServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
