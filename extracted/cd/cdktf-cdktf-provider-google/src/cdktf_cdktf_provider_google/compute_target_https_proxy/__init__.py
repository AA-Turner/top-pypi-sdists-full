r'''
# `google_compute_target_https_proxy`

Refer to the Terraform Registry for docs: [`google_compute_target_https_proxy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy).
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


class ComputeTargetHttpsProxy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeTargetHttpsProxy.ComputeTargetHttpsProxy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy google_compute_target_https_proxy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        url_map: builtins.str,
        certificate_manager_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        certificate_map: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        http_keep_alive_timeout_sec: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        proxy_bind: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        quic_override: typing.Optional[builtins.str] = None,
        server_tls_policy: typing.Optional[builtins.str] = None,
        ssl_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeTargetHttpsProxyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_early_data: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy google_compute_target_https_proxy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#name ComputeTargetHttpsProxy#name}
        :param url_map: A reference to the UrlMap resource that defines the mapping from URL to the BackendService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#url_map ComputeTargetHttpsProxy#url_map}
        :param certificate_manager_certificates: URLs to certificate manager certificate resources that are used to authenticate connections between users and the load balancer. Certificate manager certificates only apply when the load balancing scheme is set to INTERNAL_MANAGED. For EXTERNAL and EXTERNAL_MANAGED, use certificate_map instead. sslCertificates and certificateManagerCertificates fields can not be defined together. Accepted format is '//certificatemanager.googleapis.com/projects/{project}/locations/{location}/certificates/{resourceName}' or just the self_link 'projects/{project}/locations/{location}/certificates/{resourceName}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#certificate_manager_certificates ComputeTargetHttpsProxy#certificate_manager_certificates}
        :param certificate_map: A reference to the CertificateMap resource uri that identifies a certificate map associated with the given target proxy. This field is only supported for EXTERNAL and EXTERNAL_MANAGED load balancing schemes. For INTERNAL_MANAGED, use certificate_manager_certificates instead. Accepted format is '//certificatemanager.googleapis.com/projects/{project}/locations/{location}/certificateMaps/{resourceName}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#certificate_map ComputeTargetHttpsProxy#certificate_map}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#description ComputeTargetHttpsProxy#description}
        :param http_keep_alive_timeout_sec: Specifies how long to keep a connection open, after completing a response, while there is no matching traffic (in seconds). If an HTTP keepalive is not specified, a default value will be used. For Global external HTTP(S) load balancer, the default value is 610 seconds, the minimum allowed value is 5 seconds and the maximum allowed value is 1200 seconds. For cross-region internal HTTP(S) load balancer, the default value is 600 seconds, the minimum allowed value is 5 seconds, and the maximum allowed value is 600 seconds. For Global external HTTP(S) load balancer (classic), this option is not available publicly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#http_keep_alive_timeout_sec ComputeTargetHttpsProxy#http_keep_alive_timeout_sec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#id ComputeTargetHttpsProxy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#project ComputeTargetHttpsProxy#project}.
        :param proxy_bind: This field only applies when the forwarding rule that references this target proxy has a loadBalancingScheme set to INTERNAL_SELF_MANAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#proxy_bind ComputeTargetHttpsProxy#proxy_bind}
        :param quic_override: Specifies the QUIC override policy for this resource. This determines whether the load balancer will attempt to negotiate QUIC with clients or not. Can specify one of NONE, ENABLE, or DISABLE. If NONE is specified, Google manages whether QUIC is used. Default value: "NONE" Possible values: ["NONE", "ENABLE", "DISABLE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#quic_override ComputeTargetHttpsProxy#quic_override}
        :param server_tls_policy: A URL referring to a networksecurity.ServerTlsPolicy resource that describes how the proxy should authenticate inbound traffic. serverTlsPolicy only applies to a global TargetHttpsProxy attached to globalForwardingRules with the loadBalancingScheme set to INTERNAL_SELF_MANAGED or EXTERNAL or EXTERNAL_MANAGED. For details which ServerTlsPolicy resources are accepted with INTERNAL_SELF_MANAGED and which with EXTERNAL, EXTERNAL_MANAGED loadBalancingScheme consult ServerTlsPolicy documentation. If left blank, communications are not encrypted. If you remove this field from your configuration at the same time as deleting or recreating a referenced ServerTlsPolicy resource, you will receive a resourceInUseByAnotherResource error. Use lifecycle.create_before_destroy within the ServerTlsPolicy resource to avoid this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#server_tls_policy ComputeTargetHttpsProxy#server_tls_policy}
        :param ssl_certificates: URLs to SslCertificate resources that are used to authenticate connections between users and the load balancer. Currently, you may specify up to 15 SSL certificates. sslCertificates do not apply when the load balancing scheme is set to INTERNAL_SELF_MANAGED. sslCertificates and certificateManagerCertificates can not be defined together. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#ssl_certificates ComputeTargetHttpsProxy#ssl_certificates}
        :param ssl_policy: A reference to the SslPolicy resource that will be associated with the TargetHttpsProxy resource. If not set, the TargetHttpsProxy resource will not have any SSL policy configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#ssl_policy ComputeTargetHttpsProxy#ssl_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#timeouts ComputeTargetHttpsProxy#timeouts}
        :param tls_early_data: Specifies whether TLS 1.3 0-RTT Data (“Early Data”) should be accepted for this service. Early Data allows a TLS resumption handshake to include the initial application payload (a HTTP request) alongside the handshake, reducing the effective round trips to “zero”. This applies to TLS 1.3 connections over TCP (HTTP/2) as well as over UDP (QUIC/h3). Possible values: ["STRICT", "PERMISSIVE", "UNRESTRICTED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#tls_early_data ComputeTargetHttpsProxy#tls_early_data}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d71cc5483b57274113c19b889eea2779cd4b7c4a9ae6ed66ab9233651facd8c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeTargetHttpsProxyConfig(
            name=name,
            url_map=url_map,
            certificate_manager_certificates=certificate_manager_certificates,
            certificate_map=certificate_map,
            description=description,
            http_keep_alive_timeout_sec=http_keep_alive_timeout_sec,
            id=id,
            project=project,
            proxy_bind=proxy_bind,
            quic_override=quic_override,
            server_tls_policy=server_tls_policy,
            ssl_certificates=ssl_certificates,
            ssl_policy=ssl_policy,
            timeouts=timeouts,
            tls_early_data=tls_early_data,
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
        '''Generates CDKTF code for importing a ComputeTargetHttpsProxy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeTargetHttpsProxy to import.
        :param import_from_id: The id of the existing ComputeTargetHttpsProxy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeTargetHttpsProxy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787a5cae323880e663cf3c94b5e707d826bac29b1915f08d184432e5fdd14d95)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#create ComputeTargetHttpsProxy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#delete ComputeTargetHttpsProxy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#update ComputeTargetHttpsProxy#update}.
        '''
        value = ComputeTargetHttpsProxyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCertificateManagerCertificates")
    def reset_certificate_manager_certificates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateManagerCertificates", []))

    @jsii.member(jsii_name="resetCertificateMap")
    def reset_certificate_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateMap", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHttpKeepAliveTimeoutSec")
    def reset_http_keep_alive_timeout_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpKeepAliveTimeoutSec", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProxyBind")
    def reset_proxy_bind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyBind", []))

    @jsii.member(jsii_name="resetQuicOverride")
    def reset_quic_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuicOverride", []))

    @jsii.member(jsii_name="resetServerTlsPolicy")
    def reset_server_tls_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerTlsPolicy", []))

    @jsii.member(jsii_name="resetSslCertificates")
    def reset_ssl_certificates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCertificates", []))

    @jsii.member(jsii_name="resetSslPolicy")
    def reset_ssl_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslPolicy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTlsEarlyData")
    def reset_tls_early_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsEarlyData", []))

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
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="fingerprint")
    def fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fingerprint"))

    @builtins.property
    @jsii.member(jsii_name="proxyId")
    def proxy_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "proxyId"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeTargetHttpsProxyTimeoutsOutputReference":
        return typing.cast("ComputeTargetHttpsProxyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="certificateManagerCertificatesInput")
    def certificate_manager_certificates_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "certificateManagerCertificatesInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateMapInput")
    def certificate_map_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateMapInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="httpKeepAliveTimeoutSecInput")
    def http_keep_alive_timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpKeepAliveTimeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyBindInput")
    def proxy_bind_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "proxyBindInput"))

    @builtins.property
    @jsii.member(jsii_name="quicOverrideInput")
    def quic_override_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quicOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="serverTlsPolicyInput")
    def server_tls_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverTlsPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCertificatesInput")
    def ssl_certificates_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sslCertificatesInput"))

    @builtins.property
    @jsii.member(jsii_name="sslPolicyInput")
    def ssl_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeTargetHttpsProxyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeTargetHttpsProxyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsEarlyDataInput")
    def tls_early_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsEarlyDataInput"))

    @builtins.property
    @jsii.member(jsii_name="urlMapInput")
    def url_map_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlMapInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateManagerCertificates")
    def certificate_manager_certificates(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "certificateManagerCertificates"))

    @certificate_manager_certificates.setter
    def certificate_manager_certificates(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe481002406d1a67ad9978d07468319660660a8e62ef69c4f93f4ba5477b0361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateManagerCertificates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificateMap")
    def certificate_map(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateMap"))

    @certificate_map.setter
    def certificate_map(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__259e81acc1fdb9ebbabcfce119a10a9d9d043872e685df298c9db2a711a229a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateMap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c60df3952bf782df52241499ae90e7a81c60a4998eeef3b874dec64c6bd58232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpKeepAliveTimeoutSec")
    def http_keep_alive_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpKeepAliveTimeoutSec"))

    @http_keep_alive_timeout_sec.setter
    def http_keep_alive_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbe95c4a6884b6f3cc1290ba1eec9bc05112652098503cabe3f626b9fed6916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpKeepAliveTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c33b1ca9b709bf48e25e5321a768f1ca55e7749eb7b3e190f2d30b1360a252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa1ad6df765eb672bb0a17ca2029eac780c0ad41bddee4f5f9be2e1da33dad6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__837f1f05dde9594e6a9110f663c4c0f19a34ef176669036438c44daa9f1c0518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyBind")
    def proxy_bind(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "proxyBind"))

    @proxy_bind.setter
    def proxy_bind(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82e88bfdcfc8caa00f05630459508e2ad04927d487085c0631679276b484bf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyBind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quicOverride")
    def quic_override(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quicOverride"))

    @quic_override.setter
    def quic_override(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53466de55808cce917d349098bbc0ee75452cad27ebdbbbd6ac918fc56ff9ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quicOverride", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverTlsPolicy")
    def server_tls_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverTlsPolicy"))

    @server_tls_policy.setter
    def server_tls_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21cabf8e22cb6271ef92ae26ae272f3467083d2a4c232f5d8d887c6918cb851c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverTlsPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCertificates")
    def ssl_certificates(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sslCertificates"))

    @ssl_certificates.setter
    def ssl_certificates(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4109bee3a96f076d6c009d4eff70ac7628b0ceef352c5dbc3bd5160ff51bc2c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCertificates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslPolicy")
    def ssl_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslPolicy"))

    @ssl_policy.setter
    def ssl_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b56ecd063b0b92b62007a6bf2f45ba6a0f6e6bec105e3eb2f5421d292c866d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsEarlyData")
    def tls_early_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsEarlyData"))

    @tls_early_data.setter
    def tls_early_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d8f2fa89f274464b95b6f426ef70099d06fafd1c7ac5a370afab43def2388d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsEarlyData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlMap")
    def url_map(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlMap"))

    @url_map.setter
    def url_map(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__577508568afc7792ebf6c6e6b0382cbfe15a3326559250451d1f39c5ea30f1b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlMap", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeTargetHttpsProxy.ComputeTargetHttpsProxyConfig",
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
        "url_map": "urlMap",
        "certificate_manager_certificates": "certificateManagerCertificates",
        "certificate_map": "certificateMap",
        "description": "description",
        "http_keep_alive_timeout_sec": "httpKeepAliveTimeoutSec",
        "id": "id",
        "project": "project",
        "proxy_bind": "proxyBind",
        "quic_override": "quicOverride",
        "server_tls_policy": "serverTlsPolicy",
        "ssl_certificates": "sslCertificates",
        "ssl_policy": "sslPolicy",
        "timeouts": "timeouts",
        "tls_early_data": "tlsEarlyData",
    },
)
class ComputeTargetHttpsProxyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        url_map: builtins.str,
        certificate_manager_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        certificate_map: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        http_keep_alive_timeout_sec: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        proxy_bind: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        quic_override: typing.Optional[builtins.str] = None,
        server_tls_policy: typing.Optional[builtins.str] = None,
        ssl_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeTargetHttpsProxyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_early_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#name ComputeTargetHttpsProxy#name}
        :param url_map: A reference to the UrlMap resource that defines the mapping from URL to the BackendService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#url_map ComputeTargetHttpsProxy#url_map}
        :param certificate_manager_certificates: URLs to certificate manager certificate resources that are used to authenticate connections between users and the load balancer. Certificate manager certificates only apply when the load balancing scheme is set to INTERNAL_MANAGED. For EXTERNAL and EXTERNAL_MANAGED, use certificate_map instead. sslCertificates and certificateManagerCertificates fields can not be defined together. Accepted format is '//certificatemanager.googleapis.com/projects/{project}/locations/{location}/certificates/{resourceName}' or just the self_link 'projects/{project}/locations/{location}/certificates/{resourceName}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#certificate_manager_certificates ComputeTargetHttpsProxy#certificate_manager_certificates}
        :param certificate_map: A reference to the CertificateMap resource uri that identifies a certificate map associated with the given target proxy. This field is only supported for EXTERNAL and EXTERNAL_MANAGED load balancing schemes. For INTERNAL_MANAGED, use certificate_manager_certificates instead. Accepted format is '//certificatemanager.googleapis.com/projects/{project}/locations/{location}/certificateMaps/{resourceName}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#certificate_map ComputeTargetHttpsProxy#certificate_map}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#description ComputeTargetHttpsProxy#description}
        :param http_keep_alive_timeout_sec: Specifies how long to keep a connection open, after completing a response, while there is no matching traffic (in seconds). If an HTTP keepalive is not specified, a default value will be used. For Global external HTTP(S) load balancer, the default value is 610 seconds, the minimum allowed value is 5 seconds and the maximum allowed value is 1200 seconds. For cross-region internal HTTP(S) load balancer, the default value is 600 seconds, the minimum allowed value is 5 seconds, and the maximum allowed value is 600 seconds. For Global external HTTP(S) load balancer (classic), this option is not available publicly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#http_keep_alive_timeout_sec ComputeTargetHttpsProxy#http_keep_alive_timeout_sec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#id ComputeTargetHttpsProxy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#project ComputeTargetHttpsProxy#project}.
        :param proxy_bind: This field only applies when the forwarding rule that references this target proxy has a loadBalancingScheme set to INTERNAL_SELF_MANAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#proxy_bind ComputeTargetHttpsProxy#proxy_bind}
        :param quic_override: Specifies the QUIC override policy for this resource. This determines whether the load balancer will attempt to negotiate QUIC with clients or not. Can specify one of NONE, ENABLE, or DISABLE. If NONE is specified, Google manages whether QUIC is used. Default value: "NONE" Possible values: ["NONE", "ENABLE", "DISABLE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#quic_override ComputeTargetHttpsProxy#quic_override}
        :param server_tls_policy: A URL referring to a networksecurity.ServerTlsPolicy resource that describes how the proxy should authenticate inbound traffic. serverTlsPolicy only applies to a global TargetHttpsProxy attached to globalForwardingRules with the loadBalancingScheme set to INTERNAL_SELF_MANAGED or EXTERNAL or EXTERNAL_MANAGED. For details which ServerTlsPolicy resources are accepted with INTERNAL_SELF_MANAGED and which with EXTERNAL, EXTERNAL_MANAGED loadBalancingScheme consult ServerTlsPolicy documentation. If left blank, communications are not encrypted. If you remove this field from your configuration at the same time as deleting or recreating a referenced ServerTlsPolicy resource, you will receive a resourceInUseByAnotherResource error. Use lifecycle.create_before_destroy within the ServerTlsPolicy resource to avoid this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#server_tls_policy ComputeTargetHttpsProxy#server_tls_policy}
        :param ssl_certificates: URLs to SslCertificate resources that are used to authenticate connections between users and the load balancer. Currently, you may specify up to 15 SSL certificates. sslCertificates do not apply when the load balancing scheme is set to INTERNAL_SELF_MANAGED. sslCertificates and certificateManagerCertificates can not be defined together. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#ssl_certificates ComputeTargetHttpsProxy#ssl_certificates}
        :param ssl_policy: A reference to the SslPolicy resource that will be associated with the TargetHttpsProxy resource. If not set, the TargetHttpsProxy resource will not have any SSL policy configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#ssl_policy ComputeTargetHttpsProxy#ssl_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#timeouts ComputeTargetHttpsProxy#timeouts}
        :param tls_early_data: Specifies whether TLS 1.3 0-RTT Data (“Early Data”) should be accepted for this service. Early Data allows a TLS resumption handshake to include the initial application payload (a HTTP request) alongside the handshake, reducing the effective round trips to “zero”. This applies to TLS 1.3 connections over TCP (HTTP/2) as well as over UDP (QUIC/h3). Possible values: ["STRICT", "PERMISSIVE", "UNRESTRICTED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#tls_early_data ComputeTargetHttpsProxy#tls_early_data}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ComputeTargetHttpsProxyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__727af549a311c8e8c8f0255bc1be06025d30f41ddd4acab39a32e12752f0edda)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url_map", value=url_map, expected_type=type_hints["url_map"])
            check_type(argname="argument certificate_manager_certificates", value=certificate_manager_certificates, expected_type=type_hints["certificate_manager_certificates"])
            check_type(argname="argument certificate_map", value=certificate_map, expected_type=type_hints["certificate_map"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument http_keep_alive_timeout_sec", value=http_keep_alive_timeout_sec, expected_type=type_hints["http_keep_alive_timeout_sec"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument proxy_bind", value=proxy_bind, expected_type=type_hints["proxy_bind"])
            check_type(argname="argument quic_override", value=quic_override, expected_type=type_hints["quic_override"])
            check_type(argname="argument server_tls_policy", value=server_tls_policy, expected_type=type_hints["server_tls_policy"])
            check_type(argname="argument ssl_certificates", value=ssl_certificates, expected_type=type_hints["ssl_certificates"])
            check_type(argname="argument ssl_policy", value=ssl_policy, expected_type=type_hints["ssl_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument tls_early_data", value=tls_early_data, expected_type=type_hints["tls_early_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "url_map": url_map,
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
        if certificate_manager_certificates is not None:
            self._values["certificate_manager_certificates"] = certificate_manager_certificates
        if certificate_map is not None:
            self._values["certificate_map"] = certificate_map
        if description is not None:
            self._values["description"] = description
        if http_keep_alive_timeout_sec is not None:
            self._values["http_keep_alive_timeout_sec"] = http_keep_alive_timeout_sec
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if proxy_bind is not None:
            self._values["proxy_bind"] = proxy_bind
        if quic_override is not None:
            self._values["quic_override"] = quic_override
        if server_tls_policy is not None:
            self._values["server_tls_policy"] = server_tls_policy
        if ssl_certificates is not None:
            self._values["ssl_certificates"] = ssl_certificates
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if tls_early_data is not None:
            self._values["tls_early_data"] = tls_early_data

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
        '''Name of the resource.

        Provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and match
        the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#name ComputeTargetHttpsProxy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url_map(self) -> builtins.str:
        '''A reference to the UrlMap resource that defines the mapping from URL to the BackendService.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#url_map ComputeTargetHttpsProxy#url_map}
        '''
        result = self._values.get("url_map")
        assert result is not None, "Required property 'url_map' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_manager_certificates(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''URLs to certificate manager certificate resources that are used to authenticate connections between users and the load balancer.

        Certificate manager certificates only apply when the load balancing scheme is set to INTERNAL_MANAGED.
        For EXTERNAL and EXTERNAL_MANAGED, use certificate_map instead.
        sslCertificates and certificateManagerCertificates fields can not be defined together.
        Accepted format is '//certificatemanager.googleapis.com/projects/{project}/locations/{location}/certificates/{resourceName}' or just the self_link 'projects/{project}/locations/{location}/certificates/{resourceName}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#certificate_manager_certificates ComputeTargetHttpsProxy#certificate_manager_certificates}
        '''
        result = self._values.get("certificate_manager_certificates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def certificate_map(self) -> typing.Optional[builtins.str]:
        '''A reference to the CertificateMap resource uri that identifies a certificate map associated with the given target proxy.

        This field is only supported for EXTERNAL and EXTERNAL_MANAGED load balancing schemes.
        For INTERNAL_MANAGED, use certificate_manager_certificates instead.
        Accepted format is '//certificatemanager.googleapis.com/projects/{project}/locations/{location}/certificateMaps/{resourceName}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#certificate_map ComputeTargetHttpsProxy#certificate_map}
        '''
        result = self._values.get("certificate_map")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#description ComputeTargetHttpsProxy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_keep_alive_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Specifies how long to keep a connection open, after completing a response, while there is no matching traffic (in seconds).

        If an HTTP keepalive is
        not specified, a default value will be used. For Global
        external HTTP(S) load balancer, the default value is 610 seconds, the
        minimum allowed value is 5 seconds and the maximum allowed value is 1200
        seconds. For cross-region internal HTTP(S) load balancer, the default
        value is 600 seconds, the minimum allowed value is 5 seconds, and the
        maximum allowed value is 600 seconds. For Global external HTTP(S) load
        balancer (classic), this option is not available publicly.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#http_keep_alive_timeout_sec ComputeTargetHttpsProxy#http_keep_alive_timeout_sec}
        '''
        result = self._values.get("http_keep_alive_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#id ComputeTargetHttpsProxy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#project ComputeTargetHttpsProxy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_bind(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This field only applies when the forwarding rule that references this target proxy has a loadBalancingScheme set to INTERNAL_SELF_MANAGED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#proxy_bind ComputeTargetHttpsProxy#proxy_bind}
        '''
        result = self._values.get("proxy_bind")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def quic_override(self) -> typing.Optional[builtins.str]:
        '''Specifies the QUIC override policy for this resource.

        This determines
        whether the load balancer will attempt to negotiate QUIC with clients
        or not. Can specify one of NONE, ENABLE, or DISABLE. If NONE is
        specified, Google manages whether QUIC is used. Default value: "NONE" Possible values: ["NONE", "ENABLE", "DISABLE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#quic_override ComputeTargetHttpsProxy#quic_override}
        '''
        result = self._values.get("quic_override")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_tls_policy(self) -> typing.Optional[builtins.str]:
        '''A URL referring to a networksecurity.ServerTlsPolicy resource that describes how the proxy should authenticate inbound traffic. serverTlsPolicy only applies to a global TargetHttpsProxy attached to globalForwardingRules with the loadBalancingScheme set to INTERNAL_SELF_MANAGED or EXTERNAL or EXTERNAL_MANAGED. For details which ServerTlsPolicy resources are accepted with INTERNAL_SELF_MANAGED and which with EXTERNAL, EXTERNAL_MANAGED loadBalancingScheme consult ServerTlsPolicy documentation. If left blank, communications are not encrypted.

        If you remove this field from your configuration at the same time as
        deleting or recreating a referenced ServerTlsPolicy resource, you will
        receive a resourceInUseByAnotherResource error. Use lifecycle.create_before_destroy
        within the ServerTlsPolicy resource to avoid this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#server_tls_policy ComputeTargetHttpsProxy#server_tls_policy}
        '''
        result = self._values.get("server_tls_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_certificates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URLs to SslCertificate resources that are used to authenticate connections between users and the load balancer.

        Currently, you may specify up to 15 SSL certificates. sslCertificates do not apply when the load balancing scheme is set to INTERNAL_SELF_MANAGED.
        sslCertificates and certificateManagerCertificates can not be defined together.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#ssl_certificates ComputeTargetHttpsProxy#ssl_certificates}
        '''
        result = self._values.get("ssl_certificates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ssl_policy(self) -> typing.Optional[builtins.str]:
        '''A reference to the SslPolicy resource that will be associated with the TargetHttpsProxy resource.

        If not set, the TargetHttpsProxy
        resource will not have any SSL policy configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#ssl_policy ComputeTargetHttpsProxy#ssl_policy}
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeTargetHttpsProxyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#timeouts ComputeTargetHttpsProxy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeTargetHttpsProxyTimeouts"], result)

    @builtins.property
    def tls_early_data(self) -> typing.Optional[builtins.str]:
        '''Specifies whether TLS 1.3 0-RTT Data (“Early Data”) should be accepted for this service. Early Data allows a TLS resumption handshake to include the initial application payload (a HTTP request) alongside the handshake, reducing the effective round trips to “zero”. This applies to TLS 1.3 connections over TCP (HTTP/2) as well as over UDP (QUIC/h3). Possible values: ["STRICT", "PERMISSIVE", "UNRESTRICTED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#tls_early_data ComputeTargetHttpsProxy#tls_early_data}
        '''
        result = self._values.get("tls_early_data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeTargetHttpsProxyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeTargetHttpsProxy.ComputeTargetHttpsProxyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeTargetHttpsProxyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#create ComputeTargetHttpsProxy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#delete ComputeTargetHttpsProxy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#update ComputeTargetHttpsProxy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862c1978266e9a3f883996255febea239e1d9b13dbe763d4669b4ca3b484c657)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#create ComputeTargetHttpsProxy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#delete ComputeTargetHttpsProxy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_target_https_proxy#update ComputeTargetHttpsProxy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeTargetHttpsProxyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeTargetHttpsProxyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeTargetHttpsProxy.ComputeTargetHttpsProxyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f964d4b43913939cf83e20c598bbb61efea67ebf292944c22c18e3400332cf5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52af22a1df1649f1ce55e33e57af7cf4aa7247e4f4304a127cb94e22b7239a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76161e5df6620e71d2e3f1346cdbae0f4cc2a465b4cb0942309494e0967bbca7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce02a6dd05aca29bd269a5b02725a408827264140f153f3bbc3ab5e495f026cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeTargetHttpsProxyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeTargetHttpsProxyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeTargetHttpsProxyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdfff11fd25089684f9bf9f82d9f68aaeebcc91b2f86534017b85b658383c76e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeTargetHttpsProxy",
    "ComputeTargetHttpsProxyConfig",
    "ComputeTargetHttpsProxyTimeouts",
    "ComputeTargetHttpsProxyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2d71cc5483b57274113c19b889eea2779cd4b7c4a9ae6ed66ab9233651facd8c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    url_map: builtins.str,
    certificate_manager_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    certificate_map: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    http_keep_alive_timeout_sec: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    proxy_bind: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    quic_override: typing.Optional[builtins.str] = None,
    server_tls_policy: typing.Optional[builtins.str] = None,
    ssl_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssl_policy: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeTargetHttpsProxyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_early_data: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__787a5cae323880e663cf3c94b5e707d826bac29b1915f08d184432e5fdd14d95(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe481002406d1a67ad9978d07468319660660a8e62ef69c4f93f4ba5477b0361(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259e81acc1fdb9ebbabcfce119a10a9d9d043872e685df298c9db2a711a229a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60df3952bf782df52241499ae90e7a81c60a4998eeef3b874dec64c6bd58232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbe95c4a6884b6f3cc1290ba1eec9bc05112652098503cabe3f626b9fed6916(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c33b1ca9b709bf48e25e5321a768f1ca55e7749eb7b3e190f2d30b1360a252(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa1ad6df765eb672bb0a17ca2029eac780c0ad41bddee4f5f9be2e1da33dad6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837f1f05dde9594e6a9110f663c4c0f19a34ef176669036438c44daa9f1c0518(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82e88bfdcfc8caa00f05630459508e2ad04927d487085c0631679276b484bf4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53466de55808cce917d349098bbc0ee75452cad27ebdbbbd6ac918fc56ff9ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21cabf8e22cb6271ef92ae26ae272f3467083d2a4c232f5d8d887c6918cb851c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4109bee3a96f076d6c009d4eff70ac7628b0ceef352c5dbc3bd5160ff51bc2c4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b56ecd063b0b92b62007a6bf2f45ba6a0f6e6bec105e3eb2f5421d292c866d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d8f2fa89f274464b95b6f426ef70099d06fafd1c7ac5a370afab43def2388d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__577508568afc7792ebf6c6e6b0382cbfe15a3326559250451d1f39c5ea30f1b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727af549a311c8e8c8f0255bc1be06025d30f41ddd4acab39a32e12752f0edda(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    url_map: builtins.str,
    certificate_manager_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    certificate_map: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    http_keep_alive_timeout_sec: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    proxy_bind: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    quic_override: typing.Optional[builtins.str] = None,
    server_tls_policy: typing.Optional[builtins.str] = None,
    ssl_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssl_policy: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeTargetHttpsProxyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_early_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862c1978266e9a3f883996255febea239e1d9b13dbe763d4669b4ca3b484c657(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f964d4b43913939cf83e20c598bbb61efea67ebf292944c22c18e3400332cf5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52af22a1df1649f1ce55e33e57af7cf4aa7247e4f4304a127cb94e22b7239a48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76161e5df6620e71d2e3f1346cdbae0f4cc2a465b4cb0942309494e0967bbca7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce02a6dd05aca29bd269a5b02725a408827264140f153f3bbc3ab5e495f026cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdfff11fd25089684f9bf9f82d9f68aaeebcc91b2f86534017b85b658383c76e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeTargetHttpsProxyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
