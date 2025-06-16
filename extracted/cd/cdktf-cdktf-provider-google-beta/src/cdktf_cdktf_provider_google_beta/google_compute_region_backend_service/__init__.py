r'''
# `google_compute_region_backend_service`

Refer to the Terraform Registry for docs: [`google_compute_region_backend_service`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service).
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


class GoogleComputeRegionBackendService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service google_compute_region_backend_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        affinity_cookie_ttl_sec: typing.Optional[jsii.Number] = None,
        backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionBackendServiceBackend", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cdn_policy: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceCdnPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        circuit_breakers: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceCircuitBreakers", typing.Dict[builtins.str, typing.Any]]] = None,
        connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
        connection_tracking_policy: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceConnectionTrackingPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        consistent_hash: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceConsistentHash", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionBackendServiceCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamic_forwarding: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceDynamicForwarding", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failover_policy: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceFailoverPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        iap: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceIap", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address_selection_policy: typing.Optional[builtins.str] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        locality_lb_policy: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[builtins.str] = None,
        outlier_detection: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceOutlierDetection", typing.Dict[builtins.str, typing.Any]]] = None,
        port_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        security_policy: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        strong_session_affinity_cookie: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceStrongSessionAffinityCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        subsetting: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceSubsetting", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_sec: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service google_compute_region_backend_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#name GoogleComputeRegionBackendService#name}
        :param affinity_cookie_ttl_sec: Lifetime of cookies in seconds if session_affinity is GENERATED_COOKIE. If set to 0, the cookie is non-persistent and lasts only until the end of the browser session (or equivalent). The maximum allowed value for TTL is one day. When the load balancing scheme is INTERNAL, this field is not used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#affinity_cookie_ttl_sec GoogleComputeRegionBackendService#affinity_cookie_ttl_sec}
        :param backend: backend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#backend GoogleComputeRegionBackendService#backend}
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#cdn_policy GoogleComputeRegionBackendService#cdn_policy}
        :param circuit_breakers: circuit_breakers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#circuit_breakers GoogleComputeRegionBackendService#circuit_breakers}
        :param connection_draining_timeout_sec: Time for which instance will be drained (not accept new connections, but still work to finish started). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#connection_draining_timeout_sec GoogleComputeRegionBackendService#connection_draining_timeout_sec}
        :param connection_tracking_policy: connection_tracking_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#connection_tracking_policy GoogleComputeRegionBackendService#connection_tracking_policy}
        :param consistent_hash: consistent_hash block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#consistent_hash GoogleComputeRegionBackendService#consistent_hash}
        :param custom_metrics: custom_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#custom_metrics GoogleComputeRegionBackendService#custom_metrics}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#description GoogleComputeRegionBackendService#description}
        :param dynamic_forwarding: dynamic_forwarding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#dynamic_forwarding GoogleComputeRegionBackendService#dynamic_forwarding}
        :param enable_cdn: If true, enable Cloud CDN for this RegionBackendService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enable_cdn GoogleComputeRegionBackendService#enable_cdn}
        :param failover_policy: failover_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#failover_policy GoogleComputeRegionBackendService#failover_policy}
        :param health_checks: The set of URLs to HealthCheck resources for health checking this RegionBackendService. Currently at most one health check can be specified. A health check must be specified unless the backend service uses an internet or serverless NEG as a backend. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#health_checks GoogleComputeRegionBackendService#health_checks}
        :param iap: iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#iap GoogleComputeRegionBackendService#iap}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#id GoogleComputeRegionBackendService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address_selection_policy: Specifies preference of traffic to the backend (from the proxy and from the client for proxyless gRPC). Possible values: ["IPV4_ONLY", "PREFER_IPV6", "IPV6_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ip_address_selection_policy GoogleComputeRegionBackendService#ip_address_selection_policy}
        :param load_balancing_scheme: Indicates what kind of load balancing this regional backend service will be used for. A backend service created for one type of load balancing cannot be used with the other(s). For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_. Default value: "INTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL", "INTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#load_balancing_scheme GoogleComputeRegionBackendService#load_balancing_scheme}
        :param locality_lb_policy: The load balancing algorithm used within the scope of the locality. The possible values are:. - 'ROUND_ROBIN': This is a simple policy in which each healthy backend is selected in round robin order. - 'LEAST_REQUEST': An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests. - 'RING_HASH': The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests. - 'RANDOM': The load balancer selects a random healthy host. - 'ORIGINAL_DESTINATION': Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer. - 'MAGLEV': used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, refer to https://ai.google/research/pubs/pub44824 - 'WEIGHTED_MAGLEV': Per-instance weighted Load Balancing via health check reported weights. Only applicable to loadBalancingScheme EXTERNAL. If set, the Backend Service must configure a non legacy HTTP-based Health Check, and health check replies are expected to contain non-standard HTTP response header field X-Load-Balancing-Endpoint-Weight to specify the per-instance weights. If set, Load Balancing is weight based on the per-instance weights reported in the last processed health check replies, as long as every instance either reported a valid weight or had UNAVAILABLE_WEIGHT. Otherwise, Load Balancing remains equal-weight. - 'WEIGHTED_ROUND_ROBIN': Per-endpoint weighted round-robin Load Balancing using weights computed from Backend reported Custom Metrics. If set, the Backend Service responses are expected to contain non-standard HTTP response header field X-Endpoint-Load-Metrics. The reported metrics to use for computing the weights are specified via the backends[].customMetrics fields. locality_lb_policy is applicable to either: - A regional backend service with the service_protocol set to HTTP, HTTPS, HTTP2 or H2C, and loadBalancingScheme set to INTERNAL_MANAGED. - A global backend service with the load_balancing_scheme set to INTERNAL_SELF_MANAGED. - A regional backend service with loadBalancingScheme set to EXTERNAL (External Network Load Balancing). Only MAGLEV and WEIGHTED_MAGLEV values are possible for External Network Load Balancing. The default is MAGLEV. If session_affinity is not NONE, and locality_lb_policy is not set to MAGLEV, WEIGHTED_MAGLEV, or RING_HASH, session affinity settings will not take effect. Only ROUND_ROBIN and RING_HASH are supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validate_for_proxyless field set to true. Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV", "WEIGHTED_MAGLEV", "WEIGHTED_ROUND_ROBIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#locality_lb_policy GoogleComputeRegionBackendService#locality_lb_policy}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#log_config GoogleComputeRegionBackendService#log_config}
        :param network: The URL of the network to which this backend service belongs. This field can only be specified when the load balancing scheme is set to INTERNAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#network GoogleComputeRegionBackendService#network}
        :param outlier_detection: outlier_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#outlier_detection GoogleComputeRegionBackendService#outlier_detection}
        :param port_name: A named port on a backend instance group representing the port for communication to the backend VMs in that group. Required when the loadBalancingScheme is EXTERNAL, EXTERNAL_MANAGED, INTERNAL_MANAGED, or INTERNAL_SELF_MANAGED and the backends are instance groups. The named port must be defined on each backend instance group. This parameter has no meaning if the backends are NEGs. API sets a default of "http" if not given. Must be omitted when the loadBalancingScheme is INTERNAL (Internal TCP/UDP Load Balancing). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#port_name GoogleComputeRegionBackendService#port_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#project GoogleComputeRegionBackendService#project}.
        :param protocol: The protocol this BackendService uses to communicate with backends. The default is HTTP. Possible values are HTTP, HTTPS, HTTP2, H2C, TCP, SSL, UDP or GRPC. Refer to the documentation for the load balancers or for Traffic Director for more information. Possible values: ["HTTP", "HTTPS", "HTTP2", "TCP", "SSL", "UDP", "GRPC", "UNSPECIFIED", "H2C"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#protocol GoogleComputeRegionBackendService#protocol}
        :param region: The Region in which the created backend service should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#region GoogleComputeRegionBackendService#region}
        :param security_policy: The security policy associated with this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#security_policy GoogleComputeRegionBackendService#security_policy}
        :param session_affinity: Type of session affinity to use. The default is NONE. Session affinity is not applicable if the protocol is UDP. Possible values: ["NONE", "CLIENT_IP", "CLIENT_IP_PORT_PROTO", "CLIENT_IP_PROTO", "GENERATED_COOKIE", "HEADER_FIELD", "HTTP_COOKIE", "CLIENT_IP_NO_DESTINATION", "STRONG_COOKIE_AFFINITY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#session_affinity GoogleComputeRegionBackendService#session_affinity}
        :param strong_session_affinity_cookie: strong_session_affinity_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#strong_session_affinity_cookie GoogleComputeRegionBackendService#strong_session_affinity_cookie}
        :param subsetting: subsetting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#subsetting GoogleComputeRegionBackendService#subsetting}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#timeouts GoogleComputeRegionBackendService#timeouts}
        :param timeout_sec: The backend service timeout has a different meaning depending on the type of load balancer. For more information see, `Backend service settings <https://cloud.google.com/compute/docs/reference/rest/v1/backendServices>`_. The default is 30 seconds. The full range of timeout values allowed goes from 1 through 2,147,483,647 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#timeout_sec GoogleComputeRegionBackendService#timeout_sec}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e16cc2d745a76f8cb556f7b43dcf234fece74dcd1b6d618d688f637e1557d77)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeRegionBackendServiceConfig(
            name=name,
            affinity_cookie_ttl_sec=affinity_cookie_ttl_sec,
            backend=backend,
            cdn_policy=cdn_policy,
            circuit_breakers=circuit_breakers,
            connection_draining_timeout_sec=connection_draining_timeout_sec,
            connection_tracking_policy=connection_tracking_policy,
            consistent_hash=consistent_hash,
            custom_metrics=custom_metrics,
            description=description,
            dynamic_forwarding=dynamic_forwarding,
            enable_cdn=enable_cdn,
            failover_policy=failover_policy,
            health_checks=health_checks,
            iap=iap,
            id=id,
            ip_address_selection_policy=ip_address_selection_policy,
            load_balancing_scheme=load_balancing_scheme,
            locality_lb_policy=locality_lb_policy,
            log_config=log_config,
            network=network,
            outlier_detection=outlier_detection,
            port_name=port_name,
            project=project,
            protocol=protocol,
            region=region,
            security_policy=security_policy,
            session_affinity=session_affinity,
            strong_session_affinity_cookie=strong_session_affinity_cookie,
            subsetting=subsetting,
            timeouts=timeouts,
            timeout_sec=timeout_sec,
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
        '''Generates CDKTF code for importing a GoogleComputeRegionBackendService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeRegionBackendService to import.
        :param import_from_id: The id of the existing GoogleComputeRegionBackendService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeRegionBackendService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27907a3b034f26dc85e3722ae1236483fcaf4d88b90b219d795e5a3e7a66e5c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackend")
    def put_backend(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionBackendServiceBackend", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe6af6df038d3611da5bc5cbe4479e61f81eb2d70cc6f4b33c2af0a6e1b1a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackend", [value]))

    @jsii.member(jsii_name="putCdnPolicy")
    def put_cdn_policy(
        self,
        *,
        cache_key_policy: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[jsii.Number] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        max_ttl: typing.Optional[jsii.Number] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        serve_while_stale: typing.Optional[jsii.Number] = None,
        signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#cache_key_policy GoogleComputeRegionBackendService#cache_key_policy}
        :param cache_mode: Specifies the cache setting for all responses from this backend. The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#cache_mode GoogleComputeRegionBackendService#cache_mode}
        :param client_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#client_ttl GoogleComputeRegionBackendService#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#default_ttl GoogleComputeRegionBackendService#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_ttl GoogleComputeRegionBackendService#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#negative_caching GoogleComputeRegionBackendService#negative_caching}
        :param negative_caching_policy: negative_caching_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#negative_caching_policy GoogleComputeRegionBackendService#negative_caching_policy}
        :param serve_while_stale: Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#serve_while_stale GoogleComputeRegionBackendService#serve_while_stale}
        :param signed_url_cache_max_age_sec: Maximum number of seconds the response to a signed URL request will be considered fresh, defaults to 1hr (3600s). After this time period, the response will be revalidated before being served. When serving responses to signed URL requests, Cloud CDN will internally behave as though all responses from this backend had a "Cache-Control: public, max-age=[TTL]" header, regardless of any existing Cache-Control header. The actual headers served in responses will not be altered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#signed_url_cache_max_age_sec GoogleComputeRegionBackendService#signed_url_cache_max_age_sec}
        '''
        value = GoogleComputeRegionBackendServiceCdnPolicy(
            cache_key_policy=cache_key_policy,
            cache_mode=cache_mode,
            client_ttl=client_ttl,
            default_ttl=default_ttl,
            max_ttl=max_ttl,
            negative_caching=negative_caching,
            negative_caching_policy=negative_caching_policy,
            serve_while_stale=serve_while_stale,
            signed_url_cache_max_age_sec=signed_url_cache_max_age_sec,
        )

        return typing.cast(None, jsii.invoke(self, "putCdnPolicy", [value]))

    @jsii.member(jsii_name="putCircuitBreakers")
    def put_circuit_breakers(
        self,
        *,
        connect_timeout: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        max_connections: typing.Optional[jsii.Number] = None,
        max_pending_requests: typing.Optional[jsii.Number] = None,
        max_requests: typing.Optional[jsii.Number] = None,
        max_requests_per_connection: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connect_timeout: connect_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#connect_timeout GoogleComputeRegionBackendService#connect_timeout}
        :param max_connections: The maximum number of connections to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_connections GoogleComputeRegionBackendService#max_connections}
        :param max_pending_requests: The maximum number of pending requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_pending_requests GoogleComputeRegionBackendService#max_pending_requests}
        :param max_requests: The maximum number of parallel requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_requests GoogleComputeRegionBackendService#max_requests}
        :param max_requests_per_connection: Maximum requests for a single backend connection. This parameter is respected by both the HTTP/1.1 and HTTP/2 implementations. If not specified, there is no limit. Setting this parameter to 1 will effectively disable keep alive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_requests_per_connection GoogleComputeRegionBackendService#max_requests_per_connection}
        :param max_retries: The maximum number of parallel retries to the backend cluster. Defaults to 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_retries GoogleComputeRegionBackendService#max_retries}
        '''
        value = GoogleComputeRegionBackendServiceCircuitBreakers(
            connect_timeout=connect_timeout,
            max_connections=max_connections,
            max_pending_requests=max_pending_requests,
            max_requests=max_requests,
            max_requests_per_connection=max_requests_per_connection,
            max_retries=max_retries,
        )

        return typing.cast(None, jsii.invoke(self, "putCircuitBreakers", [value]))

    @jsii.member(jsii_name="putConnectionTrackingPolicy")
    def put_connection_tracking_policy(
        self,
        *,
        connection_persistence_on_unhealthy_backends: typing.Optional[builtins.str] = None,
        enable_strong_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        idle_timeout_sec: typing.Optional[jsii.Number] = None,
        tracking_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection_persistence_on_unhealthy_backends: Specifies connection persistence when backends are unhealthy. If set to 'DEFAULT_FOR_PROTOCOL', the existing connections persist on unhealthy backends only for connection-oriented protocols (TCP and SCTP) and only if the Tracking Mode is PER_CONNECTION (default tracking mode) or the Session Affinity is configured for 5-tuple. They do not persist for UDP. If set to 'NEVER_PERSIST', after a backend becomes unhealthy, the existing connections on the unhealthy backend are never persisted on the unhealthy backend. They are always diverted to newly selected healthy backends (unless all backends are unhealthy). If set to 'ALWAYS_PERSIST', existing connections always persist on unhealthy backends regardless of protocol and session affinity. It is generally not recommended to use this mode overriding the default. Default value: "DEFAULT_FOR_PROTOCOL" Possible values: ["DEFAULT_FOR_PROTOCOL", "NEVER_PERSIST", "ALWAYS_PERSIST"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#connection_persistence_on_unhealthy_backends GoogleComputeRegionBackendService#connection_persistence_on_unhealthy_backends}
        :param enable_strong_affinity: Enable Strong Session Affinity for Network Load Balancing. This option is not available publicly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enable_strong_affinity GoogleComputeRegionBackendService#enable_strong_affinity}
        :param idle_timeout_sec: Specifies how long to keep a Connection Tracking entry while there is no matching traffic (in seconds). For L4 ILB the minimum(default) is 10 minutes and maximum is 16 hours. For NLB the minimum(default) is 60 seconds and the maximum is 16 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#idle_timeout_sec GoogleComputeRegionBackendService#idle_timeout_sec}
        :param tracking_mode: Specifies the key used for connection tracking. There are two options: 'PER_CONNECTION': The Connection Tracking is performed as per the Connection Key (default Hash Method) for the specific protocol. 'PER_SESSION': The Connection Tracking is performed as per the configured Session Affinity. It matches the configured Session Affinity. Default value: "PER_CONNECTION" Possible values: ["PER_CONNECTION", "PER_SESSION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#tracking_mode GoogleComputeRegionBackendService#tracking_mode}
        '''
        value = GoogleComputeRegionBackendServiceConnectionTrackingPolicy(
            connection_persistence_on_unhealthy_backends=connection_persistence_on_unhealthy_backends,
            enable_strong_affinity=enable_strong_affinity,
            idle_timeout_sec=idle_timeout_sec,
            tracking_mode=tracking_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putConnectionTrackingPolicy", [value]))

    @jsii.member(jsii_name="putConsistentHash")
    def put_consistent_hash(
        self,
        *,
        http_cookie: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceConsistentHashHttpCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        http_header_name: typing.Optional[builtins.str] = None,
        minimum_ring_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_cookie: http_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#http_cookie GoogleComputeRegionBackendService#http_cookie}
        :param http_header_name: The hash based on the value of the specified header field. This field is applicable if the sessionAffinity is set to HEADER_FIELD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#http_header_name GoogleComputeRegionBackendService#http_header_name}
        :param minimum_ring_size: The minimum number of virtual nodes to use for the hash ring. Larger ring sizes result in more granular load distributions. If the number of hosts in the load balancing pool is larger than the ring size, each host will be assigned a single virtual node. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#minimum_ring_size GoogleComputeRegionBackendService#minimum_ring_size}
        '''
        value = GoogleComputeRegionBackendServiceConsistentHash(
            http_cookie=http_cookie,
            http_header_name=http_header_name,
            minimum_ring_size=minimum_ring_size,
        )

        return typing.cast(None, jsii.invoke(self, "putConsistentHash", [value]))

    @jsii.member(jsii_name="putCustomMetrics")
    def put_custom_metrics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionBackendServiceCustomMetrics", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47794b7f71f90a95bd2b1a5a7905a7ff7a3f2822d3fddea3149403bb9c68dfaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomMetrics", [value]))

    @jsii.member(jsii_name="putDynamicForwarding")
    def put_dynamic_forwarding(
        self,
        *,
        ip_port_selection: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ip_port_selection: ip_port_selection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ip_port_selection GoogleComputeRegionBackendService#ip_port_selection}
        '''
        value = GoogleComputeRegionBackendServiceDynamicForwarding(
            ip_port_selection=ip_port_selection
        )

        return typing.cast(None, jsii.invoke(self, "putDynamicForwarding", [value]))

    @jsii.member(jsii_name="putFailoverPolicy")
    def put_failover_policy(
        self,
        *,
        disable_connection_drain_on_failover: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_traffic_if_unhealthy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failover_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disable_connection_drain_on_failover: On failover or failback, this field indicates whether connection drain will be honored. Setting this to true has the following effect: connections to the old active pool are not drained. Connections to the new active pool use the timeout of 10 min (currently fixed). Setting to false has the following effect: both old and new connections will have a drain timeout of 10 min. This can be set to true only if the protocol is TCP. The default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#disable_connection_drain_on_failover GoogleComputeRegionBackendService#disable_connection_drain_on_failover}
        :param drop_traffic_if_unhealthy: This option is used only when no healthy VMs are detected in the primary and backup instance groups. When set to true, traffic is dropped. When set to false, new connections are sent across all VMs in the primary group. The default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#drop_traffic_if_unhealthy GoogleComputeRegionBackendService#drop_traffic_if_unhealthy}
        :param failover_ratio: The value of the field must be in [0, 1]. If the ratio of the healthy VMs in the primary backend is at or below this number, traffic arriving at the load-balanced IP will be directed to the failover backend. In case where 'failoverRatio' is not set or all the VMs in the backup backend are unhealthy, the traffic will be directed back to the primary backend in the "force" mode, where traffic will be spread to the healthy VMs with the best effort, or to all VMs when no VM is healthy. This field is only used with l4 load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#failover_ratio GoogleComputeRegionBackendService#failover_ratio}
        '''
        value = GoogleComputeRegionBackendServiceFailoverPolicy(
            disable_connection_drain_on_failover=disable_connection_drain_on_failover,
            drop_traffic_if_unhealthy=drop_traffic_if_unhealthy,
            failover_ratio=failover_ratio,
        )

        return typing.cast(None, jsii.invoke(self, "putFailoverPolicy", [value]))

    @jsii.member(jsii_name="putIap")
    def put_iap(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        oauth2_client_id: typing.Optional[builtins.str] = None,
        oauth2_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether the serving infrastructure will authenticate and authorize all incoming requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enabled GoogleComputeRegionBackendService#enabled}
        :param oauth2_client_id: OAuth2 Client ID for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#oauth2_client_id GoogleComputeRegionBackendService#oauth2_client_id}
        :param oauth2_client_secret: OAuth2 Client Secret for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#oauth2_client_secret GoogleComputeRegionBackendService#oauth2_client_secret}
        '''
        value = GoogleComputeRegionBackendServiceIap(
            enabled=enabled,
            oauth2_client_id=oauth2_client_id,
            oauth2_client_secret=oauth2_client_secret,
        )

        return typing.cast(None, jsii.invoke(self, "putIap", [value]))

    @jsii.member(jsii_name="putLogConfig")
    def put_log_config(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        optional_mode: typing.Optional[builtins.str] = None,
        sample_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable: Whether to enable logging for the load balancer traffic served by this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enable GoogleComputeRegionBackendService#enable}
        :param optional_fields: Specifies the fields to include in logging. This field can only be specified if logging is enabled for this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#optional_fields GoogleComputeRegionBackendService#optional_fields}
        :param optional_mode: Specifies the optional logging mode for the load balancer traffic. Supported values: INCLUDE_ALL_OPTIONAL, EXCLUDE_ALL_OPTIONAL, CUSTOM. Possible values: ["INCLUDE_ALL_OPTIONAL", "EXCLUDE_ALL_OPTIONAL", "CUSTOM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#optional_mode GoogleComputeRegionBackendService#optional_mode}
        :param sample_rate: This field can only be specified if logging is enabled for this backend service. The value of the field must be in [0, 1]. This configures the sampling rate of requests to the load balancer where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#sample_rate GoogleComputeRegionBackendService#sample_rate}
        '''
        value = GoogleComputeRegionBackendServiceLogConfig(
            enable=enable,
            optional_fields=optional_fields,
            optional_mode=optional_mode,
            sample_rate=sample_rate,
        )

        return typing.cast(None, jsii.invoke(self, "putLogConfig", [value]))

    @jsii.member(jsii_name="putOutlierDetection")
    def put_outlier_detection(
        self,
        *,
        base_ejection_time: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime", typing.Dict[builtins.str, typing.Any]]] = None,
        consecutive_errors: typing.Optional[jsii.Number] = None,
        consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_errors: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_success_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceOutlierDetectionInterval", typing.Dict[builtins.str, typing.Any]]] = None,
        max_ejection_percent: typing.Optional[jsii.Number] = None,
        success_rate_minimum_hosts: typing.Optional[jsii.Number] = None,
        success_rate_request_volume: typing.Optional[jsii.Number] = None,
        success_rate_stdev_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param base_ejection_time: base_ejection_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#base_ejection_time GoogleComputeRegionBackendService#base_ejection_time}
        :param consecutive_errors: Number of errors before a host is ejected from the connection pool. When the backend host is accessed over HTTP, a 5xx return code qualifies as an error. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#consecutive_errors GoogleComputeRegionBackendService#consecutive_errors}
        :param consecutive_gateway_failure: The number of consecutive gateway failures (502, 503, 504 status or connection errors that are mapped to one of those status codes) before a consecutive gateway failure ejection occurs. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#consecutive_gateway_failure GoogleComputeRegionBackendService#consecutive_gateway_failure}
        :param enforcing_consecutive_errors: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive 5xx. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enforcing_consecutive_errors GoogleComputeRegionBackendService#enforcing_consecutive_errors}
        :param enforcing_consecutive_gateway_failure: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive gateway failures. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enforcing_consecutive_gateway_failure GoogleComputeRegionBackendService#enforcing_consecutive_gateway_failure}
        :param enforcing_success_rate: The percentage chance that a host will be actually ejected when an outlier status is detected through success rate statistics. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enforcing_success_rate GoogleComputeRegionBackendService#enforcing_success_rate}
        :param interval: interval block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#interval GoogleComputeRegionBackendService#interval}
        :param max_ejection_percent: Maximum percentage of hosts in the load balancing pool for the backend service that can be ejected. Defaults to 10%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_ejection_percent GoogleComputeRegionBackendService#max_ejection_percent}
        :param success_rate_minimum_hosts: The number of hosts in a cluster that must have enough request volume to detect success rate outliers. If the number of hosts is less than this setting, outlier detection via success rate statistics is not performed for any host in the cluster. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#success_rate_minimum_hosts GoogleComputeRegionBackendService#success_rate_minimum_hosts}
        :param success_rate_request_volume: The minimum number of total requests that must be collected in one interval (as defined by the interval duration above) to include this host in success rate based outlier detection. If the volume is lower than this setting, outlier detection via success rate statistics is not performed for that host. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#success_rate_request_volume GoogleComputeRegionBackendService#success_rate_request_volume}
        :param success_rate_stdev_factor: This factor is used to determine the ejection threshold for success rate outlier ejection. The ejection threshold is the difference between the mean success rate, and the product of this factor and the standard deviation of the mean success rate: mean - (stdev * success_rate_stdev_factor). This factor is divided by a thousand to get a double. That is, if the desired factor is 1.9, the runtime value should be 1900. Defaults to 1900. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#success_rate_stdev_factor GoogleComputeRegionBackendService#success_rate_stdev_factor}
        '''
        value = GoogleComputeRegionBackendServiceOutlierDetection(
            base_ejection_time=base_ejection_time,
            consecutive_errors=consecutive_errors,
            consecutive_gateway_failure=consecutive_gateway_failure,
            enforcing_consecutive_errors=enforcing_consecutive_errors,
            enforcing_consecutive_gateway_failure=enforcing_consecutive_gateway_failure,
            enforcing_success_rate=enforcing_success_rate,
            interval=interval,
            max_ejection_percent=max_ejection_percent,
            success_rate_minimum_hosts=success_rate_minimum_hosts,
            success_rate_request_volume=success_rate_request_volume,
            success_rate_stdev_factor=success_rate_stdev_factor,
        )

        return typing.cast(None, jsii.invoke(self, "putOutlierDetection", [value]))

    @jsii.member(jsii_name="putStrongSessionAffinityCookie")
    def put_strong_session_affinity_cookie(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#name GoogleComputeRegionBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#path GoogleComputeRegionBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ttl GoogleComputeRegionBackendService#ttl}
        '''
        value = GoogleComputeRegionBackendServiceStrongSessionAffinityCookie(
            name=name, path=path, ttl=ttl
        )

        return typing.cast(None, jsii.invoke(self, "putStrongSessionAffinityCookie", [value]))

    @jsii.member(jsii_name="putSubsetting")
    def put_subsetting(
        self,
        *,
        policy: builtins.str,
        subset_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param policy: The algorithm used for subsetting. Possible values: ["CONSISTENT_HASH_SUBSETTING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#policy GoogleComputeRegionBackendService#policy}
        :param subset_size: The number of backends per backend group assigned to each proxy instance or each service mesh client. An input parameter to the CONSISTENT_HASH_SUBSETTING algorithm. Can only be set if policy is set to CONSISTENT_HASH_SUBSETTING. Can only be set if load balancing scheme is INTERNAL_MANAGED or INTERNAL_SELF_MANAGED. subsetSize is optional for Internal HTTP(S) load balancing and required for Traffic Director. If you do not provide this value, Cloud Load Balancing will calculate it dynamically to optimize the number of proxies/clients visible to each backend and vice versa. Must be greater than 0. If subsetSize is larger than the number of backends/endpoints, then subsetting is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#subset_size GoogleComputeRegionBackendService#subset_size}
        '''
        value = GoogleComputeRegionBackendServiceSubsetting(
            policy=policy, subset_size=subset_size
        )

        return typing.cast(None, jsii.invoke(self, "putSubsetting", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#create GoogleComputeRegionBackendService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#delete GoogleComputeRegionBackendService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#update GoogleComputeRegionBackendService#update}.
        '''
        value = GoogleComputeRegionBackendServiceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAffinityCookieTtlSec")
    def reset_affinity_cookie_ttl_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAffinityCookieTtlSec", []))

    @jsii.member(jsii_name="resetBackend")
    def reset_backend(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackend", []))

    @jsii.member(jsii_name="resetCdnPolicy")
    def reset_cdn_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCdnPolicy", []))

    @jsii.member(jsii_name="resetCircuitBreakers")
    def reset_circuit_breakers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCircuitBreakers", []))

    @jsii.member(jsii_name="resetConnectionDrainingTimeoutSec")
    def reset_connection_draining_timeout_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionDrainingTimeoutSec", []))

    @jsii.member(jsii_name="resetConnectionTrackingPolicy")
    def reset_connection_tracking_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionTrackingPolicy", []))

    @jsii.member(jsii_name="resetConsistentHash")
    def reset_consistent_hash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsistentHash", []))

    @jsii.member(jsii_name="resetCustomMetrics")
    def reset_custom_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomMetrics", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDynamicForwarding")
    def reset_dynamic_forwarding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicForwarding", []))

    @jsii.member(jsii_name="resetEnableCdn")
    def reset_enable_cdn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableCdn", []))

    @jsii.member(jsii_name="resetFailoverPolicy")
    def reset_failover_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailoverPolicy", []))

    @jsii.member(jsii_name="resetHealthChecks")
    def reset_health_checks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthChecks", []))

    @jsii.member(jsii_name="resetIap")
    def reset_iap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIap", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpAddressSelectionPolicy")
    def reset_ip_address_selection_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddressSelectionPolicy", []))

    @jsii.member(jsii_name="resetLoadBalancingScheme")
    def reset_load_balancing_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancingScheme", []))

    @jsii.member(jsii_name="resetLocalityLbPolicy")
    def reset_locality_lb_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalityLbPolicy", []))

    @jsii.member(jsii_name="resetLogConfig")
    def reset_log_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogConfig", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetOutlierDetection")
    def reset_outlier_detection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutlierDetection", []))

    @jsii.member(jsii_name="resetPortName")
    def reset_port_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortName", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSecurityPolicy")
    def reset_security_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityPolicy", []))

    @jsii.member(jsii_name="resetSessionAffinity")
    def reset_session_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinity", []))

    @jsii.member(jsii_name="resetStrongSessionAffinityCookie")
    def reset_strong_session_affinity_cookie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrongSessionAffinityCookie", []))

    @jsii.member(jsii_name="resetSubsetting")
    def reset_subsetting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubsetting", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimeoutSec")
    def reset_timeout_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSec", []))

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
    @jsii.member(jsii_name="backend")
    def backend(self) -> "GoogleComputeRegionBackendServiceBackendList":
        return typing.cast("GoogleComputeRegionBackendServiceBackendList", jsii.get(self, "backend"))

    @builtins.property
    @jsii.member(jsii_name="cdnPolicy")
    def cdn_policy(self) -> "GoogleComputeRegionBackendServiceCdnPolicyOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceCdnPolicyOutputReference", jsii.get(self, "cdnPolicy"))

    @builtins.property
    @jsii.member(jsii_name="circuitBreakers")
    def circuit_breakers(
        self,
    ) -> "GoogleComputeRegionBackendServiceCircuitBreakersOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceCircuitBreakersOutputReference", jsii.get(self, "circuitBreakers"))

    @builtins.property
    @jsii.member(jsii_name="connectionTrackingPolicy")
    def connection_tracking_policy(
        self,
    ) -> "GoogleComputeRegionBackendServiceConnectionTrackingPolicyOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceConnectionTrackingPolicyOutputReference", jsii.get(self, "connectionTrackingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="consistentHash")
    def consistent_hash(
        self,
    ) -> "GoogleComputeRegionBackendServiceConsistentHashOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceConsistentHashOutputReference", jsii.get(self, "consistentHash"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="customMetrics")
    def custom_metrics(self) -> "GoogleComputeRegionBackendServiceCustomMetricsList":
        return typing.cast("GoogleComputeRegionBackendServiceCustomMetricsList", jsii.get(self, "customMetrics"))

    @builtins.property
    @jsii.member(jsii_name="dynamicForwarding")
    def dynamic_forwarding(
        self,
    ) -> "GoogleComputeRegionBackendServiceDynamicForwardingOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceDynamicForwardingOutputReference", jsii.get(self, "dynamicForwarding"))

    @builtins.property
    @jsii.member(jsii_name="failoverPolicy")
    def failover_policy(
        self,
    ) -> "GoogleComputeRegionBackendServiceFailoverPolicyOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceFailoverPolicyOutputReference", jsii.get(self, "failoverPolicy"))

    @builtins.property
    @jsii.member(jsii_name="fingerprint")
    def fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fingerprint"))

    @builtins.property
    @jsii.member(jsii_name="generatedId")
    def generated_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generatedId"))

    @builtins.property
    @jsii.member(jsii_name="iap")
    def iap(self) -> "GoogleComputeRegionBackendServiceIapOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceIapOutputReference", jsii.get(self, "iap"))

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(self) -> "GoogleComputeRegionBackendServiceLogConfigOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="outlierDetection")
    def outlier_detection(
        self,
    ) -> "GoogleComputeRegionBackendServiceOutlierDetectionOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceOutlierDetectionOutputReference", jsii.get(self, "outlierDetection"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="strongSessionAffinityCookie")
    def strong_session_affinity_cookie(
        self,
    ) -> "GoogleComputeRegionBackendServiceStrongSessionAffinityCookieOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceStrongSessionAffinityCookieOutputReference", jsii.get(self, "strongSessionAffinityCookie"))

    @builtins.property
    @jsii.member(jsii_name="subsetting")
    def subsetting(
        self,
    ) -> "GoogleComputeRegionBackendServiceSubsettingOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceSubsettingOutputReference", jsii.get(self, "subsetting"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputeRegionBackendServiceTimeoutsOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="affinityCookieTtlSecInput")
    def affinity_cookie_ttl_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "affinityCookieTtlSecInput"))

    @builtins.property
    @jsii.member(jsii_name="backendInput")
    def backend_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionBackendServiceBackend"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionBackendServiceBackend"]]], jsii.get(self, "backendInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnPolicyInput")
    def cdn_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceCdnPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceCdnPolicy"], jsii.get(self, "cdnPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="circuitBreakersInput")
    def circuit_breakers_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceCircuitBreakers"]:
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceCircuitBreakers"], jsii.get(self, "circuitBreakersInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionDrainingTimeoutSecInput")
    def connection_draining_timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectionDrainingTimeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionTrackingPolicyInput")
    def connection_tracking_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceConnectionTrackingPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceConnectionTrackingPolicy"], jsii.get(self, "connectionTrackingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="consistentHashInput")
    def consistent_hash_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceConsistentHash"]:
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceConsistentHash"], jsii.get(self, "consistentHashInput"))

    @builtins.property
    @jsii.member(jsii_name="customMetricsInput")
    def custom_metrics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionBackendServiceCustomMetrics"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionBackendServiceCustomMetrics"]]], jsii.get(self, "customMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicForwardingInput")
    def dynamic_forwarding_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceDynamicForwarding"]:
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceDynamicForwarding"], jsii.get(self, "dynamicForwardingInput"))

    @builtins.property
    @jsii.member(jsii_name="enableCdnInput")
    def enable_cdn_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableCdnInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverPolicyInput")
    def failover_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceFailoverPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceFailoverPolicy"], jsii.get(self, "failoverPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="healthChecksInput")
    def health_checks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "healthChecksInput"))

    @builtins.property
    @jsii.member(jsii_name="iapInput")
    def iap_input(self) -> typing.Optional["GoogleComputeRegionBackendServiceIap"]:
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceIap"], jsii.get(self, "iapInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressSelectionPolicyInput")
    def ip_address_selection_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressSelectionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingSchemeInput")
    def load_balancing_scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancingSchemeInput"))

    @builtins.property
    @jsii.member(jsii_name="localityLbPolicyInput")
    def locality_lb_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localityLbPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigInput")
    def log_config_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceLogConfig"]:
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceLogConfig"], jsii.get(self, "logConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="outlierDetectionInput")
    def outlier_detection_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceOutlierDetection"]:
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceOutlierDetection"], jsii.get(self, "outlierDetectionInput"))

    @builtins.property
    @jsii.member(jsii_name="portNameInput")
    def port_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portNameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="securityPolicyInput")
    def security_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityInput")
    def session_affinity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="strongSessionAffinityCookieInput")
    def strong_session_affinity_cookie_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceStrongSessionAffinityCookie"]:
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceStrongSessionAffinityCookie"], jsii.get(self, "strongSessionAffinityCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="subsettingInput")
    def subsetting_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceSubsetting"]:
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceSubsetting"], jsii.get(self, "subsettingInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecInput")
    def timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRegionBackendServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRegionBackendServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="affinityCookieTtlSec")
    def affinity_cookie_ttl_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "affinityCookieTtlSec"))

    @affinity_cookie_ttl_sec.setter
    def affinity_cookie_ttl_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388e4f1d56611ac154e1c7425c0c738ad01d1c00544763cb3f6e9376ea7224c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "affinityCookieTtlSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionDrainingTimeoutSec")
    def connection_draining_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectionDrainingTimeoutSec"))

    @connection_draining_timeout_sec.setter
    def connection_draining_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48662c52255952b43c61332cb7b6d44dcaaf6759ddc46cb7a09e10c393edf0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionDrainingTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e141224b6561a124303b8e2dfee4cfd2cdf5bcda5bb788e5cb2afcf07292336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableCdn")
    def enable_cdn(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableCdn"))

    @enable_cdn.setter
    def enable_cdn(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8968d9462a272a1e5dcfb9fd3013b9cc26668ef92c0f2af498ebced48d7ce56c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableCdn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthChecks")
    def health_checks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "healthChecks"))

    @health_checks.setter
    def health_checks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46ee6a38fd114edfe14be1319870f7f7829fde7f6a97f76e84c33114075339f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthChecks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357dfd8d7d9bc864cbd573e5d58cea96bef4556f94f151617fc24ba425e1ed02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressSelectionPolicy")
    def ip_address_selection_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressSelectionPolicy"))

    @ip_address_selection_policy.setter
    def ip_address_selection_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186f8f8b6a917569717678160e2db744d16006e66b453e0e99f3f39b11b7b266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressSelectionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0eef5df96e695b2207167bbeeeb916b1caf61d5afeee9d4f85b2777686eafa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localityLbPolicy")
    def locality_lb_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localityLbPolicy"))

    @locality_lb_policy.setter
    def locality_lb_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71f5646e86567e6183370a0e75996508e819a388958a7421ee817c4031b343b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localityLbPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21a40d0efd575f844e654199132eb5349356aeb72dfd401c4402e7289743e855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93099defbe4fb2c7d00f7b7d45c9e9665880c3b98af687305d005a66e25da868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c6d7e243062346243f15f5f08d1fc5cd24657f2cdf70e2846e57af097502e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722ebe75954967e6747c3482c8d8859f779e80d8030e48f75e26fca273ddebae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0727e5b5b4df740f568445e05cb7944a09e1b7a96ed20fdabc1804789355c9c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961e4ec1d692af08c4da5337cef5d6e6083eda60e167dc10683a9aabaa8481da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityPolicy")
    def security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityPolicy"))

    @security_policy.setter
    def security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a92d86ae32cdc68c0850bf5e1b12cf92de4da64c50bd7f70616d19a95db6b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionAffinity")
    def session_affinity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionAffinity"))

    @session_affinity.setter
    def session_affinity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d26374e2f3142759a394000ef0a657689a96446c41ea6f8045283009800c87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSec")
    def timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSec"))

    @timeout_sec.setter
    def timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345b259c60f0d99c137c967ba3f210383a0276314a00d0a544dc5b8d1ca58ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSec", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceBackend",
    jsii_struct_bases=[],
    name_mapping={
        "group": "group",
        "balancing_mode": "balancingMode",
        "capacity_scaler": "capacityScaler",
        "custom_metrics": "customMetrics",
        "description": "description",
        "failover": "failover",
        "max_connections": "maxConnections",
        "max_connections_per_endpoint": "maxConnectionsPerEndpoint",
        "max_connections_per_instance": "maxConnectionsPerInstance",
        "max_rate": "maxRate",
        "max_rate_per_endpoint": "maxRatePerEndpoint",
        "max_rate_per_instance": "maxRatePerInstance",
        "max_utilization": "maxUtilization",
    },
)
class GoogleComputeRegionBackendServiceBackend:
    def __init__(
        self,
        *,
        group: builtins.str,
        balancing_mode: typing.Optional[builtins.str] = None,
        capacity_scaler: typing.Optional[jsii.Number] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionBackendServiceBackendCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        failover: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_connections: typing.Optional[jsii.Number] = None,
        max_connections_per_endpoint: typing.Optional[jsii.Number] = None,
        max_connections_per_instance: typing.Optional[jsii.Number] = None,
        max_rate: typing.Optional[jsii.Number] = None,
        max_rate_per_endpoint: typing.Optional[jsii.Number] = None,
        max_rate_per_instance: typing.Optional[jsii.Number] = None,
        max_utilization: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param group: The fully-qualified URL of an Instance Group or Network Endpoint Group resource. In case of instance group this defines the list of instances that serve traffic. Member virtual machine instances from each instance group must live in the same zone as the instance group itself. No two backends in a backend service are allowed to use same Instance Group resource. For Network Endpoint Groups this defines list of endpoints. All endpoints of Network Endpoint Group must be hosted on instances located in the same zone as the Network Endpoint Group. Backend services cannot mix Instance Group and Network Endpoint Group backends. When the 'load_balancing_scheme' is INTERNAL, only instance groups are supported. Note that you must specify an Instance Group or Network Endpoint Group resource using the fully-qualified URL, rather than a partial URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#group GoogleComputeRegionBackendService#group}
        :param balancing_mode: Specifies the balancing mode for this backend. See the `Backend Services Overview <https://cloud.google.com/load-balancing/docs/backend-service#balancing-mode>`_ for an explanation of load balancing modes. Default value: "UTILIZATION" Possible values: ["UTILIZATION", "RATE", "CONNECTION", "CUSTOM_METRICS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#balancing_mode GoogleComputeRegionBackendService#balancing_mode}
        :param capacity_scaler: A multiplier applied to the group's maximum servicing capacity (based on UTILIZATION, RATE or CONNECTION). ~>**NOTE**: This field cannot be set for INTERNAL region backend services (default loadBalancingScheme), but is required for non-INTERNAL backend service. The total capacity_scaler for all backends must be non-zero. A setting of 0 means the group is completely drained, offering 0% of its available Capacity. Valid range is [0.0,1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#capacity_scaler GoogleComputeRegionBackendService#capacity_scaler}
        :param custom_metrics: custom_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#custom_metrics GoogleComputeRegionBackendService#custom_metrics}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#description GoogleComputeRegionBackendService#description}
        :param failover: This field designates whether this is a failover backend. More than one failover backend can be configured for a given RegionBackendService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#failover GoogleComputeRegionBackendService#failover}
        :param max_connections: The max number of simultaneous connections for the group. Can be used with either CONNECTION or UTILIZATION balancing modes. Cannot be set for INTERNAL backend services. For CONNECTION mode, either maxConnections or one of maxConnectionsPerInstance or maxConnectionsPerEndpoint, as appropriate for group type, must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_connections GoogleComputeRegionBackendService#max_connections}
        :param max_connections_per_endpoint: The max number of simultaneous connections that a single backend network endpoint can handle. Cannot be set for INTERNAL backend services. This is used to calculate the capacity of the group. Can be used in either CONNECTION or UTILIZATION balancing modes. For CONNECTION mode, either maxConnections or maxConnectionsPerEndpoint must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_connections_per_endpoint GoogleComputeRegionBackendService#max_connections_per_endpoint}
        :param max_connections_per_instance: The max number of simultaneous connections that a single backend instance can handle. Cannot be set for INTERNAL backend services. This is used to calculate the capacity of the group. Can be used in either CONNECTION or UTILIZATION balancing modes. For CONNECTION mode, either maxConnections or maxConnectionsPerInstance must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_connections_per_instance GoogleComputeRegionBackendService#max_connections_per_instance}
        :param max_rate: The max requests per second (RPS) of the group. Cannot be set for INTERNAL backend services. Can be used with either RATE or UTILIZATION balancing modes, but required if RATE mode. Either maxRate or one of maxRatePerInstance or maxRatePerEndpoint, as appropriate for group type, must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_rate GoogleComputeRegionBackendService#max_rate}
        :param max_rate_per_endpoint: The max requests per second (RPS) that a single backend network endpoint can handle. This is used to calculate the capacity of the group. Can be used in either balancing mode. For RATE mode, either maxRate or maxRatePerEndpoint must be set. Cannot be set for INTERNAL backend services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_rate_per_endpoint GoogleComputeRegionBackendService#max_rate_per_endpoint}
        :param max_rate_per_instance: The max requests per second (RPS) that a single backend instance can handle. This is used to calculate the capacity of the group. Can be used in either balancing mode. For RATE mode, either maxRate or maxRatePerInstance must be set. Cannot be set for INTERNAL backend services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_rate_per_instance GoogleComputeRegionBackendService#max_rate_per_instance}
        :param max_utilization: Used when balancingMode is UTILIZATION. This ratio defines the CPU utilization target for the group. Valid range is [0.0, 1.0]. Cannot be set for INTERNAL backend services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_utilization GoogleComputeRegionBackendService#max_utilization}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7883e8a00ba9b8e9934b3720f972c96da3837e28c99affde99f14f121de20e99)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument balancing_mode", value=balancing_mode, expected_type=type_hints["balancing_mode"])
            check_type(argname="argument capacity_scaler", value=capacity_scaler, expected_type=type_hints["capacity_scaler"])
            check_type(argname="argument custom_metrics", value=custom_metrics, expected_type=type_hints["custom_metrics"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument failover", value=failover, expected_type=type_hints["failover"])
            check_type(argname="argument max_connections", value=max_connections, expected_type=type_hints["max_connections"])
            check_type(argname="argument max_connections_per_endpoint", value=max_connections_per_endpoint, expected_type=type_hints["max_connections_per_endpoint"])
            check_type(argname="argument max_connections_per_instance", value=max_connections_per_instance, expected_type=type_hints["max_connections_per_instance"])
            check_type(argname="argument max_rate", value=max_rate, expected_type=type_hints["max_rate"])
            check_type(argname="argument max_rate_per_endpoint", value=max_rate_per_endpoint, expected_type=type_hints["max_rate_per_endpoint"])
            check_type(argname="argument max_rate_per_instance", value=max_rate_per_instance, expected_type=type_hints["max_rate_per_instance"])
            check_type(argname="argument max_utilization", value=max_utilization, expected_type=type_hints["max_utilization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group": group,
        }
        if balancing_mode is not None:
            self._values["balancing_mode"] = balancing_mode
        if capacity_scaler is not None:
            self._values["capacity_scaler"] = capacity_scaler
        if custom_metrics is not None:
            self._values["custom_metrics"] = custom_metrics
        if description is not None:
            self._values["description"] = description
        if failover is not None:
            self._values["failover"] = failover
        if max_connections is not None:
            self._values["max_connections"] = max_connections
        if max_connections_per_endpoint is not None:
            self._values["max_connections_per_endpoint"] = max_connections_per_endpoint
        if max_connections_per_instance is not None:
            self._values["max_connections_per_instance"] = max_connections_per_instance
        if max_rate is not None:
            self._values["max_rate"] = max_rate
        if max_rate_per_endpoint is not None:
            self._values["max_rate_per_endpoint"] = max_rate_per_endpoint
        if max_rate_per_instance is not None:
            self._values["max_rate_per_instance"] = max_rate_per_instance
        if max_utilization is not None:
            self._values["max_utilization"] = max_utilization

    @builtins.property
    def group(self) -> builtins.str:
        '''The fully-qualified URL of an Instance Group or Network Endpoint Group resource.

        In case of instance group this defines the list
        of instances that serve traffic. Member virtual machine
        instances from each instance group must live in the same zone as
        the instance group itself. No two backends in a backend service
        are allowed to use same Instance Group resource.

        For Network Endpoint Groups this defines list of endpoints. All
        endpoints of Network Endpoint Group must be hosted on instances
        located in the same zone as the Network Endpoint Group.

        Backend services cannot mix Instance Group and
        Network Endpoint Group backends.

        When the 'load_balancing_scheme' is INTERNAL, only instance groups
        are supported.

        Note that you must specify an Instance Group or Network Endpoint
        Group resource using the fully-qualified URL, rather than a
        partial URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#group GoogleComputeRegionBackendService#group}
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def balancing_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the balancing mode for this backend.

        See the `Backend Services Overview <https://cloud.google.com/load-balancing/docs/backend-service#balancing-mode>`_
        for an explanation of load balancing modes. Default value: "UTILIZATION" Possible values: ["UTILIZATION", "RATE", "CONNECTION", "CUSTOM_METRICS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#balancing_mode GoogleComputeRegionBackendService#balancing_mode}
        '''
        result = self._values.get("balancing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capacity_scaler(self) -> typing.Optional[jsii.Number]:
        '''A multiplier applied to the group's maximum servicing capacity (based on UTILIZATION, RATE or CONNECTION).

        ~>**NOTE**: This field cannot be set for
        INTERNAL region backend services (default loadBalancingScheme),
        but is required for non-INTERNAL backend service. The total
        capacity_scaler for all backends must be non-zero.

        A setting of 0 means the group is completely drained, offering
        0% of its available Capacity. Valid range is [0.0,1.0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#capacity_scaler GoogleComputeRegionBackendService#capacity_scaler}
        '''
        result = self._values.get("capacity_scaler")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_metrics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionBackendServiceBackendCustomMetrics"]]]:
        '''custom_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#custom_metrics GoogleComputeRegionBackendService#custom_metrics}
        '''
        result = self._values.get("custom_metrics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionBackendServiceBackendCustomMetrics"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#description GoogleComputeRegionBackendService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failover(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This field designates whether this is a failover backend.

        More
        than one failover backend can be configured for a given RegionBackendService.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#failover GoogleComputeRegionBackendService#failover}
        '''
        result = self._values.get("failover")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_connections(self) -> typing.Optional[jsii.Number]:
        '''The max number of simultaneous connections for the group.

        Can
        be used with either CONNECTION or UTILIZATION balancing modes.
        Cannot be set for INTERNAL backend services.

        For CONNECTION mode, either maxConnections or one
        of maxConnectionsPerInstance or maxConnectionsPerEndpoint,
        as appropriate for group type, must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_connections GoogleComputeRegionBackendService#max_connections}
        '''
        result = self._values.get("max_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_connections_per_endpoint(self) -> typing.Optional[jsii.Number]:
        '''The max number of simultaneous connections that a single backend network endpoint can handle. Cannot be set for INTERNAL backend services.

        This is used to calculate the capacity of the group. Can be
        used in either CONNECTION or UTILIZATION balancing modes. For
        CONNECTION mode, either maxConnections or
        maxConnectionsPerEndpoint must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_connections_per_endpoint GoogleComputeRegionBackendService#max_connections_per_endpoint}
        '''
        result = self._values.get("max_connections_per_endpoint")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_connections_per_instance(self) -> typing.Optional[jsii.Number]:
        '''The max number of simultaneous connections that a single backend instance can handle. Cannot be set for INTERNAL backend services.

        This is used to calculate the capacity of the group.
        Can be used in either CONNECTION or UTILIZATION balancing modes.
        For CONNECTION mode, either maxConnections or
        maxConnectionsPerInstance must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_connections_per_instance GoogleComputeRegionBackendService#max_connections_per_instance}
        '''
        result = self._values.get("max_connections_per_instance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_rate(self) -> typing.Optional[jsii.Number]:
        '''The max requests per second (RPS) of the group. Cannot be set for INTERNAL backend services.

        Can be used with either RATE or UTILIZATION balancing modes,
        but required if RATE mode. Either maxRate or one
        of maxRatePerInstance or maxRatePerEndpoint, as appropriate for
        group type, must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_rate GoogleComputeRegionBackendService#max_rate}
        '''
        result = self._values.get("max_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_rate_per_endpoint(self) -> typing.Optional[jsii.Number]:
        '''The max requests per second (RPS) that a single backend network endpoint can handle.

        This is used to calculate the capacity of
        the group. Can be used in either balancing mode. For RATE mode,
        either maxRate or maxRatePerEndpoint must be set. Cannot be set
        for INTERNAL backend services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_rate_per_endpoint GoogleComputeRegionBackendService#max_rate_per_endpoint}
        '''
        result = self._values.get("max_rate_per_endpoint")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_rate_per_instance(self) -> typing.Optional[jsii.Number]:
        '''The max requests per second (RPS) that a single backend instance can handle.

        This is used to calculate the capacity of
        the group. Can be used in either balancing mode. For RATE mode,
        either maxRate or maxRatePerInstance must be set. Cannot be set
        for INTERNAL backend services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_rate_per_instance GoogleComputeRegionBackendService#max_rate_per_instance}
        '''
        result = self._values.get("max_rate_per_instance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_utilization(self) -> typing.Optional[jsii.Number]:
        '''Used when balancingMode is UTILIZATION.

        This ratio defines the
        CPU utilization target for the group. Valid range is [0.0, 1.0].
        Cannot be set for INTERNAL backend services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_utilization GoogleComputeRegionBackendService#max_utilization}
        '''
        result = self._values.get("max_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceBackend(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceBackendCustomMetrics",
    jsii_struct_bases=[],
    name_mapping={
        "dry_run": "dryRun",
        "name": "name",
        "max_utilization": "maxUtilization",
    },
)
class GoogleComputeRegionBackendServiceBackendCustomMetrics:
    def __init__(
        self,
        *,
        dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        max_utilization: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param dry_run: If true, the metric data is collected and reported to Cloud Monitoring, but is not used for load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#dry_run GoogleComputeRegionBackendService#dry_run}
        :param name: Name of a custom utilization signal. The name must be 1-64 characters long and match the regular expression `a-z <%5B-_.a-z0-9%5D*%5Ba-z0-9%5D>`_? which means the first character must be a lowercase letter, and all following characters must be a dash, period, underscore, lowercase letter, or digit, except the last character, which cannot be a dash, period, or underscore. For usage guidelines, see Custom Metrics balancing mode. This field can only be used for a global or regional backend service with the loadBalancingScheme set to EXTERNAL_MANAGED, INTERNAL_MANAGED INTERNAL_SELF_MANAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#name GoogleComputeRegionBackendService#name}
        :param max_utilization: Optional parameter to define a target utilization for the Custom Metrics balancing mode. The valid range is [0.0, 1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_utilization GoogleComputeRegionBackendService#max_utilization}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f0245e026398768534fd75f8874407ca4b9791db825e0d63c9147e51e1b6d2)
            check_type(argname="argument dry_run", value=dry_run, expected_type=type_hints["dry_run"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument max_utilization", value=max_utilization, expected_type=type_hints["max_utilization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dry_run": dry_run,
            "name": name,
        }
        if max_utilization is not None:
            self._values["max_utilization"] = max_utilization

    @builtins.property
    def dry_run(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, the metric data is collected and reported to Cloud Monitoring, but is not used for load balancing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#dry_run GoogleComputeRegionBackendService#dry_run}
        '''
        result = self._values.get("dry_run")
        assert result is not None, "Required property 'dry_run' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of a custom utilization signal.

        The name must be 1-64 characters
        long and match the regular expression `a-z <%5B-_.a-z0-9%5D*%5Ba-z0-9%5D>`_? which
        means the first character must be a lowercase letter, and all following
        characters must be a dash, period, underscore, lowercase letter, or
        digit, except the last character, which cannot be a dash, period, or
        underscore. For usage guidelines, see Custom Metrics balancing mode. This
        field can only be used for a global or regional backend service with the
        loadBalancingScheme set to EXTERNAL_MANAGED,
        INTERNAL_MANAGED INTERNAL_SELF_MANAGED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#name GoogleComputeRegionBackendService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_utilization(self) -> typing.Optional[jsii.Number]:
        '''Optional parameter to define a target utilization for the Custom Metrics balancing mode. The valid range is [0.0, 1.0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_utilization GoogleComputeRegionBackendService#max_utilization}
        '''
        result = self._values.get("max_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceBackendCustomMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceBackendCustomMetricsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceBackendCustomMetricsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__490bedba664fb071d857e0874d6e428b67e69fb1c6f6dbaa4afabeabfca58dd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionBackendServiceBackendCustomMetricsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__232a22623fb10e115acccdbd3d39ed75cc0793d25a406450475ac3a3105f24e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionBackendServiceBackendCustomMetricsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cda44d944d962ec70224e77ec4c1bd2cc5d2db13a4aa03bf8ea4fe1d870820e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a2f50baa9aabc8c416ee60d817d611784752b119214653814a14fb747635ae6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03d15ac777d7bb9d8ee99beba759ab9bba0dcc86704da015e2d1e21c1b730156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceBackendCustomMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceBackendCustomMetrics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceBackendCustomMetrics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001e800e43cfb7bb831fe8f17a9e7276a948a20e324101a758b247b12ec243ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionBackendServiceBackendCustomMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceBackendCustomMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da0c3bc08cfa587893a49993c73091c87eaf7cb3cedef638cec986c7085b51dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMaxUtilization")
    def reset_max_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUtilization", []))

    @builtins.property
    @jsii.member(jsii_name="dryRunInput")
    def dry_run_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dryRunInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUtilizationInput")
    def max_utilization_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="dryRun")
    def dry_run(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dryRun"))

    @dry_run.setter
    def dry_run(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be5f8b178ad0008e771a9212cb5fdeab98f513c6bed5ede93f1d032b4ef668ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dryRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUtilization")
    def max_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUtilization"))

    @max_utilization.setter
    def max_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bda4eb6b234b781f29bc658466712c7bbfe229398d297674a80baf13f2490d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c10795f8b5c16f8b433bdacea9de6d5a035a1a20e498a2633886caa5db23554c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceBackendCustomMetrics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceBackendCustomMetrics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceBackendCustomMetrics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d27a354dc168edcbc5985d8d08273277f9132d18381e1f410687fd51fd151097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionBackendServiceBackendList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceBackendList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__468ea21e84df6580c250c1335e54bf9cdccae8d0499fedf1b8cc1f16a74e5671)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionBackendServiceBackendOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b7ddc9b8e041b35f9dbd440e2d55a3cc42b3db1b1b9daa8ced091585884df7d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionBackendServiceBackendOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398322e743f02440c0ad9269e4b93a4f33d33aa8f6a97fcad8d3de1b1f0bac6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__886c75e97c6613284d0bd2bd86c0ce25342c9b5aff2c68dfba44a4bf31c89a48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12830c235234a43f1a36ef9590a773bde1591737e4743b7237fe815754e87824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceBackend]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceBackend]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceBackend]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__427ed5df5c2038e7c054e2c336d47d57dfe1ac0d30bd1aeba735b6dfe6cb6482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionBackendServiceBackendOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceBackendOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a792586768b98a88435b4bf7427b7250be7dac3990207fad28059cdca265c818)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomMetrics")
    def put_custom_metrics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionBackendServiceBackendCustomMetrics, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c878eadeb91f3366a85725a05b03914389361e5657e18e0f064fa0a26b25055e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomMetrics", [value]))

    @jsii.member(jsii_name="resetBalancingMode")
    def reset_balancing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBalancingMode", []))

    @jsii.member(jsii_name="resetCapacityScaler")
    def reset_capacity_scaler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacityScaler", []))

    @jsii.member(jsii_name="resetCustomMetrics")
    def reset_custom_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomMetrics", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFailover")
    def reset_failover(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailover", []))

    @jsii.member(jsii_name="resetMaxConnections")
    def reset_max_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnections", []))

    @jsii.member(jsii_name="resetMaxConnectionsPerEndpoint")
    def reset_max_connections_per_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnectionsPerEndpoint", []))

    @jsii.member(jsii_name="resetMaxConnectionsPerInstance")
    def reset_max_connections_per_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnectionsPerInstance", []))

    @jsii.member(jsii_name="resetMaxRate")
    def reset_max_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRate", []))

    @jsii.member(jsii_name="resetMaxRatePerEndpoint")
    def reset_max_rate_per_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRatePerEndpoint", []))

    @jsii.member(jsii_name="resetMaxRatePerInstance")
    def reset_max_rate_per_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRatePerInstance", []))

    @jsii.member(jsii_name="resetMaxUtilization")
    def reset_max_utilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUtilization", []))

    @builtins.property
    @jsii.member(jsii_name="customMetrics")
    def custom_metrics(
        self,
    ) -> GoogleComputeRegionBackendServiceBackendCustomMetricsList:
        return typing.cast(GoogleComputeRegionBackendServiceBackendCustomMetricsList, jsii.get(self, "customMetrics"))

    @builtins.property
    @jsii.member(jsii_name="balancingModeInput")
    def balancing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "balancingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityScalerInput")
    def capacity_scaler_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "capacityScalerInput"))

    @builtins.property
    @jsii.member(jsii_name="customMetricsInput")
    def custom_metrics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceBackendCustomMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceBackendCustomMetrics]]], jsii.get(self, "customMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverInput")
    def failover_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failoverInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsInput")
    def max_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsPerEndpointInput")
    def max_connections_per_endpoint_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionsPerEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsPerInstanceInput")
    def max_connections_per_instance_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionsPerInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRateInput")
    def max_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRateInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRatePerEndpointInput")
    def max_rate_per_endpoint_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRatePerEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRatePerInstanceInput")
    def max_rate_per_instance_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRatePerInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUtilizationInput")
    def max_utilization_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUtilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="balancingMode")
    def balancing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "balancingMode"))

    @balancing_mode.setter
    def balancing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062697336d0ed803581094c1d7939f541570a5e93723cec5fff82f9e0b82a9f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "balancingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacityScaler")
    def capacity_scaler(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "capacityScaler"))

    @capacity_scaler.setter
    def capacity_scaler(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c94769931fa978d5af929b9e2c1a0f6c47082b2d1df656a65e662b9be9419b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityScaler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36eadaa441d1fb1c9d33c7561dbea20bae4b616bd5820b78e5077ad4fc652b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failover")
    def failover(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failover"))

    @failover.setter
    def failover(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__535b1ecfbea28b4e77e45b44d50cdaaa5a92a59cbe05dbe110832648611e5af0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failover", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddce24dfe250f285b4d4f58c1ba674c6d3069ae844567988645cf00d5acb94df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConnections")
    def max_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnections"))

    @max_connections.setter
    def max_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce557fb9bfb5495528f1c808ff1d662d386f4ca188583c72d13cc69d55ba856b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsPerEndpoint")
    def max_connections_per_endpoint(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionsPerEndpoint"))

    @max_connections_per_endpoint.setter
    def max_connections_per_endpoint(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737e1ec3a817b9d7547ea1f6045c38799f7a869bf9cfbe6c6c162711de991c9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionsPerEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsPerInstance")
    def max_connections_per_instance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionsPerInstance"))

    @max_connections_per_instance.setter
    def max_connections_per_instance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca3fee823ae9ad4d761dd6bad0ed456e18aa598f09c7a58ac1076f099d846fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionsPerInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRate")
    def max_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRate"))

    @max_rate.setter
    def max_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f7a1da13e64478fc1f7e1ddde734c27d52a70451a1bd8674bab7a9c893f8632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRatePerEndpoint")
    def max_rate_per_endpoint(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRatePerEndpoint"))

    @max_rate_per_endpoint.setter
    def max_rate_per_endpoint(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05807f67dd21a7b8633b60c814878cb9e9f1c78f468a99297e4c912a2470ec49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRatePerEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRatePerInstance")
    def max_rate_per_instance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRatePerInstance"))

    @max_rate_per_instance.setter
    def max_rate_per_instance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6525731c1c925c670374a6b340048e74928f3df6803afc885ab9e2dd84d3f1d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRatePerInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUtilization")
    def max_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUtilization"))

    @max_utilization.setter
    def max_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01af17f911e17f0c8aad68edb28e47c8165c1c4dc88464d8f03d7cfa52542e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceBackend]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceBackend]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceBackend]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc079e314987c2ab239e893affa3daba627bbce319fdc961cca26a3fe3f70634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCdnPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "cache_key_policy": "cacheKeyPolicy",
        "cache_mode": "cacheMode",
        "client_ttl": "clientTtl",
        "default_ttl": "defaultTtl",
        "max_ttl": "maxTtl",
        "negative_caching": "negativeCaching",
        "negative_caching_policy": "negativeCachingPolicy",
        "serve_while_stale": "serveWhileStale",
        "signed_url_cache_max_age_sec": "signedUrlCacheMaxAgeSec",
    },
)
class GoogleComputeRegionBackendServiceCdnPolicy:
    def __init__(
        self,
        *,
        cache_key_policy: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[jsii.Number] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        max_ttl: typing.Optional[jsii.Number] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        serve_while_stale: typing.Optional[jsii.Number] = None,
        signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#cache_key_policy GoogleComputeRegionBackendService#cache_key_policy}
        :param cache_mode: Specifies the cache setting for all responses from this backend. The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#cache_mode GoogleComputeRegionBackendService#cache_mode}
        :param client_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#client_ttl GoogleComputeRegionBackendService#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#default_ttl GoogleComputeRegionBackendService#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_ttl GoogleComputeRegionBackendService#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#negative_caching GoogleComputeRegionBackendService#negative_caching}
        :param negative_caching_policy: negative_caching_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#negative_caching_policy GoogleComputeRegionBackendService#negative_caching_policy}
        :param serve_while_stale: Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#serve_while_stale GoogleComputeRegionBackendService#serve_while_stale}
        :param signed_url_cache_max_age_sec: Maximum number of seconds the response to a signed URL request will be considered fresh, defaults to 1hr (3600s). After this time period, the response will be revalidated before being served. When serving responses to signed URL requests, Cloud CDN will internally behave as though all responses from this backend had a "Cache-Control: public, max-age=[TTL]" header, regardless of any existing Cache-Control header. The actual headers served in responses will not be altered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#signed_url_cache_max_age_sec GoogleComputeRegionBackendService#signed_url_cache_max_age_sec}
        '''
        if isinstance(cache_key_policy, dict):
            cache_key_policy = GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy(**cache_key_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0dc9102c3ec9eeb6eb29250cae07f52e5a95a9d66b675876f7f52165c8fabf4)
            check_type(argname="argument cache_key_policy", value=cache_key_policy, expected_type=type_hints["cache_key_policy"])
            check_type(argname="argument cache_mode", value=cache_mode, expected_type=type_hints["cache_mode"])
            check_type(argname="argument client_ttl", value=client_ttl, expected_type=type_hints["client_ttl"])
            check_type(argname="argument default_ttl", value=default_ttl, expected_type=type_hints["default_ttl"])
            check_type(argname="argument max_ttl", value=max_ttl, expected_type=type_hints["max_ttl"])
            check_type(argname="argument negative_caching", value=negative_caching, expected_type=type_hints["negative_caching"])
            check_type(argname="argument negative_caching_policy", value=negative_caching_policy, expected_type=type_hints["negative_caching_policy"])
            check_type(argname="argument serve_while_stale", value=serve_while_stale, expected_type=type_hints["serve_while_stale"])
            check_type(argname="argument signed_url_cache_max_age_sec", value=signed_url_cache_max_age_sec, expected_type=type_hints["signed_url_cache_max_age_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if serve_while_stale is not None:
            self._values["serve_while_stale"] = serve_while_stale
        if signed_url_cache_max_age_sec is not None:
            self._values["signed_url_cache_max_age_sec"] = signed_url_cache_max_age_sec

    @builtins.property
    def cache_key_policy(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy"]:
        '''cache_key_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#cache_key_policy GoogleComputeRegionBackendService#cache_key_policy}
        '''
        result = self._values.get("cache_key_policy")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy"], result)

    @builtins.property
    def cache_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the cache setting for all responses from this backend.

        The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#cache_mode GoogleComputeRegionBackendService#cache_mode}
        '''
        result = self._values.get("cache_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum allowed TTL for cached content served by this origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#client_ttl GoogleComputeRegionBackendService#client_ttl}
        '''
        result = self._values.get("client_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#default_ttl GoogleComputeRegionBackendService#default_ttl}
        '''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum allowed TTL for cached content served by this origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_ttl GoogleComputeRegionBackendService#max_ttl}
        '''
        result = self._values.get("max_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def negative_caching(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#negative_caching GoogleComputeRegionBackendService#negative_caching}
        '''
        result = self._values.get("negative_caching")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def negative_caching_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy"]]]:
        '''negative_caching_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#negative_caching_policy GoogleComputeRegionBackendService#negative_caching_policy}
        '''
        result = self._values.get("negative_caching_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy"]]], result)

    @builtins.property
    def serve_while_stale(self) -> typing.Optional[jsii.Number]:
        '''Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#serve_while_stale GoogleComputeRegionBackendService#serve_while_stale}
        '''
        result = self._values.get("serve_while_stale")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def signed_url_cache_max_age_sec(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of seconds the response to a signed URL request will be considered fresh, defaults to 1hr (3600s).

        After this
        time period, the response will be revalidated before
        being served.

        When serving responses to signed URL requests, Cloud CDN will
        internally behave as though all responses from this backend had a
        "Cache-Control: public, max-age=[TTL]" header, regardless of any
        existing Cache-Control header. The actual headers served in
        responses will not be altered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#signed_url_cache_max_age_sec GoogleComputeRegionBackendService#signed_url_cache_max_age_sec}
        '''
        result = self._values.get("signed_url_cache_max_age_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceCdnPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "include_host": "includeHost",
        "include_named_cookies": "includeNamedCookies",
        "include_protocol": "includeProtocol",
        "include_query_string": "includeQueryString",
        "query_string_blacklist": "queryStringBlacklist",
        "query_string_whitelist": "queryStringWhitelist",
    },
)
class GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy:
    def __init__(
        self,
        *,
        include_host: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_named_cookies: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_protocol: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_query_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_string_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param include_host: If true requests to different hosts will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#include_host GoogleComputeRegionBackendService#include_host}
        :param include_named_cookies: Names of cookies to include in cache keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#include_named_cookies GoogleComputeRegionBackendService#include_named_cookies}
        :param include_protocol: If true, http and https requests will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#include_protocol GoogleComputeRegionBackendService#include_protocol}
        :param include_query_string: If true, include query string parameters in the cache key according to query_string_whitelist and query_string_blacklist. If neither is set, the entire query string will be included. If false, the query string will be excluded from the cache key entirely. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#include_query_string GoogleComputeRegionBackendService#include_query_string}
        :param query_string_blacklist: Names of query string parameters to exclude in cache keys. All other parameters will be included. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#query_string_blacklist GoogleComputeRegionBackendService#query_string_blacklist}
        :param query_string_whitelist: Names of query string parameters to include in cache keys. All other parameters will be excluded. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#query_string_whitelist GoogleComputeRegionBackendService#query_string_whitelist}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a9f810f4be69252c942f083e0607589ab57ae672e7699c207372f4b691debe)
            check_type(argname="argument include_host", value=include_host, expected_type=type_hints["include_host"])
            check_type(argname="argument include_named_cookies", value=include_named_cookies, expected_type=type_hints["include_named_cookies"])
            check_type(argname="argument include_protocol", value=include_protocol, expected_type=type_hints["include_protocol"])
            check_type(argname="argument include_query_string", value=include_query_string, expected_type=type_hints["include_query_string"])
            check_type(argname="argument query_string_blacklist", value=query_string_blacklist, expected_type=type_hints["query_string_blacklist"])
            check_type(argname="argument query_string_whitelist", value=query_string_whitelist, expected_type=type_hints["query_string_whitelist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_host is not None:
            self._values["include_host"] = include_host
        if include_named_cookies is not None:
            self._values["include_named_cookies"] = include_named_cookies
        if include_protocol is not None:
            self._values["include_protocol"] = include_protocol
        if include_query_string is not None:
            self._values["include_query_string"] = include_query_string
        if query_string_blacklist is not None:
            self._values["query_string_blacklist"] = query_string_blacklist
        if query_string_whitelist is not None:
            self._values["query_string_whitelist"] = query_string_whitelist

    @builtins.property
    def include_host(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true requests to different hosts will be cached separately.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#include_host GoogleComputeRegionBackendService#include_host}
        '''
        result = self._values.get("include_host")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_named_cookies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of cookies to include in cache keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#include_named_cookies GoogleComputeRegionBackendService#include_named_cookies}
        '''
        result = self._values.get("include_named_cookies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, http and https requests will be cached separately.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#include_protocol GoogleComputeRegionBackendService#include_protocol}
        '''
        result = self._values.get("include_protocol")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_query_string(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, include query string parameters in the cache key according to query_string_whitelist and query_string_blacklist.

        If neither is set, the entire query
        string will be included.

        If false, the query string will be excluded from the cache
        key entirely.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#include_query_string GoogleComputeRegionBackendService#include_query_string}
        '''
        result = self._values.get("include_query_string")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_string_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of query string parameters to exclude in cache keys.

        All other parameters will be included. Either specify
        query_string_whitelist or query_string_blacklist, not both.
        '&' and '=' will be percent encoded and not treated as
        delimiters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#query_string_blacklist GoogleComputeRegionBackendService#query_string_blacklist}
        '''
        result = self._values.get("query_string_blacklist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_string_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of query string parameters to include in cache keys.

        All other parameters will be excluded. Either specify
        query_string_whitelist or query_string_blacklist, not both.
        '&' and '=' will be percent encoded and not treated as
        delimiters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#query_string_whitelist GoogleComputeRegionBackendService#query_string_whitelist}
        '''
        result = self._values.get("query_string_whitelist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ed143ff51eda0a00b0b5aa08d4fef2c033ce23268e4de2c2a365b650c3d470d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeHost")
    def reset_include_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeHost", []))

    @jsii.member(jsii_name="resetIncludeNamedCookies")
    def reset_include_named_cookies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeNamedCookies", []))

    @jsii.member(jsii_name="resetIncludeProtocol")
    def reset_include_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeProtocol", []))

    @jsii.member(jsii_name="resetIncludeQueryString")
    def reset_include_query_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeQueryString", []))

    @jsii.member(jsii_name="resetQueryStringBlacklist")
    def reset_query_string_blacklist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringBlacklist", []))

    @jsii.member(jsii_name="resetQueryStringWhitelist")
    def reset_query_string_whitelist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringWhitelist", []))

    @builtins.property
    @jsii.member(jsii_name="includeHostInput")
    def include_host_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeHostInput"))

    @builtins.property
    @jsii.member(jsii_name="includeNamedCookiesInput")
    def include_named_cookies_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeNamedCookiesInput"))

    @builtins.property
    @jsii.member(jsii_name="includeProtocolInput")
    def include_protocol_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="includeQueryStringInput")
    def include_query_string_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeQueryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringBlacklistInput")
    def query_string_blacklist_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryStringBlacklistInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringWhitelistInput")
    def query_string_whitelist_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryStringWhitelistInput"))

    @builtins.property
    @jsii.member(jsii_name="includeHost")
    def include_host(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeHost"))

    @include_host.setter
    def include_host(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__156a09ea57bb569ec76e6e05d8c0a80aefe6e26dd2228ac12837f780729cd379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeNamedCookies")
    def include_named_cookies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeNamedCookies"))

    @include_named_cookies.setter
    def include_named_cookies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c816fbf3942cb05ddff88bfcc1282ad074e147effa62e1ca801c28e84589f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeNamedCookies", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__24666b720692db1a81c42f261f36c58bdec80042dc67d9d85c5cece3a74343dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeQueryString")
    def include_query_string(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeQueryString"))

    @include_query_string.setter
    def include_query_string(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1efec32b41fcf7f2388a8fe44551dcdd0301527924ab8a5efd093c46175abd31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeQueryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringBlacklist")
    def query_string_blacklist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringBlacklist"))

    @query_string_blacklist.setter
    def query_string_blacklist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585bcf1398ddc39485d19317a80efc8ab29819a212e01f5914edc69150cd0155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringBlacklist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringWhitelist")
    def query_string_whitelist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringWhitelist"))

    @query_string_whitelist.setter
    def query_string_whitelist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c330dbbe9b4f043b1bea9d5b00f29738afe52b9c6f0512a75d11a38ae8d1556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringWhitelist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca0472e06daab5b2a629e5772756bf0b82c1dabab742c3bae248b2816c00bca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy",
    jsii_struct_bases=[],
    name_mapping={"code": "code", "ttl": "ttl"},
)
class GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy:
    def __init__(
        self,
        *,
        code: typing.Optional[jsii.Number] = None,
        ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param code: The HTTP status code to define a TTL against. Only HTTP status codes 300, 301, 308, 404, 405, 410, 421, 451 and 501 can be specified as values, and you cannot specify a status code more than once. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#code GoogleComputeRegionBackendService#code}
        :param ttl: The TTL (in seconds) for which to cache responses with the corresponding status code. The maximum allowed value is 1800s (30 minutes), noting that infrequently accessed objects may be evicted from the cache before the defined TTL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ttl GoogleComputeRegionBackendService#ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b122232dbe8effe1183be418f5091848b9dcb94d0724af8e640b605f582be5cf)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code is not None:
            self._values["code"] = code
        if ttl is not None:
            self._values["ttl"] = ttl

    @builtins.property
    def code(self) -> typing.Optional[jsii.Number]:
        '''The HTTP status code to define a TTL against.

        Only HTTP status codes 300, 301, 308, 404, 405, 410, 421, 451 and 501
        can be specified as values, and you cannot specify a status code more than once.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#code GoogleComputeRegionBackendService#code}
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''The TTL (in seconds) for which to cache responses with the corresponding status code.

        The maximum allowed value is 1800s
        (30 minutes), noting that infrequently accessed objects may be evicted from the cache before the defined TTL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ttl GoogleComputeRegionBackendService#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd4b4344691ea58a4525b465f192fdff10e1610f73ef2d5a34ab55ad0ab378fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff9e3c3814b819cc704a888e0be92c7fc85d35c5cfd070245e51f2b36e4e544)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24077b4a9909a4ec6de7c171f1054d99daf466851293ec4c8fc1f51f7cccd6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12cbecf14dfc8911a81b35aeeff8758991c151da162b62190d91d0d6928a9ce3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f70f6eddd81855951648dc8ce8181f085651794b084275b36d7ce62dd5fedd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3fa3c57f929f6e9e96fc7ca3cfeaf939c34a9101810c48bc42fe07793d19f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__169159986fe0eb15cb88598bbefd5b60a85ece2fadbfe60bd098b1ce93a008f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCode")
    def reset_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCode", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @builtins.property
    @jsii.member(jsii_name="codeInput")
    def code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "codeInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @code.setter
    def code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7fc89d42e187ef59a46e8954ae02bdd75bbfa8f28a0543528781632a1f31bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae53def47fdf69bb6452a9c6127f8a78f32c53fb7fbee514f31fab111df6f47f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f031c14cbed241618b8997e7b1111a81127a1f9b576a5e3d0df9f9c5c9278f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionBackendServiceCdnPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCdnPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6400dd3bba24cb8032b5e7bb4fd99fc842325f28461ba27c29169ae28acb18b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCacheKeyPolicy")
    def put_cache_key_policy(
        self,
        *,
        include_host: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_named_cookies: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_protocol: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_query_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_string_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param include_host: If true requests to different hosts will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#include_host GoogleComputeRegionBackendService#include_host}
        :param include_named_cookies: Names of cookies to include in cache keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#include_named_cookies GoogleComputeRegionBackendService#include_named_cookies}
        :param include_protocol: If true, http and https requests will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#include_protocol GoogleComputeRegionBackendService#include_protocol}
        :param include_query_string: If true, include query string parameters in the cache key according to query_string_whitelist and query_string_blacklist. If neither is set, the entire query string will be included. If false, the query string will be excluded from the cache key entirely. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#include_query_string GoogleComputeRegionBackendService#include_query_string}
        :param query_string_blacklist: Names of query string parameters to exclude in cache keys. All other parameters will be included. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#query_string_blacklist GoogleComputeRegionBackendService#query_string_blacklist}
        :param query_string_whitelist: Names of query string parameters to include in cache keys. All other parameters will be excluded. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#query_string_whitelist GoogleComputeRegionBackendService#query_string_whitelist}
        '''
        value = GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy(
            include_host=include_host,
            include_named_cookies=include_named_cookies,
            include_protocol=include_protocol,
            include_query_string=include_query_string,
            query_string_blacklist=query_string_blacklist,
            query_string_whitelist=query_string_whitelist,
        )

        return typing.cast(None, jsii.invoke(self, "putCacheKeyPolicy", [value]))

    @jsii.member(jsii_name="putNegativeCachingPolicy")
    def put_negative_caching_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f8eab777f35d4ece770f45731b2e87a94b95a0da39095bc3a31c6ade3ec940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNegativeCachingPolicy", [value]))

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

    @jsii.member(jsii_name="resetServeWhileStale")
    def reset_serve_while_stale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServeWhileStale", []))

    @jsii.member(jsii_name="resetSignedUrlCacheMaxAgeSec")
    def reset_signed_url_cache_max_age_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignedUrlCacheMaxAgeSec", []))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyPolicy")
    def cache_key_policy(
        self,
    ) -> GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicyOutputReference:
        return typing.cast(GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicyOutputReference, jsii.get(self, "cacheKeyPolicy"))

    @builtins.property
    @jsii.member(jsii_name="negativeCachingPolicy")
    def negative_caching_policy(
        self,
    ) -> GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyList:
        return typing.cast(GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyList, jsii.get(self, "negativeCachingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyPolicyInput")
    def cache_key_policy_input(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy], jsii.get(self, "cacheKeyPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheModeInput")
    def cache_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheModeInput"))

    @builtins.property
    @jsii.member(jsii_name="clientTtlInput")
    def client_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clientTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTtlInput")
    def default_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTtlInput")
    def max_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxTtlInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]], jsii.get(self, "negativeCachingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="serveWhileStaleInput")
    def serve_while_stale_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "serveWhileStaleInput"))

    @builtins.property
    @jsii.member(jsii_name="signedUrlCacheMaxAgeSecInput")
    def signed_url_cache_max_age_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "signedUrlCacheMaxAgeSecInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheMode")
    def cache_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheMode"))

    @cache_mode.setter
    def cache_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691a53f793dc1fc2c90f3b9704e950a2b892ab51bf4fe44989bde1367c9f63d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTtl")
    def client_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientTtl"))

    @client_ttl.setter
    def client_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a76f8b145ae4db179fa3f3ac2991ac7492a7d5617f51f23b031bebf0592b3de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37bff7ac53bcb02c58d131a8b640a6601039822bd82a43d7a0f3b18c589b374c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTtl")
    def max_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxTtl"))

    @max_ttl.setter
    def max_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306b8ebf73582fe0ed2a013c2a0fd769de8a35a3f8e2654cdad63905c6d2693c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c717c7a16786722f571ad82880f43c5a807501dfb3c68f228eca0d6e01dad6d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negativeCaching", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serveWhileStale")
    def serve_while_stale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "serveWhileStale"))

    @serve_while_stale.setter
    def serve_while_stale(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d1be0e408c8d1350c8c9a5ae562a73b76f2149b0716b14d9fd7538bdb0ef4fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serveWhileStale", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signedUrlCacheMaxAgeSec")
    def signed_url_cache_max_age_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "signedUrlCacheMaxAgeSec"))

    @signed_url_cache_max_age_sec.setter
    def signed_url_cache_max_age_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591689939c12763d4b015a4c640a64cb9934ad0a55697c9b564f8c5f7d922c03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signedUrlCacheMaxAgeSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceCdnPolicy]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceCdnPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceCdnPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e200d33c435e40cf5eb5401db6b66206bfbf842a18c24b634207a8301c3654b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCircuitBreakers",
    jsii_struct_bases=[],
    name_mapping={
        "connect_timeout": "connectTimeout",
        "max_connections": "maxConnections",
        "max_pending_requests": "maxPendingRequests",
        "max_requests": "maxRequests",
        "max_requests_per_connection": "maxRequestsPerConnection",
        "max_retries": "maxRetries",
    },
)
class GoogleComputeRegionBackendServiceCircuitBreakers:
    def __init__(
        self,
        *,
        connect_timeout: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        max_connections: typing.Optional[jsii.Number] = None,
        max_pending_requests: typing.Optional[jsii.Number] = None,
        max_requests: typing.Optional[jsii.Number] = None,
        max_requests_per_connection: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connect_timeout: connect_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#connect_timeout GoogleComputeRegionBackendService#connect_timeout}
        :param max_connections: The maximum number of connections to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_connections GoogleComputeRegionBackendService#max_connections}
        :param max_pending_requests: The maximum number of pending requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_pending_requests GoogleComputeRegionBackendService#max_pending_requests}
        :param max_requests: The maximum number of parallel requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_requests GoogleComputeRegionBackendService#max_requests}
        :param max_requests_per_connection: Maximum requests for a single backend connection. This parameter is respected by both the HTTP/1.1 and HTTP/2 implementations. If not specified, there is no limit. Setting this parameter to 1 will effectively disable keep alive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_requests_per_connection GoogleComputeRegionBackendService#max_requests_per_connection}
        :param max_retries: The maximum number of parallel retries to the backend cluster. Defaults to 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_retries GoogleComputeRegionBackendService#max_retries}
        '''
        if isinstance(connect_timeout, dict):
            connect_timeout = GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout(**connect_timeout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73f3471329f2687abcea89668b43f169a5960a7376f8390f7a465db4e8a8813)
            check_type(argname="argument connect_timeout", value=connect_timeout, expected_type=type_hints["connect_timeout"])
            check_type(argname="argument max_connections", value=max_connections, expected_type=type_hints["max_connections"])
            check_type(argname="argument max_pending_requests", value=max_pending_requests, expected_type=type_hints["max_pending_requests"])
            check_type(argname="argument max_requests", value=max_requests, expected_type=type_hints["max_requests"])
            check_type(argname="argument max_requests_per_connection", value=max_requests_per_connection, expected_type=type_hints["max_requests_per_connection"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connect_timeout is not None:
            self._values["connect_timeout"] = connect_timeout
        if max_connections is not None:
            self._values["max_connections"] = max_connections
        if max_pending_requests is not None:
            self._values["max_pending_requests"] = max_pending_requests
        if max_requests is not None:
            self._values["max_requests"] = max_requests
        if max_requests_per_connection is not None:
            self._values["max_requests_per_connection"] = max_requests_per_connection
        if max_retries is not None:
            self._values["max_retries"] = max_retries

    @builtins.property
    def connect_timeout(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout"]:
        '''connect_timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#connect_timeout GoogleComputeRegionBackendService#connect_timeout}
        '''
        result = self._values.get("connect_timeout")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout"], result)

    @builtins.property
    def max_connections(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of connections to the backend cluster. Defaults to 1024.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_connections GoogleComputeRegionBackendService#max_connections}
        '''
        result = self._values.get("max_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_pending_requests(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of pending requests to the backend cluster. Defaults to 1024.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_pending_requests GoogleComputeRegionBackendService#max_pending_requests}
        '''
        result = self._values.get("max_pending_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_requests(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of parallel requests to the backend cluster. Defaults to 1024.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_requests GoogleComputeRegionBackendService#max_requests}
        '''
        result = self._values.get("max_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_requests_per_connection(self) -> typing.Optional[jsii.Number]:
        '''Maximum requests for a single backend connection.

        This parameter
        is respected by both the HTTP/1.1 and HTTP/2 implementations. If
        not specified, there is no limit. Setting this parameter to 1
        will effectively disable keep alive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_requests_per_connection GoogleComputeRegionBackendService#max_requests_per_connection}
        '''
        result = self._values.get("max_requests_per_connection")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of parallel retries to the backend cluster. Defaults to 3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_retries GoogleComputeRegionBackendService#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceCircuitBreakers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d5951b1cd2d910a2fef9751320389492ddb7df5001339b1606542d697c5d1f)
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "seconds": seconds,
        }
        if nanos is not None:
            self._values["nanos"] = nanos

    @builtins.property
    def seconds(self) -> jsii.Number:
        '''Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        '''
        result = self._values.get("seconds")
        assert result is not None, "Required property 'seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Span of time that's a fraction of a second at nanosecond resolution.

        Durations less than one second are represented
        with a 0 seconds field and a positive nanos field. Must
        be from 0 to 999,999,999 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b4f5aa9447a517a0117eabf9262610becfe276abf5c7b3fd9980bfeb98f068e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c884924ba86c6452070c42b89f77a09a7ddbe357eb162b6e5ab150ed6195866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173992e7e59706aa1aa525d2005d61390aa8849901ad81b2548ae0badc53e58b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f76bddb7c7f017b1b25631be988cd19bd339035aeb07972ebff3b7d476f44348)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionBackendServiceCircuitBreakersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCircuitBreakersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6ac5362d42f6efaa56ece05f8846725891b50770ad1c6632e5d6cc92b946902)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConnectTimeout")
    def put_connect_timeout(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        value = GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout(
            seconds=seconds, nanos=nanos
        )

        return typing.cast(None, jsii.invoke(self, "putConnectTimeout", [value]))

    @jsii.member(jsii_name="resetConnectTimeout")
    def reset_connect_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectTimeout", []))

    @jsii.member(jsii_name="resetMaxConnections")
    def reset_max_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnections", []))

    @jsii.member(jsii_name="resetMaxPendingRequests")
    def reset_max_pending_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPendingRequests", []))

    @jsii.member(jsii_name="resetMaxRequests")
    def reset_max_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRequests", []))

    @jsii.member(jsii_name="resetMaxRequestsPerConnection")
    def reset_max_requests_per_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRequestsPerConnection", []))

    @jsii.member(jsii_name="resetMaxRetries")
    def reset_max_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetries", []))

    @builtins.property
    @jsii.member(jsii_name="connectTimeout")
    def connect_timeout(
        self,
    ) -> GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeoutOutputReference:
        return typing.cast(GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeoutOutputReference, jsii.get(self, "connectTimeout"))

    @builtins.property
    @jsii.member(jsii_name="connectTimeoutInput")
    def connect_timeout_input(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout], jsii.get(self, "connectTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsInput")
    def max_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPendingRequestsInput")
    def max_pending_requests_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPendingRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRequestsInput")
    def max_requests_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRequestsPerConnectionInput")
    def max_requests_per_connection_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRequestsPerConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnections")
    def max_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnections"))

    @max_connections.setter
    def max_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d07a42fdbe013e299427d0031ff7f8cce0cd95bb0491b97b6bd6fc00abd41f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPendingRequests")
    def max_pending_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPendingRequests"))

    @max_pending_requests.setter
    def max_pending_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__389f58fe63125a05fd9f364043d3fca4d1bee80597a14c5d35692c50894953ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPendingRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRequests")
    def max_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRequests"))

    @max_requests.setter
    def max_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b88083156bd98d519f3847441f787f4ca9c50479fcc6f0dabdd18eda82573f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRequestsPerConnection")
    def max_requests_per_connection(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRequestsPerConnection"))

    @max_requests_per_connection.setter
    def max_requests_per_connection(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42aa84559c0afeadb2e55900e405211aaad2300f08c3922bc7b5084225f9d6ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequestsPerConnection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba7399e478b18f8bc0f9bdaa470543164165e18c12dc365120d722f2c8ec7a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceCircuitBreakers]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceCircuitBreakers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceCircuitBreakers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40b25cc55fef9e456d84e39ec4a36fef8a5c6b81ece717a6b3dde89f822a855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceConfig",
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
        "affinity_cookie_ttl_sec": "affinityCookieTtlSec",
        "backend": "backend",
        "cdn_policy": "cdnPolicy",
        "circuit_breakers": "circuitBreakers",
        "connection_draining_timeout_sec": "connectionDrainingTimeoutSec",
        "connection_tracking_policy": "connectionTrackingPolicy",
        "consistent_hash": "consistentHash",
        "custom_metrics": "customMetrics",
        "description": "description",
        "dynamic_forwarding": "dynamicForwarding",
        "enable_cdn": "enableCdn",
        "failover_policy": "failoverPolicy",
        "health_checks": "healthChecks",
        "iap": "iap",
        "id": "id",
        "ip_address_selection_policy": "ipAddressSelectionPolicy",
        "load_balancing_scheme": "loadBalancingScheme",
        "locality_lb_policy": "localityLbPolicy",
        "log_config": "logConfig",
        "network": "network",
        "outlier_detection": "outlierDetection",
        "port_name": "portName",
        "project": "project",
        "protocol": "protocol",
        "region": "region",
        "security_policy": "securityPolicy",
        "session_affinity": "sessionAffinity",
        "strong_session_affinity_cookie": "strongSessionAffinityCookie",
        "subsetting": "subsetting",
        "timeouts": "timeouts",
        "timeout_sec": "timeoutSec",
    },
)
class GoogleComputeRegionBackendServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        affinity_cookie_ttl_sec: typing.Optional[jsii.Number] = None,
        backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cdn_policy: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        circuit_breakers: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceCircuitBreakers, typing.Dict[builtins.str, typing.Any]]] = None,
        connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
        connection_tracking_policy: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceConnectionTrackingPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        consistent_hash: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceConsistentHash", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRegionBackendServiceCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamic_forwarding: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceDynamicForwarding", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failover_policy: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceFailoverPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        iap: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceIap", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address_selection_policy: typing.Optional[builtins.str] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        locality_lb_policy: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[builtins.str] = None,
        outlier_detection: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceOutlierDetection", typing.Dict[builtins.str, typing.Any]]] = None,
        port_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        security_policy: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        strong_session_affinity_cookie: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceStrongSessionAffinityCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        subsetting: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceSubsetting", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#name GoogleComputeRegionBackendService#name}
        :param affinity_cookie_ttl_sec: Lifetime of cookies in seconds if session_affinity is GENERATED_COOKIE. If set to 0, the cookie is non-persistent and lasts only until the end of the browser session (or equivalent). The maximum allowed value for TTL is one day. When the load balancing scheme is INTERNAL, this field is not used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#affinity_cookie_ttl_sec GoogleComputeRegionBackendService#affinity_cookie_ttl_sec}
        :param backend: backend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#backend GoogleComputeRegionBackendService#backend}
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#cdn_policy GoogleComputeRegionBackendService#cdn_policy}
        :param circuit_breakers: circuit_breakers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#circuit_breakers GoogleComputeRegionBackendService#circuit_breakers}
        :param connection_draining_timeout_sec: Time for which instance will be drained (not accept new connections, but still work to finish started). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#connection_draining_timeout_sec GoogleComputeRegionBackendService#connection_draining_timeout_sec}
        :param connection_tracking_policy: connection_tracking_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#connection_tracking_policy GoogleComputeRegionBackendService#connection_tracking_policy}
        :param consistent_hash: consistent_hash block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#consistent_hash GoogleComputeRegionBackendService#consistent_hash}
        :param custom_metrics: custom_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#custom_metrics GoogleComputeRegionBackendService#custom_metrics}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#description GoogleComputeRegionBackendService#description}
        :param dynamic_forwarding: dynamic_forwarding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#dynamic_forwarding GoogleComputeRegionBackendService#dynamic_forwarding}
        :param enable_cdn: If true, enable Cloud CDN for this RegionBackendService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enable_cdn GoogleComputeRegionBackendService#enable_cdn}
        :param failover_policy: failover_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#failover_policy GoogleComputeRegionBackendService#failover_policy}
        :param health_checks: The set of URLs to HealthCheck resources for health checking this RegionBackendService. Currently at most one health check can be specified. A health check must be specified unless the backend service uses an internet or serverless NEG as a backend. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#health_checks GoogleComputeRegionBackendService#health_checks}
        :param iap: iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#iap GoogleComputeRegionBackendService#iap}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#id GoogleComputeRegionBackendService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address_selection_policy: Specifies preference of traffic to the backend (from the proxy and from the client for proxyless gRPC). Possible values: ["IPV4_ONLY", "PREFER_IPV6", "IPV6_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ip_address_selection_policy GoogleComputeRegionBackendService#ip_address_selection_policy}
        :param load_balancing_scheme: Indicates what kind of load balancing this regional backend service will be used for. A backend service created for one type of load balancing cannot be used with the other(s). For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_. Default value: "INTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL", "INTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#load_balancing_scheme GoogleComputeRegionBackendService#load_balancing_scheme}
        :param locality_lb_policy: The load balancing algorithm used within the scope of the locality. The possible values are:. - 'ROUND_ROBIN': This is a simple policy in which each healthy backend is selected in round robin order. - 'LEAST_REQUEST': An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests. - 'RING_HASH': The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests. - 'RANDOM': The load balancer selects a random healthy host. - 'ORIGINAL_DESTINATION': Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer. - 'MAGLEV': used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, refer to https://ai.google/research/pubs/pub44824 - 'WEIGHTED_MAGLEV': Per-instance weighted Load Balancing via health check reported weights. Only applicable to loadBalancingScheme EXTERNAL. If set, the Backend Service must configure a non legacy HTTP-based Health Check, and health check replies are expected to contain non-standard HTTP response header field X-Load-Balancing-Endpoint-Weight to specify the per-instance weights. If set, Load Balancing is weight based on the per-instance weights reported in the last processed health check replies, as long as every instance either reported a valid weight or had UNAVAILABLE_WEIGHT. Otherwise, Load Balancing remains equal-weight. - 'WEIGHTED_ROUND_ROBIN': Per-endpoint weighted round-robin Load Balancing using weights computed from Backend reported Custom Metrics. If set, the Backend Service responses are expected to contain non-standard HTTP response header field X-Endpoint-Load-Metrics. The reported metrics to use for computing the weights are specified via the backends[].customMetrics fields. locality_lb_policy is applicable to either: - A regional backend service with the service_protocol set to HTTP, HTTPS, HTTP2 or H2C, and loadBalancingScheme set to INTERNAL_MANAGED. - A global backend service with the load_balancing_scheme set to INTERNAL_SELF_MANAGED. - A regional backend service with loadBalancingScheme set to EXTERNAL (External Network Load Balancing). Only MAGLEV and WEIGHTED_MAGLEV values are possible for External Network Load Balancing. The default is MAGLEV. If session_affinity is not NONE, and locality_lb_policy is not set to MAGLEV, WEIGHTED_MAGLEV, or RING_HASH, session affinity settings will not take effect. Only ROUND_ROBIN and RING_HASH are supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validate_for_proxyless field set to true. Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV", "WEIGHTED_MAGLEV", "WEIGHTED_ROUND_ROBIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#locality_lb_policy GoogleComputeRegionBackendService#locality_lb_policy}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#log_config GoogleComputeRegionBackendService#log_config}
        :param network: The URL of the network to which this backend service belongs. This field can only be specified when the load balancing scheme is set to INTERNAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#network GoogleComputeRegionBackendService#network}
        :param outlier_detection: outlier_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#outlier_detection GoogleComputeRegionBackendService#outlier_detection}
        :param port_name: A named port on a backend instance group representing the port for communication to the backend VMs in that group. Required when the loadBalancingScheme is EXTERNAL, EXTERNAL_MANAGED, INTERNAL_MANAGED, or INTERNAL_SELF_MANAGED and the backends are instance groups. The named port must be defined on each backend instance group. This parameter has no meaning if the backends are NEGs. API sets a default of "http" if not given. Must be omitted when the loadBalancingScheme is INTERNAL (Internal TCP/UDP Load Balancing). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#port_name GoogleComputeRegionBackendService#port_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#project GoogleComputeRegionBackendService#project}.
        :param protocol: The protocol this BackendService uses to communicate with backends. The default is HTTP. Possible values are HTTP, HTTPS, HTTP2, H2C, TCP, SSL, UDP or GRPC. Refer to the documentation for the load balancers or for Traffic Director for more information. Possible values: ["HTTP", "HTTPS", "HTTP2", "TCP", "SSL", "UDP", "GRPC", "UNSPECIFIED", "H2C"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#protocol GoogleComputeRegionBackendService#protocol}
        :param region: The Region in which the created backend service should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#region GoogleComputeRegionBackendService#region}
        :param security_policy: The security policy associated with this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#security_policy GoogleComputeRegionBackendService#security_policy}
        :param session_affinity: Type of session affinity to use. The default is NONE. Session affinity is not applicable if the protocol is UDP. Possible values: ["NONE", "CLIENT_IP", "CLIENT_IP_PORT_PROTO", "CLIENT_IP_PROTO", "GENERATED_COOKIE", "HEADER_FIELD", "HTTP_COOKIE", "CLIENT_IP_NO_DESTINATION", "STRONG_COOKIE_AFFINITY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#session_affinity GoogleComputeRegionBackendService#session_affinity}
        :param strong_session_affinity_cookie: strong_session_affinity_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#strong_session_affinity_cookie GoogleComputeRegionBackendService#strong_session_affinity_cookie}
        :param subsetting: subsetting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#subsetting GoogleComputeRegionBackendService#subsetting}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#timeouts GoogleComputeRegionBackendService#timeouts}
        :param timeout_sec: The backend service timeout has a different meaning depending on the type of load balancer. For more information see, `Backend service settings <https://cloud.google.com/compute/docs/reference/rest/v1/backendServices>`_. The default is 30 seconds. The full range of timeout values allowed goes from 1 through 2,147,483,647 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#timeout_sec GoogleComputeRegionBackendService#timeout_sec}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cdn_policy, dict):
            cdn_policy = GoogleComputeRegionBackendServiceCdnPolicy(**cdn_policy)
        if isinstance(circuit_breakers, dict):
            circuit_breakers = GoogleComputeRegionBackendServiceCircuitBreakers(**circuit_breakers)
        if isinstance(connection_tracking_policy, dict):
            connection_tracking_policy = GoogleComputeRegionBackendServiceConnectionTrackingPolicy(**connection_tracking_policy)
        if isinstance(consistent_hash, dict):
            consistent_hash = GoogleComputeRegionBackendServiceConsistentHash(**consistent_hash)
        if isinstance(dynamic_forwarding, dict):
            dynamic_forwarding = GoogleComputeRegionBackendServiceDynamicForwarding(**dynamic_forwarding)
        if isinstance(failover_policy, dict):
            failover_policy = GoogleComputeRegionBackendServiceFailoverPolicy(**failover_policy)
        if isinstance(iap, dict):
            iap = GoogleComputeRegionBackendServiceIap(**iap)
        if isinstance(log_config, dict):
            log_config = GoogleComputeRegionBackendServiceLogConfig(**log_config)
        if isinstance(outlier_detection, dict):
            outlier_detection = GoogleComputeRegionBackendServiceOutlierDetection(**outlier_detection)
        if isinstance(strong_session_affinity_cookie, dict):
            strong_session_affinity_cookie = GoogleComputeRegionBackendServiceStrongSessionAffinityCookie(**strong_session_affinity_cookie)
        if isinstance(subsetting, dict):
            subsetting = GoogleComputeRegionBackendServiceSubsetting(**subsetting)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeRegionBackendServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cbca61b22bfc77949d7978e79f7e87c59f7a62321bf336b58551e46bf689f93)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument affinity_cookie_ttl_sec", value=affinity_cookie_ttl_sec, expected_type=type_hints["affinity_cookie_ttl_sec"])
            check_type(argname="argument backend", value=backend, expected_type=type_hints["backend"])
            check_type(argname="argument cdn_policy", value=cdn_policy, expected_type=type_hints["cdn_policy"])
            check_type(argname="argument circuit_breakers", value=circuit_breakers, expected_type=type_hints["circuit_breakers"])
            check_type(argname="argument connection_draining_timeout_sec", value=connection_draining_timeout_sec, expected_type=type_hints["connection_draining_timeout_sec"])
            check_type(argname="argument connection_tracking_policy", value=connection_tracking_policy, expected_type=type_hints["connection_tracking_policy"])
            check_type(argname="argument consistent_hash", value=consistent_hash, expected_type=type_hints["consistent_hash"])
            check_type(argname="argument custom_metrics", value=custom_metrics, expected_type=type_hints["custom_metrics"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dynamic_forwarding", value=dynamic_forwarding, expected_type=type_hints["dynamic_forwarding"])
            check_type(argname="argument enable_cdn", value=enable_cdn, expected_type=type_hints["enable_cdn"])
            check_type(argname="argument failover_policy", value=failover_policy, expected_type=type_hints["failover_policy"])
            check_type(argname="argument health_checks", value=health_checks, expected_type=type_hints["health_checks"])
            check_type(argname="argument iap", value=iap, expected_type=type_hints["iap"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_address_selection_policy", value=ip_address_selection_policy, expected_type=type_hints["ip_address_selection_policy"])
            check_type(argname="argument load_balancing_scheme", value=load_balancing_scheme, expected_type=type_hints["load_balancing_scheme"])
            check_type(argname="argument locality_lb_policy", value=locality_lb_policy, expected_type=type_hints["locality_lb_policy"])
            check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument outlier_detection", value=outlier_detection, expected_type=type_hints["outlier_detection"])
            check_type(argname="argument port_name", value=port_name, expected_type=type_hints["port_name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            check_type(argname="argument session_affinity", value=session_affinity, expected_type=type_hints["session_affinity"])
            check_type(argname="argument strong_session_affinity_cookie", value=strong_session_affinity_cookie, expected_type=type_hints["strong_session_affinity_cookie"])
            check_type(argname="argument subsetting", value=subsetting, expected_type=type_hints["subsetting"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument timeout_sec", value=timeout_sec, expected_type=type_hints["timeout_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if affinity_cookie_ttl_sec is not None:
            self._values["affinity_cookie_ttl_sec"] = affinity_cookie_ttl_sec
        if backend is not None:
            self._values["backend"] = backend
        if cdn_policy is not None:
            self._values["cdn_policy"] = cdn_policy
        if circuit_breakers is not None:
            self._values["circuit_breakers"] = circuit_breakers
        if connection_draining_timeout_sec is not None:
            self._values["connection_draining_timeout_sec"] = connection_draining_timeout_sec
        if connection_tracking_policy is not None:
            self._values["connection_tracking_policy"] = connection_tracking_policy
        if consistent_hash is not None:
            self._values["consistent_hash"] = consistent_hash
        if custom_metrics is not None:
            self._values["custom_metrics"] = custom_metrics
        if description is not None:
            self._values["description"] = description
        if dynamic_forwarding is not None:
            self._values["dynamic_forwarding"] = dynamic_forwarding
        if enable_cdn is not None:
            self._values["enable_cdn"] = enable_cdn
        if failover_policy is not None:
            self._values["failover_policy"] = failover_policy
        if health_checks is not None:
            self._values["health_checks"] = health_checks
        if iap is not None:
            self._values["iap"] = iap
        if id is not None:
            self._values["id"] = id
        if ip_address_selection_policy is not None:
            self._values["ip_address_selection_policy"] = ip_address_selection_policy
        if load_balancing_scheme is not None:
            self._values["load_balancing_scheme"] = load_balancing_scheme
        if locality_lb_policy is not None:
            self._values["locality_lb_policy"] = locality_lb_policy
        if log_config is not None:
            self._values["log_config"] = log_config
        if network is not None:
            self._values["network"] = network
        if outlier_detection is not None:
            self._values["outlier_detection"] = outlier_detection
        if port_name is not None:
            self._values["port_name"] = port_name
        if project is not None:
            self._values["project"] = project
        if protocol is not None:
            self._values["protocol"] = protocol
        if region is not None:
            self._values["region"] = region
        if security_policy is not None:
            self._values["security_policy"] = security_policy
        if session_affinity is not None:
            self._values["session_affinity"] = session_affinity
        if strong_session_affinity_cookie is not None:
            self._values["strong_session_affinity_cookie"] = strong_session_affinity_cookie
        if subsetting is not None:
            self._values["subsetting"] = subsetting
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if timeout_sec is not None:
            self._values["timeout_sec"] = timeout_sec

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#name GoogleComputeRegionBackendService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def affinity_cookie_ttl_sec(self) -> typing.Optional[jsii.Number]:
        '''Lifetime of cookies in seconds if session_affinity is GENERATED_COOKIE.

        If set to 0, the cookie is non-persistent and lasts
        only until the end of the browser session (or equivalent). The
        maximum allowed value for TTL is one day.

        When the load balancing scheme is INTERNAL, this field is not used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#affinity_cookie_ttl_sec GoogleComputeRegionBackendService#affinity_cookie_ttl_sec}
        '''
        result = self._values.get("affinity_cookie_ttl_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def backend(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceBackend]]]:
        '''backend block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#backend GoogleComputeRegionBackendService#backend}
        '''
        result = self._values.get("backend")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceBackend]]], result)

    @builtins.property
    def cdn_policy(self) -> typing.Optional[GoogleComputeRegionBackendServiceCdnPolicy]:
        '''cdn_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#cdn_policy GoogleComputeRegionBackendService#cdn_policy}
        '''
        result = self._values.get("cdn_policy")
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceCdnPolicy], result)

    @builtins.property
    def circuit_breakers(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceCircuitBreakers]:
        '''circuit_breakers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#circuit_breakers GoogleComputeRegionBackendService#circuit_breakers}
        '''
        result = self._values.get("circuit_breakers")
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceCircuitBreakers], result)

    @builtins.property
    def connection_draining_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Time for which instance will be drained (not accept new connections, but still work to finish started).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#connection_draining_timeout_sec GoogleComputeRegionBackendService#connection_draining_timeout_sec}
        '''
        result = self._values.get("connection_draining_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def connection_tracking_policy(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceConnectionTrackingPolicy"]:
        '''connection_tracking_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#connection_tracking_policy GoogleComputeRegionBackendService#connection_tracking_policy}
        '''
        result = self._values.get("connection_tracking_policy")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceConnectionTrackingPolicy"], result)

    @builtins.property
    def consistent_hash(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceConsistentHash"]:
        '''consistent_hash block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#consistent_hash GoogleComputeRegionBackendService#consistent_hash}
        '''
        result = self._values.get("consistent_hash")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceConsistentHash"], result)

    @builtins.property
    def custom_metrics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionBackendServiceCustomMetrics"]]]:
        '''custom_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#custom_metrics GoogleComputeRegionBackendService#custom_metrics}
        '''
        result = self._values.get("custom_metrics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRegionBackendServiceCustomMetrics"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#description GoogleComputeRegionBackendService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamic_forwarding(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceDynamicForwarding"]:
        '''dynamic_forwarding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#dynamic_forwarding GoogleComputeRegionBackendService#dynamic_forwarding}
        '''
        result = self._values.get("dynamic_forwarding")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceDynamicForwarding"], result)

    @builtins.property
    def enable_cdn(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, enable Cloud CDN for this RegionBackendService.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enable_cdn GoogleComputeRegionBackendService#enable_cdn}
        '''
        result = self._values.get("enable_cdn")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def failover_policy(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceFailoverPolicy"]:
        '''failover_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#failover_policy GoogleComputeRegionBackendService#failover_policy}
        '''
        result = self._values.get("failover_policy")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceFailoverPolicy"], result)

    @builtins.property
    def health_checks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of URLs to HealthCheck resources for health checking this RegionBackendService. Currently at most one health check can be specified.

        A health check must be specified unless the backend service uses an internet
        or serverless NEG as a backend.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#health_checks GoogleComputeRegionBackendService#health_checks}
        '''
        result = self._values.get("health_checks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def iap(self) -> typing.Optional["GoogleComputeRegionBackendServiceIap"]:
        '''iap block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#iap GoogleComputeRegionBackendService#iap}
        '''
        result = self._values.get("iap")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceIap"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#id GoogleComputeRegionBackendService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address_selection_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies preference of traffic to the backend (from the proxy and from the client for proxyless gRPC).

        Possible values: ["IPV4_ONLY", "PREFER_IPV6", "IPV6_ONLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ip_address_selection_policy GoogleComputeRegionBackendService#ip_address_selection_policy}
        '''
        result = self._values.get("ip_address_selection_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancing_scheme(self) -> typing.Optional[builtins.str]:
        '''Indicates what kind of load balancing this regional backend service will be used for.

        A backend service created for one type of load
        balancing cannot be used with the other(s). For more information, refer to
        `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_. Default value: "INTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL", "INTERNAL_MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#load_balancing_scheme GoogleComputeRegionBackendService#load_balancing_scheme}
        '''
        result = self._values.get("load_balancing_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality_lb_policy(self) -> typing.Optional[builtins.str]:
        '''The load balancing algorithm used within the scope of the locality. The possible values are:.

        - 'ROUND_ROBIN': This is a simple policy in which each healthy backend
          is selected in round robin order.
        - 'LEAST_REQUEST': An O(1) algorithm which selects two random healthy
          hosts and picks the host which has fewer active requests.
        - 'RING_HASH': The ring/modulo hash load balancer implements consistent
          hashing to backends. The algorithm has the property that the
          addition/removal of a host from a set of N hosts only affects
          1/N of the requests.
        - 'RANDOM': The load balancer selects a random healthy host.
        - 'ORIGINAL_DESTINATION': Backend host is selected based on the client
          connection metadata, i.e., connections are opened
          to the same address as the destination address of
          the incoming connection before the connection
          was redirected to the load balancer.
        - 'MAGLEV': used as a drop in replacement for the ring hash load balancer.
          Maglev is not as stable as ring hash but has faster table lookup
          build times and host selection times. For more information about
          Maglev, refer to https://ai.google/research/pubs/pub44824
        - 'WEIGHTED_MAGLEV': Per-instance weighted Load Balancing via health check
          reported weights. Only applicable to loadBalancingScheme
          EXTERNAL. If set, the Backend Service must
          configure a non legacy HTTP-based Health Check, and
          health check replies are expected to contain
          non-standard HTTP response header field
          X-Load-Balancing-Endpoint-Weight to specify the
          per-instance weights. If set, Load Balancing is weight
          based on the per-instance weights reported in the last
          processed health check replies, as long as every
          instance either reported a valid weight or had
          UNAVAILABLE_WEIGHT. Otherwise, Load Balancing remains
          equal-weight.
        - 'WEIGHTED_ROUND_ROBIN': Per-endpoint weighted round-robin Load Balancing using weights computed
          from Backend reported Custom Metrics. If set, the Backend Service
          responses are expected to contain non-standard HTTP response header field
          X-Endpoint-Load-Metrics. The reported metrics
          to use for computing the weights are specified via the
          backends[].customMetrics fields.

        locality_lb_policy is applicable to either:

        - A regional backend service with the service_protocol set to HTTP, HTTPS, HTTP2 or H2C,
          and loadBalancingScheme set to INTERNAL_MANAGED.
        - A global backend service with the load_balancing_scheme set to INTERNAL_SELF_MANAGED.
        - A regional backend service with loadBalancingScheme set to EXTERNAL (External Network
          Load Balancing). Only MAGLEV and WEIGHTED_MAGLEV values are possible for External
          Network Load Balancing. The default is MAGLEV.

        If session_affinity is not NONE, and locality_lb_policy is not set to MAGLEV, WEIGHTED_MAGLEV,
        or RING_HASH, session affinity settings will not take effect.

        Only ROUND_ROBIN and RING_HASH are supported when the backend service is referenced
        by a URL map that is bound to target gRPC proxy that has validate_for_proxyless
        field set to true. Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV", "WEIGHTED_MAGLEV", "WEIGHTED_ROUND_ROBIN"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#locality_lb_policy GoogleComputeRegionBackendService#locality_lb_policy}
        '''
        result = self._values.get("locality_lb_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_config(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#log_config GoogleComputeRegionBackendService#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceLogConfig"], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The URL of the network to which this backend service belongs.

        This field can only be specified when the load balancing scheme is set to INTERNAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#network GoogleComputeRegionBackendService#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outlier_detection(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceOutlierDetection"]:
        '''outlier_detection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#outlier_detection GoogleComputeRegionBackendService#outlier_detection}
        '''
        result = self._values.get("outlier_detection")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceOutlierDetection"], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''A named port on a backend instance group representing the port for communication to the backend VMs in that group.

        Required when the
        loadBalancingScheme is EXTERNAL, EXTERNAL_MANAGED, INTERNAL_MANAGED, or INTERNAL_SELF_MANAGED
        and the backends are instance groups. The named port must be defined on each
        backend instance group. This parameter has no meaning if the backends are NEGs. API sets a
        default of "http" if not given.
        Must be omitted when the loadBalancingScheme is INTERNAL (Internal TCP/UDP Load Balancing).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#port_name GoogleComputeRegionBackendService#port_name}
        '''
        result = self._values.get("port_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#project GoogleComputeRegionBackendService#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol this BackendService uses to communicate with backends.

        The default is HTTP. Possible values are HTTP, HTTPS, HTTP2, H2C, TCP, SSL, UDP
        or GRPC. Refer to the documentation for the load balancers or for Traffic Director
        for more information. Possible values: ["HTTP", "HTTPS", "HTTP2", "TCP", "SSL", "UDP", "GRPC", "UNSPECIFIED", "H2C"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#protocol GoogleComputeRegionBackendService#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The Region in which the created backend service should reside. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#region GoogleComputeRegionBackendService#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_policy(self) -> typing.Optional[builtins.str]:
        '''The security policy associated with this backend service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#security_policy GoogleComputeRegionBackendService#security_policy}
        '''
        result = self._values.get("security_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_affinity(self) -> typing.Optional[builtins.str]:
        '''Type of session affinity to use.

        The default is NONE. Session affinity is
        not applicable if the protocol is UDP. Possible values: ["NONE", "CLIENT_IP", "CLIENT_IP_PORT_PROTO", "CLIENT_IP_PROTO", "GENERATED_COOKIE", "HEADER_FIELD", "HTTP_COOKIE", "CLIENT_IP_NO_DESTINATION", "STRONG_COOKIE_AFFINITY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#session_affinity GoogleComputeRegionBackendService#session_affinity}
        '''
        result = self._values.get("session_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strong_session_affinity_cookie(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceStrongSessionAffinityCookie"]:
        '''strong_session_affinity_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#strong_session_affinity_cookie GoogleComputeRegionBackendService#strong_session_affinity_cookie}
        '''
        result = self._values.get("strong_session_affinity_cookie")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceStrongSessionAffinityCookie"], result)

    @builtins.property
    def subsetting(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceSubsetting"]:
        '''subsetting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#subsetting GoogleComputeRegionBackendService#subsetting}
        '''
        result = self._values.get("subsetting")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceSubsetting"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeRegionBackendServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#timeouts GoogleComputeRegionBackendService#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceTimeouts"], result)

    @builtins.property
    def timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''The backend service timeout has a different meaning depending on the type of load balancer.

        For more information see, `Backend service settings <https://cloud.google.com/compute/docs/reference/rest/v1/backendServices>`_.
        The default is 30 seconds.
        The full range of timeout values allowed goes from 1 through 2,147,483,647 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#timeout_sec GoogleComputeRegionBackendService#timeout_sec}
        '''
        result = self._values.get("timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceConnectionTrackingPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "connection_persistence_on_unhealthy_backends": "connectionPersistenceOnUnhealthyBackends",
        "enable_strong_affinity": "enableStrongAffinity",
        "idle_timeout_sec": "idleTimeoutSec",
        "tracking_mode": "trackingMode",
    },
)
class GoogleComputeRegionBackendServiceConnectionTrackingPolicy:
    def __init__(
        self,
        *,
        connection_persistence_on_unhealthy_backends: typing.Optional[builtins.str] = None,
        enable_strong_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        idle_timeout_sec: typing.Optional[jsii.Number] = None,
        tracking_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection_persistence_on_unhealthy_backends: Specifies connection persistence when backends are unhealthy. If set to 'DEFAULT_FOR_PROTOCOL', the existing connections persist on unhealthy backends only for connection-oriented protocols (TCP and SCTP) and only if the Tracking Mode is PER_CONNECTION (default tracking mode) or the Session Affinity is configured for 5-tuple. They do not persist for UDP. If set to 'NEVER_PERSIST', after a backend becomes unhealthy, the existing connections on the unhealthy backend are never persisted on the unhealthy backend. They are always diverted to newly selected healthy backends (unless all backends are unhealthy). If set to 'ALWAYS_PERSIST', existing connections always persist on unhealthy backends regardless of protocol and session affinity. It is generally not recommended to use this mode overriding the default. Default value: "DEFAULT_FOR_PROTOCOL" Possible values: ["DEFAULT_FOR_PROTOCOL", "NEVER_PERSIST", "ALWAYS_PERSIST"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#connection_persistence_on_unhealthy_backends GoogleComputeRegionBackendService#connection_persistence_on_unhealthy_backends}
        :param enable_strong_affinity: Enable Strong Session Affinity for Network Load Balancing. This option is not available publicly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enable_strong_affinity GoogleComputeRegionBackendService#enable_strong_affinity}
        :param idle_timeout_sec: Specifies how long to keep a Connection Tracking entry while there is no matching traffic (in seconds). For L4 ILB the minimum(default) is 10 minutes and maximum is 16 hours. For NLB the minimum(default) is 60 seconds and the maximum is 16 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#idle_timeout_sec GoogleComputeRegionBackendService#idle_timeout_sec}
        :param tracking_mode: Specifies the key used for connection tracking. There are two options: 'PER_CONNECTION': The Connection Tracking is performed as per the Connection Key (default Hash Method) for the specific protocol. 'PER_SESSION': The Connection Tracking is performed as per the configured Session Affinity. It matches the configured Session Affinity. Default value: "PER_CONNECTION" Possible values: ["PER_CONNECTION", "PER_SESSION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#tracking_mode GoogleComputeRegionBackendService#tracking_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186850c287f38b5670c0f949d38a86ba008496cd243c95eb63dfad6a08bfe77b)
            check_type(argname="argument connection_persistence_on_unhealthy_backends", value=connection_persistence_on_unhealthy_backends, expected_type=type_hints["connection_persistence_on_unhealthy_backends"])
            check_type(argname="argument enable_strong_affinity", value=enable_strong_affinity, expected_type=type_hints["enable_strong_affinity"])
            check_type(argname="argument idle_timeout_sec", value=idle_timeout_sec, expected_type=type_hints["idle_timeout_sec"])
            check_type(argname="argument tracking_mode", value=tracking_mode, expected_type=type_hints["tracking_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_persistence_on_unhealthy_backends is not None:
            self._values["connection_persistence_on_unhealthy_backends"] = connection_persistence_on_unhealthy_backends
        if enable_strong_affinity is not None:
            self._values["enable_strong_affinity"] = enable_strong_affinity
        if idle_timeout_sec is not None:
            self._values["idle_timeout_sec"] = idle_timeout_sec
        if tracking_mode is not None:
            self._values["tracking_mode"] = tracking_mode

    @builtins.property
    def connection_persistence_on_unhealthy_backends(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Specifies connection persistence when backends are unhealthy.

        If set to 'DEFAULT_FOR_PROTOCOL', the existing connections persist on
        unhealthy backends only for connection-oriented protocols (TCP and SCTP)
        and only if the Tracking Mode is PER_CONNECTION (default tracking mode)
        or the Session Affinity is configured for 5-tuple. They do not persist
        for UDP.

        If set to 'NEVER_PERSIST', after a backend becomes unhealthy, the existing
        connections on the unhealthy backend are never persisted on the unhealthy
        backend. They are always diverted to newly selected healthy backends
        (unless all backends are unhealthy).

        If set to 'ALWAYS_PERSIST', existing connections always persist on
        unhealthy backends regardless of protocol and session affinity. It is
        generally not recommended to use this mode overriding the default. Default value: "DEFAULT_FOR_PROTOCOL" Possible values: ["DEFAULT_FOR_PROTOCOL", "NEVER_PERSIST", "ALWAYS_PERSIST"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#connection_persistence_on_unhealthy_backends GoogleComputeRegionBackendService#connection_persistence_on_unhealthy_backends}
        '''
        result = self._values.get("connection_persistence_on_unhealthy_backends")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_strong_affinity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Strong Session Affinity for Network Load Balancing. This option is not available publicly.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enable_strong_affinity GoogleComputeRegionBackendService#enable_strong_affinity}
        '''
        result = self._values.get("enable_strong_affinity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def idle_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Specifies how long to keep a Connection Tracking entry while there is no matching traffic (in seconds).

        For L4 ILB the minimum(default) is 10 minutes and maximum is 16 hours.

        For NLB the minimum(default) is 60 seconds and the maximum is 16 hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#idle_timeout_sec GoogleComputeRegionBackendService#idle_timeout_sec}
        '''
        result = self._values.get("idle_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tracking_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the key used for connection tracking.

        There are two options:
        'PER_CONNECTION': The Connection Tracking is performed as per the
        Connection Key (default Hash Method) for the specific protocol.

        'PER_SESSION': The Connection Tracking is performed as per the
        configured Session Affinity. It matches the configured Session Affinity. Default value: "PER_CONNECTION" Possible values: ["PER_CONNECTION", "PER_SESSION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#tracking_mode GoogleComputeRegionBackendService#tracking_mode}
        '''
        result = self._values.get("tracking_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceConnectionTrackingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceConnectionTrackingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceConnectionTrackingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d5d1c9003d7a56a17379a7e909eb90c24c282a07bd604d4879a0aeec1b756ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConnectionPersistenceOnUnhealthyBackends")
    def reset_connection_persistence_on_unhealthy_backends(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionPersistenceOnUnhealthyBackends", []))

    @jsii.member(jsii_name="resetEnableStrongAffinity")
    def reset_enable_strong_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableStrongAffinity", []))

    @jsii.member(jsii_name="resetIdleTimeoutSec")
    def reset_idle_timeout_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleTimeoutSec", []))

    @jsii.member(jsii_name="resetTrackingMode")
    def reset_tracking_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrackingMode", []))

    @builtins.property
    @jsii.member(jsii_name="connectionPersistenceOnUnhealthyBackendsInput")
    def connection_persistence_on_unhealthy_backends_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionPersistenceOnUnhealthyBackendsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableStrongAffinityInput")
    def enable_strong_affinity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableStrongAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutSecInput")
    def idle_timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleTimeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="trackingModeInput")
    def tracking_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trackingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionPersistenceOnUnhealthyBackends")
    def connection_persistence_on_unhealthy_backends(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionPersistenceOnUnhealthyBackends"))

    @connection_persistence_on_unhealthy_backends.setter
    def connection_persistence_on_unhealthy_backends(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec8c518fbe9613134ae6b426cd460cb9fc94c64eeada7504946c88c9cfe6e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionPersistenceOnUnhealthyBackends", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableStrongAffinity")
    def enable_strong_affinity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableStrongAffinity"))

    @enable_strong_affinity.setter
    def enable_strong_affinity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be4f49fb30d1efd7a5e9c233071bec658c7e30376cd7350fa5febb6d2a9e1ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStrongAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutSec")
    def idle_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "idleTimeoutSec"))

    @idle_timeout_sec.setter
    def idle_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963c59ae89f11bac0d9f1c5cc20dadfc353111b9ae2a2b889142bf5654683a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trackingMode")
    def tracking_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trackingMode"))

    @tracking_mode.setter
    def tracking_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f0f8673cbfe57faaa19c1d1375d534372d930c608e288454916848565c686c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceConnectionTrackingPolicy]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceConnectionTrackingPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceConnectionTrackingPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c66ea8e970ce634d831c0bb6799114f020fca6fab6accf6ec76ac0e4129cd67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceConsistentHash",
    jsii_struct_bases=[],
    name_mapping={
        "http_cookie": "httpCookie",
        "http_header_name": "httpHeaderName",
        "minimum_ring_size": "minimumRingSize",
    },
)
class GoogleComputeRegionBackendServiceConsistentHash:
    def __init__(
        self,
        *,
        http_cookie: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceConsistentHashHttpCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        http_header_name: typing.Optional[builtins.str] = None,
        minimum_ring_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_cookie: http_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#http_cookie GoogleComputeRegionBackendService#http_cookie}
        :param http_header_name: The hash based on the value of the specified header field. This field is applicable if the sessionAffinity is set to HEADER_FIELD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#http_header_name GoogleComputeRegionBackendService#http_header_name}
        :param minimum_ring_size: The minimum number of virtual nodes to use for the hash ring. Larger ring sizes result in more granular load distributions. If the number of hosts in the load balancing pool is larger than the ring size, each host will be assigned a single virtual node. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#minimum_ring_size GoogleComputeRegionBackendService#minimum_ring_size}
        '''
        if isinstance(http_cookie, dict):
            http_cookie = GoogleComputeRegionBackendServiceConsistentHashHttpCookie(**http_cookie)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a05c015bd6fcc92648de303fdd634b305576421e1aacd3393022ba04a44a70d4)
            check_type(argname="argument http_cookie", value=http_cookie, expected_type=type_hints["http_cookie"])
            check_type(argname="argument http_header_name", value=http_header_name, expected_type=type_hints["http_header_name"])
            check_type(argname="argument minimum_ring_size", value=minimum_ring_size, expected_type=type_hints["minimum_ring_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_cookie is not None:
            self._values["http_cookie"] = http_cookie
        if http_header_name is not None:
            self._values["http_header_name"] = http_header_name
        if minimum_ring_size is not None:
            self._values["minimum_ring_size"] = minimum_ring_size

    @builtins.property
    def http_cookie(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceConsistentHashHttpCookie"]:
        '''http_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#http_cookie GoogleComputeRegionBackendService#http_cookie}
        '''
        result = self._values.get("http_cookie")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceConsistentHashHttpCookie"], result)

    @builtins.property
    def http_header_name(self) -> typing.Optional[builtins.str]:
        '''The hash based on the value of the specified header field.

        This field is applicable if the sessionAffinity is set to HEADER_FIELD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#http_header_name GoogleComputeRegionBackendService#http_header_name}
        '''
        result = self._values.get("http_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_ring_size(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of virtual nodes to use for the hash ring.

        Larger ring sizes result in more granular load
        distributions. If the number of hosts in the load balancing pool
        is larger than the ring size, each host will be assigned a single
        virtual node.
        Defaults to 1024.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#minimum_ring_size GoogleComputeRegionBackendService#minimum_ring_size}
        '''
        result = self._values.get("minimum_ring_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceConsistentHash(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceConsistentHashHttpCookie",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "ttl": "ttl"},
)
class GoogleComputeRegionBackendServiceConsistentHashHttpCookie:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#name GoogleComputeRegionBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#path GoogleComputeRegionBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ttl GoogleComputeRegionBackendService#ttl}
        '''
        if isinstance(ttl, dict):
            ttl = GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl(**ttl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1111f2fedc5e8349f60587f91ba9cd6047b501e76b7afe8facb9474b431d20)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if path is not None:
            self._values["path"] = path
        if ttl is not None:
            self._values["ttl"] = ttl

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the cookie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#name GoogleComputeRegionBackendService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to set for the cookie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#path GoogleComputeRegionBackendService#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl"]:
        '''ttl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ttl GoogleComputeRegionBackendService#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceConsistentHashHttpCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceConsistentHashHttpCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceConsistentHashHttpCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f83da1285925badf3e455064abeedf73fa263f3d790041d8b018441b67238db7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTtl")
    def put_ttl(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        value = GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl(
            seconds=seconds, nanos=nanos
        )

        return typing.cast(None, jsii.invoke(self, "putTtl", [value]))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(
        self,
    ) -> "GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtlOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtlOutputReference", jsii.get(self, "ttl"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl"]:
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl"], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe347293601a4214e4a3411d27beecca37d9a301be3bc5ff0576dc511ff471a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679904b30d2ad284fc2ebe4f5a30138380be90b8ab79b81e576ae0ceb75edca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceConsistentHashHttpCookie]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceConsistentHashHttpCookie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceConsistentHashHttpCookie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2c1b61ca8bbf89f4aa913bd2088d30b92ea4b2ca64e3d900be9f4accff3617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac4a015ce0a8ad48fd7d1419b10bd987cc5e350d23556a2afb67b52a097f0d71)
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "seconds": seconds,
        }
        if nanos is not None:
            self._values["nanos"] = nanos

    @builtins.property
    def seconds(self) -> jsii.Number:
        '''Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        '''
        result = self._values.get("seconds")
        assert result is not None, "Required property 'seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Span of time that's a fraction of a second at nanosecond resolution.

        Durations less than one second are represented
        with a 0 seconds field and a positive nanos field. Must
        be from 0 to 999,999,999 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f7fb9512799f035be88456dc6ac598a72081506d2bb4ee3fec95c86a9d74045)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f174878baa8f957103347a5d49f28166b176927a09281c9151f08a08a6aae75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2757511df94ac3d8c6b0cf623b42f12d5d098fd0698ac055965be33e9414ba2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2769149c28dfac0fbac939dd045ce5905114ca85449b0adab35bfa75348a448d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionBackendServiceConsistentHashOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceConsistentHashOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b4898e8db26c2f881fbbfa6fa2be8e91571521b0bb35f38bc5cf224883feefa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpCookie")
    def put_http_cookie(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#name GoogleComputeRegionBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#path GoogleComputeRegionBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ttl GoogleComputeRegionBackendService#ttl}
        '''
        value = GoogleComputeRegionBackendServiceConsistentHashHttpCookie(
            name=name, path=path, ttl=ttl
        )

        return typing.cast(None, jsii.invoke(self, "putHttpCookie", [value]))

    @jsii.member(jsii_name="resetHttpCookie")
    def reset_http_cookie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCookie", []))

    @jsii.member(jsii_name="resetHttpHeaderName")
    def reset_http_header_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeaderName", []))

    @jsii.member(jsii_name="resetMinimumRingSize")
    def reset_minimum_ring_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumRingSize", []))

    @builtins.property
    @jsii.member(jsii_name="httpCookie")
    def http_cookie(
        self,
    ) -> GoogleComputeRegionBackendServiceConsistentHashHttpCookieOutputReference:
        return typing.cast(GoogleComputeRegionBackendServiceConsistentHashHttpCookieOutputReference, jsii.get(self, "httpCookie"))

    @builtins.property
    @jsii.member(jsii_name="httpCookieInput")
    def http_cookie_input(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceConsistentHashHttpCookie]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceConsistentHashHttpCookie], jsii.get(self, "httpCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeaderNameInput")
    def http_header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumRingSizeInput")
    def minimum_ring_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumRingSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeaderName")
    def http_header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpHeaderName"))

    @http_header_name.setter
    def http_header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15d2387caa5ef93fe26a11cae0f7c36e1e7be3186cc4a938b5473ad14e6455f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumRingSize")
    def minimum_ring_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumRingSize"))

    @minimum_ring_size.setter
    def minimum_ring_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3dce71a3a04d2b2bb9426d4cc8b11e408506f33ba76920075d4ddbf77623c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumRingSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceConsistentHash]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceConsistentHash], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceConsistentHash],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac254ff911892f1e4c4d9aa274ff57c1fd014a658b668a269227502fa188430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCustomMetrics",
    jsii_struct_bases=[],
    name_mapping={"dry_run": "dryRun", "name": "name"},
)
class GoogleComputeRegionBackendServiceCustomMetrics:
    def __init__(
        self,
        *,
        dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
    ) -> None:
        '''
        :param dry_run: If true, the metric data is not used for load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#dry_run GoogleComputeRegionBackendService#dry_run}
        :param name: Name of a custom utilization signal. The name must be 1-64 characters long and match the regular expression `a-z <%5B-_.a-z0-9%5D*%5Ba-z0-9%5D>`_? which means the first character must be a lowercase letter, and all following characters must be a dash, period, underscore, lowercase letter, or digit, except the last character, which cannot be a dash, period, or underscore. For usage guidelines, see Custom Metrics balancing mode. This field can only be used for a global or regional backend service with the loadBalancingScheme set to EXTERNAL_MANAGED, INTERNAL_MANAGED INTERNAL_SELF_MANAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#name GoogleComputeRegionBackendService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e95fc8f422a037d9378ce45a126e9b63a6e815b68aacc5f4fe99300a6bb9d8)
            check_type(argname="argument dry_run", value=dry_run, expected_type=type_hints["dry_run"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dry_run": dry_run,
            "name": name,
        }

    @builtins.property
    def dry_run(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, the metric data is not used for load balancing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#dry_run GoogleComputeRegionBackendService#dry_run}
        '''
        result = self._values.get("dry_run")
        assert result is not None, "Required property 'dry_run' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of a custom utilization signal.

        The name must be 1-64 characters
        long and match the regular expression `a-z <%5B-_.a-z0-9%5D*%5Ba-z0-9%5D>`_? which
        means the first character must be a lowercase letter, and all following
        characters must be a dash, period, underscore, lowercase letter, or
        digit, except the last character, which cannot be a dash, period, or
        underscore. For usage guidelines, see Custom Metrics balancing mode. This
        field can only be used for a global or regional backend service with the
        loadBalancingScheme set to EXTERNAL_MANAGED,
        INTERNAL_MANAGED INTERNAL_SELF_MANAGED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#name GoogleComputeRegionBackendService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceCustomMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceCustomMetricsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCustomMetricsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e0925527a984174502f9f295ab6c1bf67dcce7305a67ad735d839232baf429f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRegionBackendServiceCustomMetricsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb99a428c438e04063339e94d7c3689b4f95ad8410609eaee452ba9ec0de5e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRegionBackendServiceCustomMetricsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9908db6338b9852b94934c28cee130bcc7fc92b38d4b0d96c6c2059b396beb2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ec596cef20c9bd60e07aacd4594e156d592409de83a811f8508a648b86aa1b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__559e5695183c03bc5c96ca402df532c50de3aaf61dc7b4f74d6af1c1cabac9cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceCustomMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceCustomMetrics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceCustomMetrics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84513dee6fbce06ec4829b81fdede85958b0020ea564ea7e3b309ded3eee26f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionBackendServiceCustomMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceCustomMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b31e68c7be5bd6e300cd802f5028727134c5246323aa976d9b8d7e1a13e234d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dryRunInput")
    def dry_run_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dryRunInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="dryRun")
    def dry_run(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dryRun"))

    @dry_run.setter
    def dry_run(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d835e33de227b7b3be8ce1810518968cd2b4cb6352dd91e19cba314b6fd3afa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dryRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1297b906e3d31c8b62b7014c2289b22cae9201850bc1076bb49d38d1feeef3b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceCustomMetrics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceCustomMetrics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceCustomMetrics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f8ba8bb823b3f1fce1de1a96a2a26e9dd61c40b5123903d4709130c0bf697e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceDynamicForwarding",
    jsii_struct_bases=[],
    name_mapping={"ip_port_selection": "ipPortSelection"},
)
class GoogleComputeRegionBackendServiceDynamicForwarding:
    def __init__(
        self,
        *,
        ip_port_selection: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ip_port_selection: ip_port_selection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ip_port_selection GoogleComputeRegionBackendService#ip_port_selection}
        '''
        if isinstance(ip_port_selection, dict):
            ip_port_selection = GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection(**ip_port_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eaef17e15382260e6f9082ba9c78aff777bad52e8291d11941554f6a3abbff0)
            check_type(argname="argument ip_port_selection", value=ip_port_selection, expected_type=type_hints["ip_port_selection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ip_port_selection is not None:
            self._values["ip_port_selection"] = ip_port_selection

    @builtins.property
    def ip_port_selection(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection"]:
        '''ip_port_selection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ip_port_selection GoogleComputeRegionBackendService#ip_port_selection}
        '''
        result = self._values.get("ip_port_selection")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceDynamicForwarding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: A boolean flag enabling IP:PORT based dynamic forwarding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enabled GoogleComputeRegionBackendService#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a67cd95b0bbff7c1faac034872621716cc1d9891f216bc3faea09f664f81a65d)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean flag enabling IP:PORT based dynamic forwarding.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enabled GoogleComputeRegionBackendService#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6972b36613f1c40b50ef6da7b2b899a03a06933576c0283bcfd440126c54db7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c04761ea6ab0fd8ef4324f0d150954efceb3d9d861fb73b95f1bdb146132cfb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b190703618a76c5081214b896b0471788e44f5e655ecc1aa94350d6bc35aec07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionBackendServiceDynamicForwardingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceDynamicForwardingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22fb5472514720f7f28b4f2e95071cdbf903bdf0ca0fe2541183ebe9da1162a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpPortSelection")
    def put_ip_port_selection(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: A boolean flag enabling IP:PORT based dynamic forwarding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enabled GoogleComputeRegionBackendService#enabled}
        '''
        value = GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putIpPortSelection", [value]))

    @jsii.member(jsii_name="resetIpPortSelection")
    def reset_ip_port_selection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpPortSelection", []))

    @builtins.property
    @jsii.member(jsii_name="ipPortSelection")
    def ip_port_selection(
        self,
    ) -> GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelectionOutputReference:
        return typing.cast(GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelectionOutputReference, jsii.get(self, "ipPortSelection"))

    @builtins.property
    @jsii.member(jsii_name="ipPortSelectionInput")
    def ip_port_selection_input(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection], jsii.get(self, "ipPortSelectionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceDynamicForwarding]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceDynamicForwarding], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceDynamicForwarding],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fed537b8e13eb4905f95b4e56c88695800336328a191b502e5346f5d7754b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceFailoverPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "disable_connection_drain_on_failover": "disableConnectionDrainOnFailover",
        "drop_traffic_if_unhealthy": "dropTrafficIfUnhealthy",
        "failover_ratio": "failoverRatio",
    },
)
class GoogleComputeRegionBackendServiceFailoverPolicy:
    def __init__(
        self,
        *,
        disable_connection_drain_on_failover: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_traffic_if_unhealthy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failover_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disable_connection_drain_on_failover: On failover or failback, this field indicates whether connection drain will be honored. Setting this to true has the following effect: connections to the old active pool are not drained. Connections to the new active pool use the timeout of 10 min (currently fixed). Setting to false has the following effect: both old and new connections will have a drain timeout of 10 min. This can be set to true only if the protocol is TCP. The default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#disable_connection_drain_on_failover GoogleComputeRegionBackendService#disable_connection_drain_on_failover}
        :param drop_traffic_if_unhealthy: This option is used only when no healthy VMs are detected in the primary and backup instance groups. When set to true, traffic is dropped. When set to false, new connections are sent across all VMs in the primary group. The default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#drop_traffic_if_unhealthy GoogleComputeRegionBackendService#drop_traffic_if_unhealthy}
        :param failover_ratio: The value of the field must be in [0, 1]. If the ratio of the healthy VMs in the primary backend is at or below this number, traffic arriving at the load-balanced IP will be directed to the failover backend. In case where 'failoverRatio' is not set or all the VMs in the backup backend are unhealthy, the traffic will be directed back to the primary backend in the "force" mode, where traffic will be spread to the healthy VMs with the best effort, or to all VMs when no VM is healthy. This field is only used with l4 load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#failover_ratio GoogleComputeRegionBackendService#failover_ratio}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b8c9dc333fae7e990487ee1a726804babe31df145270d86dad471f2d85875e0)
            check_type(argname="argument disable_connection_drain_on_failover", value=disable_connection_drain_on_failover, expected_type=type_hints["disable_connection_drain_on_failover"])
            check_type(argname="argument drop_traffic_if_unhealthy", value=drop_traffic_if_unhealthy, expected_type=type_hints["drop_traffic_if_unhealthy"])
            check_type(argname="argument failover_ratio", value=failover_ratio, expected_type=type_hints["failover_ratio"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_connection_drain_on_failover is not None:
            self._values["disable_connection_drain_on_failover"] = disable_connection_drain_on_failover
        if drop_traffic_if_unhealthy is not None:
            self._values["drop_traffic_if_unhealthy"] = drop_traffic_if_unhealthy
        if failover_ratio is not None:
            self._values["failover_ratio"] = failover_ratio

    @builtins.property
    def disable_connection_drain_on_failover(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''On failover or failback, this field indicates whether connection drain will be honored.

        Setting this to true has the following effect: connections
        to the old active pool are not drained. Connections to the new active pool
        use the timeout of 10 min (currently fixed). Setting to false has the
        following effect: both old and new connections will have a drain timeout
        of 10 min.
        This can be set to true only if the protocol is TCP.
        The default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#disable_connection_drain_on_failover GoogleComputeRegionBackendService#disable_connection_drain_on_failover}
        '''
        result = self._values.get("disable_connection_drain_on_failover")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drop_traffic_if_unhealthy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This option is used only when no healthy VMs are detected in the primary and backup instance groups.

        When set to true, traffic is dropped. When
        set to false, new connections are sent across all VMs in the primary group.
        The default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#drop_traffic_if_unhealthy GoogleComputeRegionBackendService#drop_traffic_if_unhealthy}
        '''
        result = self._values.get("drop_traffic_if_unhealthy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def failover_ratio(self) -> typing.Optional[jsii.Number]:
        '''The value of the field must be in [0, 1].

        If the ratio of the healthy
        VMs in the primary backend is at or below this number, traffic arriving
        at the load-balanced IP will be directed to the failover backend.
        In case where 'failoverRatio' is not set or all the VMs in the backup
        backend are unhealthy, the traffic will be directed back to the primary
        backend in the "force" mode, where traffic will be spread to the healthy
        VMs with the best effort, or to all VMs when no VM is healthy.
        This field is only used with l4 load balancing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#failover_ratio GoogleComputeRegionBackendService#failover_ratio}
        '''
        result = self._values.get("failover_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceFailoverPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceFailoverPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceFailoverPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2e1ff00edd371c637c7c14bfe198364f46f90bddf2a110a3d3383248f523a4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisableConnectionDrainOnFailover")
    def reset_disable_connection_drain_on_failover(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableConnectionDrainOnFailover", []))

    @jsii.member(jsii_name="resetDropTrafficIfUnhealthy")
    def reset_drop_traffic_if_unhealthy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropTrafficIfUnhealthy", []))

    @jsii.member(jsii_name="resetFailoverRatio")
    def reset_failover_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailoverRatio", []))

    @builtins.property
    @jsii.member(jsii_name="disableConnectionDrainOnFailoverInput")
    def disable_connection_drain_on_failover_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableConnectionDrainOnFailoverInput"))

    @builtins.property
    @jsii.member(jsii_name="dropTrafficIfUnhealthyInput")
    def drop_traffic_if_unhealthy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropTrafficIfUnhealthyInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverRatioInput")
    def failover_ratio_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failoverRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="disableConnectionDrainOnFailover")
    def disable_connection_drain_on_failover(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableConnectionDrainOnFailover"))

    @disable_connection_drain_on_failover.setter
    def disable_connection_drain_on_failover(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10c2654404b4600accae7a699f8c449d32098f17dc5fc967f96e5fe44d15902e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableConnectionDrainOnFailover", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dropTrafficIfUnhealthy")
    def drop_traffic_if_unhealthy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropTrafficIfUnhealthy"))

    @drop_traffic_if_unhealthy.setter
    def drop_traffic_if_unhealthy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ad0939143e5e01edcdadfb1c4b6679040295d822973dfdc4b470e608c76429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropTrafficIfUnhealthy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failoverRatio")
    def failover_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failoverRatio"))

    @failover_ratio.setter
    def failover_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e1be36edf39f334609c01e9edea83f6aa55fa50f44221b1592fd7217be72de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceFailoverPolicy]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceFailoverPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceFailoverPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57970fb46a212dd310af7a2b1d7c356f62aae853d6d24ff41473cfa985fb068a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceIap",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "oauth2_client_id": "oauth2ClientId",
        "oauth2_client_secret": "oauth2ClientSecret",
    },
)
class GoogleComputeRegionBackendServiceIap:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        oauth2_client_id: typing.Optional[builtins.str] = None,
        oauth2_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether the serving infrastructure will authenticate and authorize all incoming requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enabled GoogleComputeRegionBackendService#enabled}
        :param oauth2_client_id: OAuth2 Client ID for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#oauth2_client_id GoogleComputeRegionBackendService#oauth2_client_id}
        :param oauth2_client_secret: OAuth2 Client Secret for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#oauth2_client_secret GoogleComputeRegionBackendService#oauth2_client_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f300bb090f2cb7740ab2055d393eadabff0c250ffc86a426e0210c8725dd088c)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument oauth2_client_id", value=oauth2_client_id, expected_type=type_hints["oauth2_client_id"])
            check_type(argname="argument oauth2_client_secret", value=oauth2_client_secret, expected_type=type_hints["oauth2_client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if oauth2_client_id is not None:
            self._values["oauth2_client_id"] = oauth2_client_id
        if oauth2_client_secret is not None:
            self._values["oauth2_client_secret"] = oauth2_client_secret

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the serving infrastructure will authenticate and authorize all incoming requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enabled GoogleComputeRegionBackendService#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def oauth2_client_id(self) -> typing.Optional[builtins.str]:
        '''OAuth2 Client ID for IAP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#oauth2_client_id GoogleComputeRegionBackendService#oauth2_client_id}
        '''
        result = self._values.get("oauth2_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth2_client_secret(self) -> typing.Optional[builtins.str]:
        '''OAuth2 Client Secret for IAP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#oauth2_client_secret GoogleComputeRegionBackendService#oauth2_client_secret}
        '''
        result = self._values.get("oauth2_client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceIap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceIapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceIapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a61fac610bde6fe213bfab52fcdb66efdd6cc4784e8be8d12cfa2d36c82aab9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOauth2ClientId")
    def reset_oauth2_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2ClientId", []))

    @jsii.member(jsii_name="resetOauth2ClientSecret")
    def reset_oauth2_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2ClientSecret", []))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientSecretSha256")
    def oauth2_client_secret_sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2ClientSecretSha256"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientIdInput")
    def oauth2_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauth2ClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientSecretInput")
    def oauth2_client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauth2ClientSecretInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d2de6196fd0ea1b41fc2ed19a4cfcffd3db2093407cc2404a238762860597c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientId")
    def oauth2_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2ClientId"))

    @oauth2_client_id.setter
    def oauth2_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567954f723c342344563217e38d1a6df2467b97163784177beabb2592f4e439c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2ClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientSecret")
    def oauth2_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2ClientSecret"))

    @oauth2_client_secret.setter
    def oauth2_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e846fc569a993869720c32d582b86ee42bc1404b9baca130983bf664fa99049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2ClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeRegionBackendServiceIap]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceIap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceIap],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5074bb02ba714f8038d6ffd09841d75df56c6479b3b2ebcf60ab295964b6dd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceLogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable": "enable",
        "optional_fields": "optionalFields",
        "optional_mode": "optionalMode",
        "sample_rate": "sampleRate",
    },
)
class GoogleComputeRegionBackendServiceLogConfig:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        optional_mode: typing.Optional[builtins.str] = None,
        sample_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable: Whether to enable logging for the load balancer traffic served by this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enable GoogleComputeRegionBackendService#enable}
        :param optional_fields: Specifies the fields to include in logging. This field can only be specified if logging is enabled for this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#optional_fields GoogleComputeRegionBackendService#optional_fields}
        :param optional_mode: Specifies the optional logging mode for the load balancer traffic. Supported values: INCLUDE_ALL_OPTIONAL, EXCLUDE_ALL_OPTIONAL, CUSTOM. Possible values: ["INCLUDE_ALL_OPTIONAL", "EXCLUDE_ALL_OPTIONAL", "CUSTOM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#optional_mode GoogleComputeRegionBackendService#optional_mode}
        :param sample_rate: This field can only be specified if logging is enabled for this backend service. The value of the field must be in [0, 1]. This configures the sampling rate of requests to the load balancer where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#sample_rate GoogleComputeRegionBackendService#sample_rate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c70034f84c1e3507374074f498b2edfb8571d89f9c3c721522559ad70e199032)
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument optional_fields", value=optional_fields, expected_type=type_hints["optional_fields"])
            check_type(argname="argument optional_mode", value=optional_mode, expected_type=type_hints["optional_mode"])
            check_type(argname="argument sample_rate", value=sample_rate, expected_type=type_hints["sample_rate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable is not None:
            self._values["enable"] = enable
        if optional_fields is not None:
            self._values["optional_fields"] = optional_fields
        if optional_mode is not None:
            self._values["optional_mode"] = optional_mode
        if sample_rate is not None:
            self._values["sample_rate"] = sample_rate

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable logging for the load balancer traffic served by this backend service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enable GoogleComputeRegionBackendService#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def optional_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the fields to include in logging.

        This field can only be specified if logging is enabled for this backend service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#optional_fields GoogleComputeRegionBackendService#optional_fields}
        '''
        result = self._values.get("optional_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def optional_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the optional logging mode for the load balancer traffic. Supported values: INCLUDE_ALL_OPTIONAL, EXCLUDE_ALL_OPTIONAL, CUSTOM. Possible values: ["INCLUDE_ALL_OPTIONAL", "EXCLUDE_ALL_OPTIONAL", "CUSTOM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#optional_mode GoogleComputeRegionBackendService#optional_mode}
        '''
        result = self._values.get("optional_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_rate(self) -> typing.Optional[jsii.Number]:
        '''This field can only be specified if logging is enabled for this backend service.

        The value of
        the field must be in [0, 1]. This configures the sampling rate of requests to the load balancer
        where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported.
        The default value is 1.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#sample_rate GoogleComputeRegionBackendService#sample_rate}
        '''
        result = self._values.get("sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0ad3a4760c2dcf98312f2b828502e243144ef06d743cba94ee78a2f2e290be8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnable")
    def reset_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnable", []))

    @jsii.member(jsii_name="resetOptionalFields")
    def reset_optional_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptionalFields", []))

    @jsii.member(jsii_name="resetOptionalMode")
    def reset_optional_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptionalMode", []))

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
    @jsii.member(jsii_name="optionalFieldsInput")
    def optional_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "optionalFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalModeInput")
    def optional_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "optionalModeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__18d7096dae4e686629680ddd40d5342420aa196ca5a91482f083b20d29e1bb3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optionalFields")
    def optional_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "optionalFields"))

    @optional_fields.setter
    def optional_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d099e44f7b1851073d1c68a2c8cee6268d2489fd001a64255a9fdc635ade759e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionalFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optionalMode")
    def optional_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "optionalMode"))

    @optional_mode.setter
    def optional_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba17e114adadff0b1eae8253563e19c1628a75ae7fa4625298794f3e624ccad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionalMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRate")
    def sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRate"))

    @sample_rate.setter
    def sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318c82500340a14e6a41d6f813aa66aea76eebdacec338221c54733752467523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceLogConfig]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e49042912a863761ecbddb9f6cab7bcdef4a082794d7266b018899dc94ef01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceOutlierDetection",
    jsii_struct_bases=[],
    name_mapping={
        "base_ejection_time": "baseEjectionTime",
        "consecutive_errors": "consecutiveErrors",
        "consecutive_gateway_failure": "consecutiveGatewayFailure",
        "enforcing_consecutive_errors": "enforcingConsecutiveErrors",
        "enforcing_consecutive_gateway_failure": "enforcingConsecutiveGatewayFailure",
        "enforcing_success_rate": "enforcingSuccessRate",
        "interval": "interval",
        "max_ejection_percent": "maxEjectionPercent",
        "success_rate_minimum_hosts": "successRateMinimumHosts",
        "success_rate_request_volume": "successRateRequestVolume",
        "success_rate_stdev_factor": "successRateStdevFactor",
    },
)
class GoogleComputeRegionBackendServiceOutlierDetection:
    def __init__(
        self,
        *,
        base_ejection_time: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime", typing.Dict[builtins.str, typing.Any]]] = None,
        consecutive_errors: typing.Optional[jsii.Number] = None,
        consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_errors: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_success_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceOutlierDetectionInterval", typing.Dict[builtins.str, typing.Any]]] = None,
        max_ejection_percent: typing.Optional[jsii.Number] = None,
        success_rate_minimum_hosts: typing.Optional[jsii.Number] = None,
        success_rate_request_volume: typing.Optional[jsii.Number] = None,
        success_rate_stdev_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param base_ejection_time: base_ejection_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#base_ejection_time GoogleComputeRegionBackendService#base_ejection_time}
        :param consecutive_errors: Number of errors before a host is ejected from the connection pool. When the backend host is accessed over HTTP, a 5xx return code qualifies as an error. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#consecutive_errors GoogleComputeRegionBackendService#consecutive_errors}
        :param consecutive_gateway_failure: The number of consecutive gateway failures (502, 503, 504 status or connection errors that are mapped to one of those status codes) before a consecutive gateway failure ejection occurs. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#consecutive_gateway_failure GoogleComputeRegionBackendService#consecutive_gateway_failure}
        :param enforcing_consecutive_errors: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive 5xx. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enforcing_consecutive_errors GoogleComputeRegionBackendService#enforcing_consecutive_errors}
        :param enforcing_consecutive_gateway_failure: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive gateway failures. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enforcing_consecutive_gateway_failure GoogleComputeRegionBackendService#enforcing_consecutive_gateway_failure}
        :param enforcing_success_rate: The percentage chance that a host will be actually ejected when an outlier status is detected through success rate statistics. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enforcing_success_rate GoogleComputeRegionBackendService#enforcing_success_rate}
        :param interval: interval block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#interval GoogleComputeRegionBackendService#interval}
        :param max_ejection_percent: Maximum percentage of hosts in the load balancing pool for the backend service that can be ejected. Defaults to 10%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_ejection_percent GoogleComputeRegionBackendService#max_ejection_percent}
        :param success_rate_minimum_hosts: The number of hosts in a cluster that must have enough request volume to detect success rate outliers. If the number of hosts is less than this setting, outlier detection via success rate statistics is not performed for any host in the cluster. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#success_rate_minimum_hosts GoogleComputeRegionBackendService#success_rate_minimum_hosts}
        :param success_rate_request_volume: The minimum number of total requests that must be collected in one interval (as defined by the interval duration above) to include this host in success rate based outlier detection. If the volume is lower than this setting, outlier detection via success rate statistics is not performed for that host. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#success_rate_request_volume GoogleComputeRegionBackendService#success_rate_request_volume}
        :param success_rate_stdev_factor: This factor is used to determine the ejection threshold for success rate outlier ejection. The ejection threshold is the difference between the mean success rate, and the product of this factor and the standard deviation of the mean success rate: mean - (stdev * success_rate_stdev_factor). This factor is divided by a thousand to get a double. That is, if the desired factor is 1.9, the runtime value should be 1900. Defaults to 1900. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#success_rate_stdev_factor GoogleComputeRegionBackendService#success_rate_stdev_factor}
        '''
        if isinstance(base_ejection_time, dict):
            base_ejection_time = GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime(**base_ejection_time)
        if isinstance(interval, dict):
            interval = GoogleComputeRegionBackendServiceOutlierDetectionInterval(**interval)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba2c3aa66fa2e50d62d5ebd9180f503ed706df3dd6e9dcb9ab96fa338cc3af0)
            check_type(argname="argument base_ejection_time", value=base_ejection_time, expected_type=type_hints["base_ejection_time"])
            check_type(argname="argument consecutive_errors", value=consecutive_errors, expected_type=type_hints["consecutive_errors"])
            check_type(argname="argument consecutive_gateway_failure", value=consecutive_gateway_failure, expected_type=type_hints["consecutive_gateway_failure"])
            check_type(argname="argument enforcing_consecutive_errors", value=enforcing_consecutive_errors, expected_type=type_hints["enforcing_consecutive_errors"])
            check_type(argname="argument enforcing_consecutive_gateway_failure", value=enforcing_consecutive_gateway_failure, expected_type=type_hints["enforcing_consecutive_gateway_failure"])
            check_type(argname="argument enforcing_success_rate", value=enforcing_success_rate, expected_type=type_hints["enforcing_success_rate"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument max_ejection_percent", value=max_ejection_percent, expected_type=type_hints["max_ejection_percent"])
            check_type(argname="argument success_rate_minimum_hosts", value=success_rate_minimum_hosts, expected_type=type_hints["success_rate_minimum_hosts"])
            check_type(argname="argument success_rate_request_volume", value=success_rate_request_volume, expected_type=type_hints["success_rate_request_volume"])
            check_type(argname="argument success_rate_stdev_factor", value=success_rate_stdev_factor, expected_type=type_hints["success_rate_stdev_factor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base_ejection_time is not None:
            self._values["base_ejection_time"] = base_ejection_time
        if consecutive_errors is not None:
            self._values["consecutive_errors"] = consecutive_errors
        if consecutive_gateway_failure is not None:
            self._values["consecutive_gateway_failure"] = consecutive_gateway_failure
        if enforcing_consecutive_errors is not None:
            self._values["enforcing_consecutive_errors"] = enforcing_consecutive_errors
        if enforcing_consecutive_gateway_failure is not None:
            self._values["enforcing_consecutive_gateway_failure"] = enforcing_consecutive_gateway_failure
        if enforcing_success_rate is not None:
            self._values["enforcing_success_rate"] = enforcing_success_rate
        if interval is not None:
            self._values["interval"] = interval
        if max_ejection_percent is not None:
            self._values["max_ejection_percent"] = max_ejection_percent
        if success_rate_minimum_hosts is not None:
            self._values["success_rate_minimum_hosts"] = success_rate_minimum_hosts
        if success_rate_request_volume is not None:
            self._values["success_rate_request_volume"] = success_rate_request_volume
        if success_rate_stdev_factor is not None:
            self._values["success_rate_stdev_factor"] = success_rate_stdev_factor

    @builtins.property
    def base_ejection_time(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime"]:
        '''base_ejection_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#base_ejection_time GoogleComputeRegionBackendService#base_ejection_time}
        '''
        result = self._values.get("base_ejection_time")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime"], result)

    @builtins.property
    def consecutive_errors(self) -> typing.Optional[jsii.Number]:
        '''Number of errors before a host is ejected from the connection pool.

        When the
        backend host is accessed over HTTP, a 5xx return code qualifies as an error.
        Defaults to 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#consecutive_errors GoogleComputeRegionBackendService#consecutive_errors}
        '''
        result = self._values.get("consecutive_errors")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def consecutive_gateway_failure(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive gateway failures (502, 503, 504 status or connection errors that are mapped to one of those status codes) before a consecutive gateway failure ejection occurs.

        Defaults to 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#consecutive_gateway_failure GoogleComputeRegionBackendService#consecutive_gateway_failure}
        '''
        result = self._values.get("consecutive_gateway_failure")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enforcing_consecutive_errors(self) -> typing.Optional[jsii.Number]:
        '''The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive 5xx.

        This setting can be used to disable
        ejection or to ramp it up slowly. Defaults to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enforcing_consecutive_errors GoogleComputeRegionBackendService#enforcing_consecutive_errors}
        '''
        result = self._values.get("enforcing_consecutive_errors")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enforcing_consecutive_gateway_failure(self) -> typing.Optional[jsii.Number]:
        '''The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive gateway failures.

        This setting can be
        used to disable ejection or to ramp it up slowly. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enforcing_consecutive_gateway_failure GoogleComputeRegionBackendService#enforcing_consecutive_gateway_failure}
        '''
        result = self._values.get("enforcing_consecutive_gateway_failure")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enforcing_success_rate(self) -> typing.Optional[jsii.Number]:
        '''The percentage chance that a host will be actually ejected when an outlier status is detected through success rate statistics.

        This setting can be used to
        disable ejection or to ramp it up slowly. Defaults to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#enforcing_success_rate GoogleComputeRegionBackendService#enforcing_success_rate}
        '''
        result = self._values.get("enforcing_success_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceOutlierDetectionInterval"]:
        '''interval block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#interval GoogleComputeRegionBackendService#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceOutlierDetectionInterval"], result)

    @builtins.property
    def max_ejection_percent(self) -> typing.Optional[jsii.Number]:
        '''Maximum percentage of hosts in the load balancing pool for the backend service that can be ejected. Defaults to 10%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#max_ejection_percent GoogleComputeRegionBackendService#max_ejection_percent}
        '''
        result = self._values.get("max_ejection_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_rate_minimum_hosts(self) -> typing.Optional[jsii.Number]:
        '''The number of hosts in a cluster that must have enough request volume to detect success rate outliers.

        If the number of hosts is less than this setting, outlier
        detection via success rate statistics is not performed for any host in the
        cluster. Defaults to 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#success_rate_minimum_hosts GoogleComputeRegionBackendService#success_rate_minimum_hosts}
        '''
        result = self._values.get("success_rate_minimum_hosts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_rate_request_volume(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of total requests that must be collected in one interval (as defined by the interval duration above) to include this host in success rate based outlier detection.

        If the volume is lower than this setting, outlier
        detection via success rate statistics is not performed for that host. Defaults
        to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#success_rate_request_volume GoogleComputeRegionBackendService#success_rate_request_volume}
        '''
        result = self._values.get("success_rate_request_volume")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_rate_stdev_factor(self) -> typing.Optional[jsii.Number]:
        '''This factor is used to determine the ejection threshold for success rate outlier ejection.

        The ejection threshold is the difference between the mean success
        rate, and the product of this factor and the standard deviation of the mean
        success rate: mean - (stdev * success_rate_stdev_factor). This factor is divided
        by a thousand to get a double. That is, if the desired factor is 1.9, the
        runtime value should be 1900. Defaults to 1900.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#success_rate_stdev_factor GoogleComputeRegionBackendService#success_rate_stdev_factor}
        '''
        result = self._values.get("success_rate_stdev_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceOutlierDetection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf352f4de254f5e4a715ecce8fbe807c1494531e19926459fbef09cb8851f05)
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "seconds": seconds,
        }
        if nanos is not None:
            self._values["nanos"] = nanos

    @builtins.property
    def seconds(self) -> jsii.Number:
        '''Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        '''
        result = self._values.get("seconds")
        assert result is not None, "Required property 'seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Span of time that's a fraction of a second at nanosecond resolution.

        Durations
        less than one second are represented with a 0 'seconds' field and a positive
        'nanos' field. Must be from 0 to 999,999,999 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b030be36a22e431f0dc63beb08cd3c6949efe97bc4cd9998852451ea8ce45699)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f6baec217c752c0f598fd347481332345e06b97c72cf3f30cff1fe8f735d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39caa1b3c7097c9d17c59b438b147f447029a1aad45100a19f65eb1784602177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01fe7586673928b37a9bf02e6bc822f89b13b81c35a08cb1ace04c430529172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceOutlierDetectionInterval",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class GoogleComputeRegionBackendServiceOutlierDetectionInterval:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d17ca4b51ad1a331074b0cfe8f801230155fab41d8e571bcf81875ba6ae894)
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "seconds": seconds,
        }
        if nanos is not None:
            self._values["nanos"] = nanos

    @builtins.property
    def seconds(self) -> jsii.Number:
        '''Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        '''
        result = self._values.get("seconds")
        assert result is not None, "Required property 'seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Span of time that's a fraction of a second at nanosecond resolution.

        Durations
        less than one second are represented with a 0 'seconds' field and a positive
        'nanos' field. Must be from 0 to 999,999,999 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceOutlierDetectionInterval(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceOutlierDetectionIntervalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceOutlierDetectionIntervalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8100048c88232a347e1ba744a634fa3e2daf9b7e2497425e2aa754104b8728b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d7150903e91a1fa594fbe1b63262408cca2ead83a1bd4c1dc3b47b2f0693dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17777558983d27589adc2ea9dbf168308e9e9be99c3da7c8ebd3efb44f662103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceOutlierDetectionInterval]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceOutlierDetectionInterval], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceOutlierDetectionInterval],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d61d33ceb368b1b65add269a866dd785bc4460e8d432255973ac015ad92f3aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRegionBackendServiceOutlierDetectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceOutlierDetectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3b060d212cd17f4b8cf5def2cb841f45c46ec3ef0e9c6bd053d76a6adbbbab0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBaseEjectionTime")
    def put_base_ejection_time(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        value = GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime(
            seconds=seconds, nanos=nanos
        )

        return typing.cast(None, jsii.invoke(self, "putBaseEjectionTime", [value]))

    @jsii.member(jsii_name="putInterval")
    def put_interval(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        value = GoogleComputeRegionBackendServiceOutlierDetectionInterval(
            seconds=seconds, nanos=nanos
        )

        return typing.cast(None, jsii.invoke(self, "putInterval", [value]))

    @jsii.member(jsii_name="resetBaseEjectionTime")
    def reset_base_ejection_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseEjectionTime", []))

    @jsii.member(jsii_name="resetConsecutiveErrors")
    def reset_consecutive_errors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsecutiveErrors", []))

    @jsii.member(jsii_name="resetConsecutiveGatewayFailure")
    def reset_consecutive_gateway_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsecutiveGatewayFailure", []))

    @jsii.member(jsii_name="resetEnforcingConsecutiveErrors")
    def reset_enforcing_consecutive_errors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforcingConsecutiveErrors", []))

    @jsii.member(jsii_name="resetEnforcingConsecutiveGatewayFailure")
    def reset_enforcing_consecutive_gateway_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforcingConsecutiveGatewayFailure", []))

    @jsii.member(jsii_name="resetEnforcingSuccessRate")
    def reset_enforcing_success_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforcingSuccessRate", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetMaxEjectionPercent")
    def reset_max_ejection_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxEjectionPercent", []))

    @jsii.member(jsii_name="resetSuccessRateMinimumHosts")
    def reset_success_rate_minimum_hosts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessRateMinimumHosts", []))

    @jsii.member(jsii_name="resetSuccessRateRequestVolume")
    def reset_success_rate_request_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessRateRequestVolume", []))

    @jsii.member(jsii_name="resetSuccessRateStdevFactor")
    def reset_success_rate_stdev_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessRateStdevFactor", []))

    @builtins.property
    @jsii.member(jsii_name="baseEjectionTime")
    def base_ejection_time(
        self,
    ) -> GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTimeOutputReference:
        return typing.cast(GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTimeOutputReference, jsii.get(self, "baseEjectionTime"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(
        self,
    ) -> GoogleComputeRegionBackendServiceOutlierDetectionIntervalOutputReference:
        return typing.cast(GoogleComputeRegionBackendServiceOutlierDetectionIntervalOutputReference, jsii.get(self, "interval"))

    @builtins.property
    @jsii.member(jsii_name="baseEjectionTimeInput")
    def base_ejection_time_input(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime], jsii.get(self, "baseEjectionTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="consecutiveErrorsInput")
    def consecutive_errors_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "consecutiveErrorsInput"))

    @builtins.property
    @jsii.member(jsii_name="consecutiveGatewayFailureInput")
    def consecutive_gateway_failure_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "consecutiveGatewayFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="enforcingConsecutiveErrorsInput")
    def enforcing_consecutive_errors_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "enforcingConsecutiveErrorsInput"))

    @builtins.property
    @jsii.member(jsii_name="enforcingConsecutiveGatewayFailureInput")
    def enforcing_consecutive_gateway_failure_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "enforcingConsecutiveGatewayFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="enforcingSuccessRateInput")
    def enforcing_success_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "enforcingSuccessRateInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceOutlierDetectionInterval]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceOutlierDetectionInterval], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="maxEjectionPercentInput")
    def max_ejection_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxEjectionPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="successRateMinimumHostsInput")
    def success_rate_minimum_hosts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successRateMinimumHostsInput"))

    @builtins.property
    @jsii.member(jsii_name="successRateRequestVolumeInput")
    def success_rate_request_volume_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successRateRequestVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="successRateStdevFactorInput")
    def success_rate_stdev_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successRateStdevFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="consecutiveErrors")
    def consecutive_errors(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "consecutiveErrors"))

    @consecutive_errors.setter
    def consecutive_errors(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832a9447cc9c48f63e23f5a62729c2d5dc4dc052b88aa53b4a3ffd07fb2e5063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consecutiveErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consecutiveGatewayFailure")
    def consecutive_gateway_failure(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "consecutiveGatewayFailure"))

    @consecutive_gateway_failure.setter
    def consecutive_gateway_failure(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d901814879bdd5163f79f873d5f783877c75c982f90f3cb59f4d86d028bcb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consecutiveGatewayFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcingConsecutiveErrors")
    def enforcing_consecutive_errors(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enforcingConsecutiveErrors"))

    @enforcing_consecutive_errors.setter
    def enforcing_consecutive_errors(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec7d2a89743b62591a7d4017cde80be8823ed2cbdf2fc206d430395f57441003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcingConsecutiveErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcingConsecutiveGatewayFailure")
    def enforcing_consecutive_gateway_failure(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enforcingConsecutiveGatewayFailure"))

    @enforcing_consecutive_gateway_failure.setter
    def enforcing_consecutive_gateway_failure(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b553097e17d3c86edee6d0bd2ebb24dbf71a480f8989bad07ecd42ba0eca735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcingConsecutiveGatewayFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcingSuccessRate")
    def enforcing_success_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enforcingSuccessRate"))

    @enforcing_success_rate.setter
    def enforcing_success_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e327ae0ae0be45c7623dc8c4d6385082e961ae20df199eede806040f088ad234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcingSuccessRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxEjectionPercent")
    def max_ejection_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxEjectionPercent"))

    @max_ejection_percent.setter
    def max_ejection_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234a73d037aff70d216c79d34007827e81ccbb0b0a9a46bff63e294842b28889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxEjectionPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successRateMinimumHosts")
    def success_rate_minimum_hosts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successRateMinimumHosts"))

    @success_rate_minimum_hosts.setter
    def success_rate_minimum_hosts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c867ff5389025dc5763da2963f84f3674c5725a0303d57d6808f4de938492c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successRateMinimumHosts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successRateRequestVolume")
    def success_rate_request_volume(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successRateRequestVolume"))

    @success_rate_request_volume.setter
    def success_rate_request_volume(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c803e6b79c688a9e3299cb41aaac1a957995c86c30e201685054588ee6687411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successRateRequestVolume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successRateStdevFactor")
    def success_rate_stdev_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successRateStdevFactor"))

    @success_rate_stdev_factor.setter
    def success_rate_stdev_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a114014beea2a6cb902d8fa37a52c405e4027574ef881ffdd9827bcf3b245efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successRateStdevFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceOutlierDetection]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceOutlierDetection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceOutlierDetection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aae43db9ba821ebacc995f701cf78734ff644d24add9c04777f70b4ec8c41dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceStrongSessionAffinityCookie",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "ttl": "ttl"},
)
class GoogleComputeRegionBackendServiceStrongSessionAffinityCookie:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union["GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#name GoogleComputeRegionBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#path GoogleComputeRegionBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ttl GoogleComputeRegionBackendService#ttl}
        '''
        if isinstance(ttl, dict):
            ttl = GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl(**ttl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374d3c58b59f25ca65640bad5958958e90a2910aac68a6b59d6ec2f5de5bd974)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if path is not None:
            self._values["path"] = path
        if ttl is not None:
            self._values["ttl"] = ttl

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the cookie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#name GoogleComputeRegionBackendService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to set for the cookie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#path GoogleComputeRegionBackendService#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl"]:
        '''ttl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#ttl GoogleComputeRegionBackendService#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceStrongSessionAffinityCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceStrongSessionAffinityCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceStrongSessionAffinityCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cf02ce783bbdccde518d85a89f883dab4fd5de6abea34a0985db0185a576519)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTtl")
    def put_ttl(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        value = GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl(
            seconds=seconds, nanos=nanos
        )

        return typing.cast(None, jsii.invoke(self, "putTtl", [value]))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(
        self,
    ) -> "GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtlOutputReference":
        return typing.cast("GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtlOutputReference", jsii.get(self, "ttl"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(
        self,
    ) -> typing.Optional["GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl"]:
        return typing.cast(typing.Optional["GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl"], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__867bc6d41eb66acc0b9c7d57f4d7803a1860bf3f95440f285525660018c330b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c473e8989fd0e392a28c630befc037ff6551ea2cc75195ba7292a0756e5cf877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceStrongSessionAffinityCookie]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceStrongSessionAffinityCookie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceStrongSessionAffinityCookie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e2f4dab3c678c1cd379f3d3f2c535293b867d3c7bfaabef110f4a145dc08688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c61e0cc853c077e4a0065cadacbd560df10927fe954d3623289468ec18cde5d)
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "seconds": seconds,
        }
        if nanos is not None:
            self._values["nanos"] = nanos

    @builtins.property
    def seconds(self) -> jsii.Number:
        '''Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#seconds GoogleComputeRegionBackendService#seconds}
        '''
        result = self._values.get("seconds")
        assert result is not None, "Required property 'seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Span of time that's a fraction of a second at nanosecond resolution.

        Durations less than one second are represented
        with a 0 seconds field and a positive nanos field. Must
        be from 0 to 999,999,999 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#nanos GoogleComputeRegionBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6cc01c98525d80978e064c6303c28103891cacb5ac3238701fee28c7fb21481)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318f1067ac5a09f3f650f3d3dad4febecacaebe9df0dd4be0d45a385e948be9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c0662d7914837f858b8c1db830aa8b44ed80998ccb565f5040452b5cbdcb83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a5ddde61fefc1599318a0d67dc7e448957850b8c968bd5b87198619a8d14c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceSubsetting",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "subset_size": "subsetSize"},
)
class GoogleComputeRegionBackendServiceSubsetting:
    def __init__(
        self,
        *,
        policy: builtins.str,
        subset_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param policy: The algorithm used for subsetting. Possible values: ["CONSISTENT_HASH_SUBSETTING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#policy GoogleComputeRegionBackendService#policy}
        :param subset_size: The number of backends per backend group assigned to each proxy instance or each service mesh client. An input parameter to the CONSISTENT_HASH_SUBSETTING algorithm. Can only be set if policy is set to CONSISTENT_HASH_SUBSETTING. Can only be set if load balancing scheme is INTERNAL_MANAGED or INTERNAL_SELF_MANAGED. subsetSize is optional for Internal HTTP(S) load balancing and required for Traffic Director. If you do not provide this value, Cloud Load Balancing will calculate it dynamically to optimize the number of proxies/clients visible to each backend and vice versa. Must be greater than 0. If subsetSize is larger than the number of backends/endpoints, then subsetting is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#subset_size GoogleComputeRegionBackendService#subset_size}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0df901c96d83f64c7aa9de796bb54e9dfd055bcf246f4f2569aeaf0408b27c0)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument subset_size", value=subset_size, expected_type=type_hints["subset_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
        }
        if subset_size is not None:
            self._values["subset_size"] = subset_size

    @builtins.property
    def policy(self) -> builtins.str:
        '''The algorithm used for subsetting. Possible values: ["CONSISTENT_HASH_SUBSETTING"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#policy GoogleComputeRegionBackendService#policy}
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subset_size(self) -> typing.Optional[jsii.Number]:
        '''The number of backends per backend group assigned to each proxy instance or each service mesh client.

        An input parameter to the CONSISTENT_HASH_SUBSETTING algorithm. Can only be set if policy is set to
        CONSISTENT_HASH_SUBSETTING. Can only be set if load balancing scheme is INTERNAL_MANAGED or INTERNAL_SELF_MANAGED.
        subsetSize is optional for Internal HTTP(S) load balancing and required for Traffic Director.
        If you do not provide this value, Cloud Load Balancing will calculate it dynamically to optimize the number
        of proxies/clients visible to each backend and vice versa.
        Must be greater than 0. If subsetSize is larger than the number of backends/endpoints, then subsetting is disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#subset_size GoogleComputeRegionBackendService#subset_size}
        '''
        result = self._values.get("subset_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceSubsetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceSubsettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceSubsettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1134ab4a3f5d8297337bb8bd2a09efcbe998cdf323dc2ebc66eddf42121b1b65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSubsetSize")
    def reset_subset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubsetSize", []))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="subsetSizeInput")
    def subset_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "subsetSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f3867a25d50867461e9ca9311d653894b5dd26b0f6d6d15765dea801a3e4c46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subsetSize")
    def subset_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "subsetSize"))

    @subset_size.setter
    def subset_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb64a68f632995ae2239ff3f00c6d3df404e7b7fb3680ddb339b6928f7d6bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subsetSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeRegionBackendServiceSubsetting]:
        return typing.cast(typing.Optional[GoogleComputeRegionBackendServiceSubsetting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRegionBackendServiceSubsetting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf6c2f48be28a5beb6e52c7a78b0926e191a515d237c190fa5b65d2c45f6da8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeRegionBackendServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#create GoogleComputeRegionBackendService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#delete GoogleComputeRegionBackendService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#update GoogleComputeRegionBackendService#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98f779571c764e79473650f2de723c5675a27601b11052459b6116ed0ffd8eaf)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#create GoogleComputeRegionBackendService#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#delete GoogleComputeRegionBackendService#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_region_backend_service#update GoogleComputeRegionBackendService#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRegionBackendServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRegionBackendServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRegionBackendService.GoogleComputeRegionBackendServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d90140e549d77bd3b6e263df957405e49612d774a9c3ee61604f689584f85df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92702fd444f7408dba111368f94a7af4e744439528914e91923462d0350ece0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d3897be4d6ea382bfc8019b1dbe28738a8060b407d532c8dffb9492e7f756b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0fc38db2149a0971701c5c18dc971cb22d38549af91e444867e67f51103131c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce61859b892c21c84b86f2295c23a38a231afb9a4d167785bd5b337fd60e851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeRegionBackendService",
    "GoogleComputeRegionBackendServiceBackend",
    "GoogleComputeRegionBackendServiceBackendCustomMetrics",
    "GoogleComputeRegionBackendServiceBackendCustomMetricsList",
    "GoogleComputeRegionBackendServiceBackendCustomMetricsOutputReference",
    "GoogleComputeRegionBackendServiceBackendList",
    "GoogleComputeRegionBackendServiceBackendOutputReference",
    "GoogleComputeRegionBackendServiceCdnPolicy",
    "GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy",
    "GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicyOutputReference",
    "GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy",
    "GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyList",
    "GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyOutputReference",
    "GoogleComputeRegionBackendServiceCdnPolicyOutputReference",
    "GoogleComputeRegionBackendServiceCircuitBreakers",
    "GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout",
    "GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeoutOutputReference",
    "GoogleComputeRegionBackendServiceCircuitBreakersOutputReference",
    "GoogleComputeRegionBackendServiceConfig",
    "GoogleComputeRegionBackendServiceConnectionTrackingPolicy",
    "GoogleComputeRegionBackendServiceConnectionTrackingPolicyOutputReference",
    "GoogleComputeRegionBackendServiceConsistentHash",
    "GoogleComputeRegionBackendServiceConsistentHashHttpCookie",
    "GoogleComputeRegionBackendServiceConsistentHashHttpCookieOutputReference",
    "GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl",
    "GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtlOutputReference",
    "GoogleComputeRegionBackendServiceConsistentHashOutputReference",
    "GoogleComputeRegionBackendServiceCustomMetrics",
    "GoogleComputeRegionBackendServiceCustomMetricsList",
    "GoogleComputeRegionBackendServiceCustomMetricsOutputReference",
    "GoogleComputeRegionBackendServiceDynamicForwarding",
    "GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection",
    "GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelectionOutputReference",
    "GoogleComputeRegionBackendServiceDynamicForwardingOutputReference",
    "GoogleComputeRegionBackendServiceFailoverPolicy",
    "GoogleComputeRegionBackendServiceFailoverPolicyOutputReference",
    "GoogleComputeRegionBackendServiceIap",
    "GoogleComputeRegionBackendServiceIapOutputReference",
    "GoogleComputeRegionBackendServiceLogConfig",
    "GoogleComputeRegionBackendServiceLogConfigOutputReference",
    "GoogleComputeRegionBackendServiceOutlierDetection",
    "GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime",
    "GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTimeOutputReference",
    "GoogleComputeRegionBackendServiceOutlierDetectionInterval",
    "GoogleComputeRegionBackendServiceOutlierDetectionIntervalOutputReference",
    "GoogleComputeRegionBackendServiceOutlierDetectionOutputReference",
    "GoogleComputeRegionBackendServiceStrongSessionAffinityCookie",
    "GoogleComputeRegionBackendServiceStrongSessionAffinityCookieOutputReference",
    "GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl",
    "GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtlOutputReference",
    "GoogleComputeRegionBackendServiceSubsetting",
    "GoogleComputeRegionBackendServiceSubsettingOutputReference",
    "GoogleComputeRegionBackendServiceTimeouts",
    "GoogleComputeRegionBackendServiceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0e16cc2d745a76f8cb556f7b43dcf234fece74dcd1b6d618d688f637e1557d77(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    affinity_cookie_ttl_sec: typing.Optional[jsii.Number] = None,
    backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cdn_policy: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    circuit_breakers: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceCircuitBreakers, typing.Dict[builtins.str, typing.Any]]] = None,
    connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
    connection_tracking_policy: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceConnectionTrackingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    consistent_hash: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceConsistentHash, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionBackendServiceCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamic_forwarding: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceDynamicForwarding, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    failover_policy: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceFailoverPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    iap: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceIap, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address_selection_policy: typing.Optional[builtins.str] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    locality_lb_policy: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[builtins.str] = None,
    outlier_detection: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceOutlierDetection, typing.Dict[builtins.str, typing.Any]]] = None,
    port_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    security_policy: typing.Optional[builtins.str] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    strong_session_affinity_cookie: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceStrongSessionAffinityCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    subsetting: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceSubsetting, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_sec: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__a27907a3b034f26dc85e3722ae1236483fcaf4d88b90b219d795e5a3e7a66e5c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe6af6df038d3611da5bc5cbe4479e61f81eb2d70cc6f4b33c2af0a6e1b1a38(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47794b7f71f90a95bd2b1a5a7905a7ff7a3f2822d3fddea3149403bb9c68dfaf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionBackendServiceCustomMetrics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388e4f1d56611ac154e1c7425c0c738ad01d1c00544763cb3f6e9376ea7224c1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48662c52255952b43c61332cb7b6d44dcaaf6759ddc46cb7a09e10c393edf0a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e141224b6561a124303b8e2dfee4cfd2cdf5bcda5bb788e5cb2afcf07292336(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8968d9462a272a1e5dcfb9fd3013b9cc26668ef92c0f2af498ebced48d7ce56c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ee6a38fd114edfe14be1319870f7f7829fde7f6a97f76e84c33114075339f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357dfd8d7d9bc864cbd573e5d58cea96bef4556f94f151617fc24ba425e1ed02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186f8f8b6a917569717678160e2db744d16006e66b453e0e99f3f39b11b7b266(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0eef5df96e695b2207167bbeeeb916b1caf61d5afeee9d4f85b2777686eafa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71f5646e86567e6183370a0e75996508e819a388958a7421ee817c4031b343b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a40d0efd575f844e654199132eb5349356aeb72dfd401c4402e7289743e855(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93099defbe4fb2c7d00f7b7d45c9e9665880c3b98af687305d005a66e25da868(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c6d7e243062346243f15f5f08d1fc5cd24657f2cdf70e2846e57af097502e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722ebe75954967e6747c3482c8d8859f779e80d8030e48f75e26fca273ddebae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0727e5b5b4df740f568445e05cb7944a09e1b7a96ed20fdabc1804789355c9c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961e4ec1d692af08c4da5337cef5d6e6083eda60e167dc10683a9aabaa8481da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a92d86ae32cdc68c0850bf5e1b12cf92de4da64c50bd7f70616d19a95db6b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d26374e2f3142759a394000ef0a657689a96446c41ea6f8045283009800c87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345b259c60f0d99c137c967ba3f210383a0276314a00d0a544dc5b8d1ca58ec9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7883e8a00ba9b8e9934b3720f972c96da3837e28c99affde99f14f121de20e99(
    *,
    group: builtins.str,
    balancing_mode: typing.Optional[builtins.str] = None,
    capacity_scaler: typing.Optional[jsii.Number] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionBackendServiceBackendCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    failover: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_connections: typing.Optional[jsii.Number] = None,
    max_connections_per_endpoint: typing.Optional[jsii.Number] = None,
    max_connections_per_instance: typing.Optional[jsii.Number] = None,
    max_rate: typing.Optional[jsii.Number] = None,
    max_rate_per_endpoint: typing.Optional[jsii.Number] = None,
    max_rate_per_instance: typing.Optional[jsii.Number] = None,
    max_utilization: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f0245e026398768534fd75f8874407ca4b9791db825e0d63c9147e51e1b6d2(
    *,
    dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    max_utilization: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490bedba664fb071d857e0874d6e428b67e69fb1c6f6dbaa4afabeabfca58dd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__232a22623fb10e115acccdbd3d39ed75cc0793d25a406450475ac3a3105f24e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cda44d944d962ec70224e77ec4c1bd2cc5d2db13a4aa03bf8ea4fe1d870820e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2f50baa9aabc8c416ee60d817d611784752b119214653814a14fb747635ae6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d15ac777d7bb9d8ee99beba759ab9bba0dcc86704da015e2d1e21c1b730156(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001e800e43cfb7bb831fe8f17a9e7276a948a20e324101a758b247b12ec243ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceBackendCustomMetrics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0c3bc08cfa587893a49993c73091c87eaf7cb3cedef638cec986c7085b51dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5f8b178ad0008e771a9212cb5fdeab98f513c6bed5ede93f1d032b4ef668ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bda4eb6b234b781f29bc658466712c7bbfe229398d297674a80baf13f2490d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10795f8b5c16f8b433bdacea9de6d5a035a1a20e498a2633886caa5db23554c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27a354dc168edcbc5985d8d08273277f9132d18381e1f410687fd51fd151097(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceBackendCustomMetrics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468ea21e84df6580c250c1335e54bf9cdccae8d0499fedf1b8cc1f16a74e5671(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7ddc9b8e041b35f9dbd440e2d55a3cc42b3db1b1b9daa8ced091585884df7d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398322e743f02440c0ad9269e4b93a4f33d33aa8f6a97fcad8d3de1b1f0bac6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886c75e97c6613284d0bd2bd86c0ce25342c9b5aff2c68dfba44a4bf31c89a48(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12830c235234a43f1a36ef9590a773bde1591737e4743b7237fe815754e87824(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427ed5df5c2038e7c054e2c336d47d57dfe1ac0d30bd1aeba735b6dfe6cb6482(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceBackend]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a792586768b98a88435b4bf7427b7250be7dac3990207fad28059cdca265c818(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c878eadeb91f3366a85725a05b03914389361e5657e18e0f064fa0a26b25055e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionBackendServiceBackendCustomMetrics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__062697336d0ed803581094c1d7939f541570a5e93723cec5fff82f9e0b82a9f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c94769931fa978d5af929b9e2c1a0f6c47082b2d1df656a65e662b9be9419b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36eadaa441d1fb1c9d33c7561dbea20bae4b616bd5820b78e5077ad4fc652b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535b1ecfbea28b4e77e45b44d50cdaaa5a92a59cbe05dbe110832648611e5af0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddce24dfe250f285b4d4f58c1ba674c6d3069ae844567988645cf00d5acb94df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce557fb9bfb5495528f1c808ff1d662d386f4ca188583c72d13cc69d55ba856b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737e1ec3a817b9d7547ea1f6045c38799f7a869bf9cfbe6c6c162711de991c9c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3fee823ae9ad4d761dd6bad0ed456e18aa598f09c7a58ac1076f099d846fc4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7a1da13e64478fc1f7e1ddde734c27d52a70451a1bd8674bab7a9c893f8632(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05807f67dd21a7b8633b60c814878cb9e9f1c78f468a99297e4c912a2470ec49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6525731c1c925c670374a6b340048e74928f3df6803afc885ab9e2dd84d3f1d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01af17f911e17f0c8aad68edb28e47c8165c1c4dc88464d8f03d7cfa52542e23(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc079e314987c2ab239e893affa3daba627bbce319fdc961cca26a3fe3f70634(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceBackend]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0dc9102c3ec9eeb6eb29250cae07f52e5a95a9d66b675876f7f52165c8fabf4(
    *,
    cache_key_policy: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    cache_mode: typing.Optional[builtins.str] = None,
    client_ttl: typing.Optional[jsii.Number] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    max_ttl: typing.Optional[jsii.Number] = None,
    negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    serve_while_stale: typing.Optional[jsii.Number] = None,
    signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a9f810f4be69252c942f083e0607589ab57ae672e7699c207372f4b691debe(
    *,
    include_host: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_named_cookies: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_protocol: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_query_string: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_string_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed143ff51eda0a00b0b5aa08d4fef2c033ce23268e4de2c2a365b650c3d470d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__156a09ea57bb569ec76e6e05d8c0a80aefe6e26dd2228ac12837f780729cd379(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c816fbf3942cb05ddff88bfcc1282ad074e147effa62e1ca801c28e84589f1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24666b720692db1a81c42f261f36c58bdec80042dc67d9d85c5cece3a74343dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efec32b41fcf7f2388a8fe44551dcdd0301527924ab8a5efd093c46175abd31(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585bcf1398ddc39485d19317a80efc8ab29819a212e01f5914edc69150cd0155(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c330dbbe9b4f043b1bea9d5b00f29738afe52b9c6f0512a75d11a38ae8d1556(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca0472e06daab5b2a629e5772756bf0b82c1dabab742c3bae248b2816c00bca(
    value: typing.Optional[GoogleComputeRegionBackendServiceCdnPolicyCacheKeyPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b122232dbe8effe1183be418f5091848b9dcb94d0724af8e640b605f582be5cf(
    *,
    code: typing.Optional[jsii.Number] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4b4344691ea58a4525b465f192fdff10e1610f73ef2d5a34ab55ad0ab378fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff9e3c3814b819cc704a888e0be92c7fc85d35c5cfd070245e51f2b36e4e544(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24077b4a9909a4ec6de7c171f1054d99daf466851293ec4c8fc1f51f7cccd6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12cbecf14dfc8911a81b35aeeff8758991c151da162b62190d91d0d6928a9ce3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f70f6eddd81855951648dc8ce8181f085651794b084275b36d7ce62dd5fedd7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3fa3c57f929f6e9e96fc7ca3cfeaf939c34a9101810c48bc42fe07793d19f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169159986fe0eb15cb88598bbefd5b60a85ece2fadbfe60bd098b1ce93a008f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7fc89d42e187ef59a46e8954ae02bdd75bbfa8f28a0543528781632a1f31bb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae53def47fdf69bb6452a9c6127f8a78f32c53fb7fbee514f31fab111df6f47f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f031c14cbed241618b8997e7b1111a81127a1f9b576a5e3d0df9f9c5c9278f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6400dd3bba24cb8032b5e7bb4fd99fc842325f28461ba27c29169ae28acb18b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f8eab777f35d4ece770f45731b2e87a94b95a0da39095bc3a31c6ade3ec940(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691a53f793dc1fc2c90f3b9704e950a2b892ab51bf4fe44989bde1367c9f63d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a76f8b145ae4db179fa3f3ac2991ac7492a7d5617f51f23b031bebf0592b3de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37bff7ac53bcb02c58d131a8b640a6601039822bd82a43d7a0f3b18c589b374c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306b8ebf73582fe0ed2a013c2a0fd769de8a35a3f8e2654cdad63905c6d2693c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c717c7a16786722f571ad82880f43c5a807501dfb3c68f228eca0d6e01dad6d5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d1be0e408c8d1350c8c9a5ae562a73b76f2149b0716b14d9fd7538bdb0ef4fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591689939c12763d4b015a4c640a64cb9934ad0a55697c9b564f8c5f7d922c03(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e200d33c435e40cf5eb5401db6b66206bfbf842a18c24b634207a8301c3654b(
    value: typing.Optional[GoogleComputeRegionBackendServiceCdnPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73f3471329f2687abcea89668b43f169a5960a7376f8390f7a465db4e8a8813(
    *,
    connect_timeout: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
    max_connections: typing.Optional[jsii.Number] = None,
    max_pending_requests: typing.Optional[jsii.Number] = None,
    max_requests: typing.Optional[jsii.Number] = None,
    max_requests_per_connection: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d5951b1cd2d910a2fef9751320389492ddb7df5001339b1606542d697c5d1f(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b4f5aa9447a517a0117eabf9262610becfe276abf5c7b3fd9980bfeb98f068e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c884924ba86c6452070c42b89f77a09a7ddbe357eb162b6e5ab150ed6195866(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173992e7e59706aa1aa525d2005d61390aa8849901ad81b2548ae0badc53e58b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76bddb7c7f017b1b25631be988cd19bd339035aeb07972ebff3b7d476f44348(
    value: typing.Optional[GoogleComputeRegionBackendServiceCircuitBreakersConnectTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ac5362d42f6efaa56ece05f8846725891b50770ad1c6632e5d6cc92b946902(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d07a42fdbe013e299427d0031ff7f8cce0cd95bb0491b97b6bd6fc00abd41f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389f58fe63125a05fd9f364043d3fca4d1bee80597a14c5d35692c50894953ac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b88083156bd98d519f3847441f787f4ca9c50479fcc6f0dabdd18eda82573f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42aa84559c0afeadb2e55900e405211aaad2300f08c3922bc7b5084225f9d6ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba7399e478b18f8bc0f9bdaa470543164165e18c12dc365120d722f2c8ec7a0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40b25cc55fef9e456d84e39ec4a36fef8a5c6b81ece717a6b3dde89f822a855(
    value: typing.Optional[GoogleComputeRegionBackendServiceCircuitBreakers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cbca61b22bfc77949d7978e79f7e87c59f7a62321bf336b58551e46bf689f93(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    affinity_cookie_ttl_sec: typing.Optional[jsii.Number] = None,
    backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cdn_policy: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    circuit_breakers: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceCircuitBreakers, typing.Dict[builtins.str, typing.Any]]] = None,
    connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
    connection_tracking_policy: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceConnectionTrackingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    consistent_hash: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceConsistentHash, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRegionBackendServiceCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamic_forwarding: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceDynamicForwarding, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    failover_policy: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceFailoverPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    iap: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceIap, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address_selection_policy: typing.Optional[builtins.str] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    locality_lb_policy: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[builtins.str] = None,
    outlier_detection: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceOutlierDetection, typing.Dict[builtins.str, typing.Any]]] = None,
    port_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    security_policy: typing.Optional[builtins.str] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    strong_session_affinity_cookie: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceStrongSessionAffinityCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    subsetting: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceSubsetting, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186850c287f38b5670c0f949d38a86ba008496cd243c95eb63dfad6a08bfe77b(
    *,
    connection_persistence_on_unhealthy_backends: typing.Optional[builtins.str] = None,
    enable_strong_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    idle_timeout_sec: typing.Optional[jsii.Number] = None,
    tracking_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5d1c9003d7a56a17379a7e909eb90c24c282a07bd604d4879a0aeec1b756ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec8c518fbe9613134ae6b426cd460cb9fc94c64eeada7504946c88c9cfe6e28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be4f49fb30d1efd7a5e9c233071bec658c7e30376cd7350fa5febb6d2a9e1ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963c59ae89f11bac0d9f1c5cc20dadfc353111b9ae2a2b889142bf5654683a77(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f0f8673cbfe57faaa19c1d1375d534372d930c608e288454916848565c686c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c66ea8e970ce634d831c0bb6799114f020fca6fab6accf6ec76ac0e4129cd67(
    value: typing.Optional[GoogleComputeRegionBackendServiceConnectionTrackingPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05c015bd6fcc92648de303fdd634b305576421e1aacd3393022ba04a44a70d4(
    *,
    http_cookie: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceConsistentHashHttpCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    http_header_name: typing.Optional[builtins.str] = None,
    minimum_ring_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1111f2fedc5e8349f60587f91ba9cd6047b501e76b7afe8facb9474b431d20(
    *,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83da1285925badf3e455064abeedf73fa263f3d790041d8b018441b67238db7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe347293601a4214e4a3411d27beecca37d9a301be3bc5ff0576dc511ff471a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679904b30d2ad284fc2ebe4f5a30138380be90b8ab79b81e576ae0ceb75edca9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2c1b61ca8bbf89f4aa913bd2088d30b92ea4b2ca64e3d900be9f4accff3617(
    value: typing.Optional[GoogleComputeRegionBackendServiceConsistentHashHttpCookie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4a015ce0a8ad48fd7d1419b10bd987cc5e350d23556a2afb67b52a097f0d71(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7fb9512799f035be88456dc6ac598a72081506d2bb4ee3fec95c86a9d74045(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f174878baa8f957103347a5d49f28166b176927a09281c9151f08a08a6aae75(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2757511df94ac3d8c6b0cf623b42f12d5d098fd0698ac055965be33e9414ba2d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2769149c28dfac0fbac939dd045ce5905114ca85449b0adab35bfa75348a448d(
    value: typing.Optional[GoogleComputeRegionBackendServiceConsistentHashHttpCookieTtl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4898e8db26c2f881fbbfa6fa2be8e91571521b0bb35f38bc5cf224883feefa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15d2387caa5ef93fe26a11cae0f7c36e1e7be3186cc4a938b5473ad14e6455f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3dce71a3a04d2b2bb9426d4cc8b11e408506f33ba76920075d4ddbf77623c20(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac254ff911892f1e4c4d9aa274ff57c1fd014a658b668a269227502fa188430(
    value: typing.Optional[GoogleComputeRegionBackendServiceConsistentHash],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e95fc8f422a037d9378ce45a126e9b63a6e815b68aacc5f4fe99300a6bb9d8(
    *,
    dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0925527a984174502f9f295ab6c1bf67dcce7305a67ad735d839232baf429f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb99a428c438e04063339e94d7c3689b4f95ad8410609eaee452ba9ec0de5e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9908db6338b9852b94934c28cee130bcc7fc92b38d4b0d96c6c2059b396beb2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec596cef20c9bd60e07aacd4594e156d592409de83a811f8508a648b86aa1b5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559e5695183c03bc5c96ca402df532c50de3aaf61dc7b4f74d6af1c1cabac9cb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84513dee6fbce06ec4829b81fdede85958b0020ea564ea7e3b309ded3eee26f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRegionBackendServiceCustomMetrics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b31e68c7be5bd6e300cd802f5028727134c5246323aa976d9b8d7e1a13e234d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d835e33de227b7b3be8ce1810518968cd2b4cb6352dd91e19cba314b6fd3afa1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1297b906e3d31c8b62b7014c2289b22cae9201850bc1076bb49d38d1feeef3b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8ba8bb823b3f1fce1de1a96a2a26e9dd61c40b5123903d4709130c0bf697e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceCustomMetrics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eaef17e15382260e6f9082ba9c78aff777bad52e8291d11941554f6a3abbff0(
    *,
    ip_port_selection: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67cd95b0bbff7c1faac034872621716cc1d9891f216bc3faea09f664f81a65d(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6972b36613f1c40b50ef6da7b2b899a03a06933576c0283bcfd440126c54db7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04761ea6ab0fd8ef4324f0d150954efceb3d9d861fb73b95f1bdb146132cfb6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b190703618a76c5081214b896b0471788e44f5e655ecc1aa94350d6bc35aec07(
    value: typing.Optional[GoogleComputeRegionBackendServiceDynamicForwardingIpPortSelection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22fb5472514720f7f28b4f2e95071cdbf903bdf0ca0fe2541183ebe9da1162a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fed537b8e13eb4905f95b4e56c88695800336328a191b502e5346f5d7754b1c(
    value: typing.Optional[GoogleComputeRegionBackendServiceDynamicForwarding],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b8c9dc333fae7e990487ee1a726804babe31df145270d86dad471f2d85875e0(
    *,
    disable_connection_drain_on_failover: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drop_traffic_if_unhealthy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    failover_ratio: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e1ff00edd371c637c7c14bfe198364f46f90bddf2a110a3d3383248f523a4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c2654404b4600accae7a699f8c449d32098f17dc5fc967f96e5fe44d15902e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ad0939143e5e01edcdadfb1c4b6679040295d822973dfdc4b470e608c76429(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e1be36edf39f334609c01e9edea83f6aa55fa50f44221b1592fd7217be72de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57970fb46a212dd310af7a2b1d7c356f62aae853d6d24ff41473cfa985fb068a(
    value: typing.Optional[GoogleComputeRegionBackendServiceFailoverPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f300bb090f2cb7740ab2055d393eadabff0c250ffc86a426e0210c8725dd088c(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    oauth2_client_id: typing.Optional[builtins.str] = None,
    oauth2_client_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a61fac610bde6fe213bfab52fcdb66efdd6cc4784e8be8d12cfa2d36c82aab9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2de6196fd0ea1b41fc2ed19a4cfcffd3db2093407cc2404a238762860597c20(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567954f723c342344563217e38d1a6df2467b97163784177beabb2592f4e439c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e846fc569a993869720c32d582b86ee42bc1404b9baca130983bf664fa99049(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5074bb02ba714f8038d6ffd09841d75df56c6479b3b2ebcf60ab295964b6dd0(
    value: typing.Optional[GoogleComputeRegionBackendServiceIap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70034f84c1e3507374074f498b2edfb8571d89f9c3c721522559ad70e199032(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    optional_mode: typing.Optional[builtins.str] = None,
    sample_rate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ad3a4760c2dcf98312f2b828502e243144ef06d743cba94ee78a2f2e290be8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d7096dae4e686629680ddd40d5342420aa196ca5a91482f083b20d29e1bb3f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d099e44f7b1851073d1c68a2c8cee6268d2489fd001a64255a9fdc635ade759e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba17e114adadff0b1eae8253563e19c1628a75ae7fa4625298794f3e624ccad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318c82500340a14e6a41d6f813aa66aea76eebdacec338221c54733752467523(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e49042912a863761ecbddb9f6cab7bcdef4a082794d7266b018899dc94ef01(
    value: typing.Optional[GoogleComputeRegionBackendServiceLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba2c3aa66fa2e50d62d5ebd9180f503ed706df3dd6e9dcb9ab96fa338cc3af0(
    *,
    base_ejection_time: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime, typing.Dict[builtins.str, typing.Any]]] = None,
    consecutive_errors: typing.Optional[jsii.Number] = None,
    consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
    enforcing_consecutive_errors: typing.Optional[jsii.Number] = None,
    enforcing_consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
    enforcing_success_rate: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceOutlierDetectionInterval, typing.Dict[builtins.str, typing.Any]]] = None,
    max_ejection_percent: typing.Optional[jsii.Number] = None,
    success_rate_minimum_hosts: typing.Optional[jsii.Number] = None,
    success_rate_request_volume: typing.Optional[jsii.Number] = None,
    success_rate_stdev_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf352f4de254f5e4a715ecce8fbe807c1494531e19926459fbef09cb8851f05(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b030be36a22e431f0dc63beb08cd3c6949efe97bc4cd9998852451ea8ce45699(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f6baec217c752c0f598fd347481332345e06b97c72cf3f30cff1fe8f735d7b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39caa1b3c7097c9d17c59b438b147f447029a1aad45100a19f65eb1784602177(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01fe7586673928b37a9bf02e6bc822f89b13b81c35a08cb1ace04c430529172(
    value: typing.Optional[GoogleComputeRegionBackendServiceOutlierDetectionBaseEjectionTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d17ca4b51ad1a331074b0cfe8f801230155fab41d8e571bcf81875ba6ae894(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8100048c88232a347e1ba744a634fa3e2daf9b7e2497425e2aa754104b8728b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d7150903e91a1fa594fbe1b63262408cca2ead83a1bd4c1dc3b47b2f0693dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17777558983d27589adc2ea9dbf168308e9e9be99c3da7c8ebd3efb44f662103(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d61d33ceb368b1b65add269a866dd785bc4460e8d432255973ac015ad92f3aa(
    value: typing.Optional[GoogleComputeRegionBackendServiceOutlierDetectionInterval],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b060d212cd17f4b8cf5def2cb841f45c46ec3ef0e9c6bd053d76a6adbbbab0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832a9447cc9c48f63e23f5a62729c2d5dc4dc052b88aa53b4a3ffd07fb2e5063(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d901814879bdd5163f79f873d5f783877c75c982f90f3cb59f4d86d028bcb3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7d2a89743b62591a7d4017cde80be8823ed2cbdf2fc206d430395f57441003(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b553097e17d3c86edee6d0bd2ebb24dbf71a480f8989bad07ecd42ba0eca735(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e327ae0ae0be45c7623dc8c4d6385082e961ae20df199eede806040f088ad234(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234a73d037aff70d216c79d34007827e81ccbb0b0a9a46bff63e294842b28889(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c867ff5389025dc5763da2963f84f3674c5725a0303d57d6808f4de938492c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c803e6b79c688a9e3299cb41aaac1a957995c86c30e201685054588ee6687411(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a114014beea2a6cb902d8fa37a52c405e4027574ef881ffdd9827bcf3b245efc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aae43db9ba821ebacc995f701cf78734ff644d24add9c04777f70b4ec8c41dd(
    value: typing.Optional[GoogleComputeRegionBackendServiceOutlierDetection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374d3c58b59f25ca65640bad5958958e90a2910aac68a6b59d6ec2f5de5bd974(
    *,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[typing.Union[GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf02ce783bbdccde518d85a89f883dab4fd5de6abea34a0985db0185a576519(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867bc6d41eb66acc0b9c7d57f4d7803a1860bf3f95440f285525660018c330b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c473e8989fd0e392a28c630befc037ff6551ea2cc75195ba7292a0756e5cf877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e2f4dab3c678c1cd379f3d3f2c535293b867d3c7bfaabef110f4a145dc08688(
    value: typing.Optional[GoogleComputeRegionBackendServiceStrongSessionAffinityCookie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c61e0cc853c077e4a0065cadacbd560df10927fe954d3623289468ec18cde5d(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6cc01c98525d80978e064c6303c28103891cacb5ac3238701fee28c7fb21481(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318f1067ac5a09f3f650f3d3dad4febecacaebe9df0dd4be0d45a385e948be9d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c0662d7914837f858b8c1db830aa8b44ed80998ccb565f5040452b5cbdcb83(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a5ddde61fefc1599318a0d67dc7e448957850b8c968bd5b87198619a8d14c5(
    value: typing.Optional[GoogleComputeRegionBackendServiceStrongSessionAffinityCookieTtl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0df901c96d83f64c7aa9de796bb54e9dfd055bcf246f4f2569aeaf0408b27c0(
    *,
    policy: builtins.str,
    subset_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1134ab4a3f5d8297337bb8bd2a09efcbe998cdf323dc2ebc66eddf42121b1b65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3867a25d50867461e9ca9311d653894b5dd26b0f6d6d15765dea801a3e4c46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb64a68f632995ae2239ff3f00c6d3df404e7b7fb3680ddb339b6928f7d6bdd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6c2f48be28a5beb6e52c7a78b0926e191a515d237c190fa5b65d2c45f6da8d(
    value: typing.Optional[GoogleComputeRegionBackendServiceSubsetting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98f779571c764e79473650f2de723c5675a27601b11052459b6116ed0ffd8eaf(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d90140e549d77bd3b6e263df957405e49612d774a9c3ee61604f689584f85df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92702fd444f7408dba111368f94a7af4e744439528914e91923462d0350ece0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d3897be4d6ea382bfc8019b1dbe28738a8060b407d532c8dffb9492e7f756b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fc38db2149a0971701c5c18dc971cb22d38549af91e444867e67f51103131c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce61859b892c21c84b86f2295c23a38a231afb9a4d167785bd5b337fd60e851(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRegionBackendServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
