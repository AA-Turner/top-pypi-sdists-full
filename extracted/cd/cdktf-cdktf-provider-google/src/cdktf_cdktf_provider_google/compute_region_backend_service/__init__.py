r'''
# `google_compute_region_backend_service`

Refer to the Terraform Registry for docs: [`google_compute_region_backend_service`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service).
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


class ComputeRegionBackendService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service google_compute_region_backend_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        affinity_cookie_ttl_sec: typing.Optional[jsii.Number] = None,
        backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionBackendServiceBackend", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cdn_policy: typing.Optional[typing.Union["ComputeRegionBackendServiceCdnPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        circuit_breakers: typing.Optional[typing.Union["ComputeRegionBackendServiceCircuitBreakers", typing.Dict[builtins.str, typing.Any]]] = None,
        connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
        consistent_hash: typing.Optional[typing.Union["ComputeRegionBackendServiceConsistentHash", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionBackendServiceCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failover_policy: typing.Optional[typing.Union["ComputeRegionBackendServiceFailoverPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        iap: typing.Optional[typing.Union["ComputeRegionBackendServiceIap", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address_selection_policy: typing.Optional[builtins.str] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        locality_lb_policy: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["ComputeRegionBackendServiceLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[builtins.str] = None,
        outlier_detection: typing.Optional[typing.Union["ComputeRegionBackendServiceOutlierDetection", typing.Dict[builtins.str, typing.Any]]] = None,
        port_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        strong_session_affinity_cookie: typing.Optional[typing.Union["ComputeRegionBackendServiceStrongSessionAffinityCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionBackendServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_sec: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service google_compute_region_backend_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#name ComputeRegionBackendService#name}
        :param affinity_cookie_ttl_sec: Lifetime of cookies in seconds if session_affinity is GENERATED_COOKIE. If set to 0, the cookie is non-persistent and lasts only until the end of the browser session (or equivalent). The maximum allowed value for TTL is one day. When the load balancing scheme is INTERNAL, this field is not used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#affinity_cookie_ttl_sec ComputeRegionBackendService#affinity_cookie_ttl_sec}
        :param backend: backend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#backend ComputeRegionBackendService#backend}
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#cdn_policy ComputeRegionBackendService#cdn_policy}
        :param circuit_breakers: circuit_breakers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#circuit_breakers ComputeRegionBackendService#circuit_breakers}
        :param connection_draining_timeout_sec: Time for which instance will be drained (not accept new connections, but still work to finish started). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#connection_draining_timeout_sec ComputeRegionBackendService#connection_draining_timeout_sec}
        :param consistent_hash: consistent_hash block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#consistent_hash ComputeRegionBackendService#consistent_hash}
        :param custom_metrics: custom_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#custom_metrics ComputeRegionBackendService#custom_metrics}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#description ComputeRegionBackendService#description}
        :param enable_cdn: If true, enable Cloud CDN for this RegionBackendService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enable_cdn ComputeRegionBackendService#enable_cdn}
        :param failover_policy: failover_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#failover_policy ComputeRegionBackendService#failover_policy}
        :param health_checks: The set of URLs to HealthCheck resources for health checking this RegionBackendService. Currently at most one health check can be specified. A health check must be specified unless the backend service uses an internet or serverless NEG as a backend. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#health_checks ComputeRegionBackendService#health_checks}
        :param iap: iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#iap ComputeRegionBackendService#iap}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#id ComputeRegionBackendService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address_selection_policy: Specifies preference of traffic to the backend (from the proxy and from the client for proxyless gRPC). Possible values: ["IPV4_ONLY", "PREFER_IPV6", "IPV6_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#ip_address_selection_policy ComputeRegionBackendService#ip_address_selection_policy}
        :param load_balancing_scheme: Indicates what kind of load balancing this regional backend service will be used for. A backend service created for one type of load balancing cannot be used with the other(s). For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_. Default value: "INTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL", "INTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#load_balancing_scheme ComputeRegionBackendService#load_balancing_scheme}
        :param locality_lb_policy: The load balancing algorithm used within the scope of the locality. The possible values are:. - 'ROUND_ROBIN': This is a simple policy in which each healthy backend is selected in round robin order. - 'LEAST_REQUEST': An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests. - 'RING_HASH': The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests. - 'RANDOM': The load balancer selects a random healthy host. - 'ORIGINAL_DESTINATION': Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer. - 'MAGLEV': used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, refer to https://ai.google/research/pubs/pub44824 - 'WEIGHTED_MAGLEV': Per-instance weighted Load Balancing via health check reported weights. Only applicable to loadBalancingScheme EXTERNAL. If set, the Backend Service must configure a non legacy HTTP-based Health Check, and health check replies are expected to contain non-standard HTTP response header field X-Load-Balancing-Endpoint-Weight to specify the per-instance weights. If set, Load Balancing is weight based on the per-instance weights reported in the last processed health check replies, as long as every instance either reported a valid weight or had UNAVAILABLE_WEIGHT. Otherwise, Load Balancing remains equal-weight. - 'WEIGHTED_ROUND_ROBIN': Per-endpoint weighted round-robin Load Balancing using weights computed from Backend reported Custom Metrics. If set, the Backend Service responses are expected to contain non-standard HTTP response header field X-Endpoint-Load-Metrics. The reported metrics to use for computing the weights are specified via the backends[].customMetrics fields. locality_lb_policy is applicable to either: - A regional backend service with the service_protocol set to HTTP, HTTPS, HTTP2 or H2C, and loadBalancingScheme set to INTERNAL_MANAGED. - A global backend service with the load_balancing_scheme set to INTERNAL_SELF_MANAGED. - A regional backend service with loadBalancingScheme set to EXTERNAL (External Network Load Balancing). Only MAGLEV and WEIGHTED_MAGLEV values are possible for External Network Load Balancing. The default is MAGLEV. If session_affinity is not NONE, and locality_lb_policy is not set to MAGLEV, WEIGHTED_MAGLEV, or RING_HASH, session affinity settings will not take effect. Only ROUND_ROBIN and RING_HASH are supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validate_for_proxyless field set to true. Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV", "WEIGHTED_MAGLEV", "WEIGHTED_ROUND_ROBIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#locality_lb_policy ComputeRegionBackendService#locality_lb_policy}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#log_config ComputeRegionBackendService#log_config}
        :param network: The URL of the network to which this backend service belongs. This field can only be specified when the load balancing scheme is set to INTERNAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#network ComputeRegionBackendService#network}
        :param outlier_detection: outlier_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#outlier_detection ComputeRegionBackendService#outlier_detection}
        :param port_name: A named port on a backend instance group representing the port for communication to the backend VMs in that group. Required when the loadBalancingScheme is EXTERNAL, EXTERNAL_MANAGED, INTERNAL_MANAGED, or INTERNAL_SELF_MANAGED and the backends are instance groups. The named port must be defined on each backend instance group. This parameter has no meaning if the backends are NEGs. API sets a default of "http" if not given. Must be omitted when the loadBalancingScheme is INTERNAL (Internal TCP/UDP Load Balancing). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#port_name ComputeRegionBackendService#port_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#project ComputeRegionBackendService#project}.
        :param protocol: The protocol this BackendService uses to communicate with backends. The default is HTTP. Possible values are HTTP, HTTPS, HTTP2, H2C, TCP, SSL, UDP or GRPC. Refer to the documentation for the load balancers or for Traffic Director for more information. Possible values: ["HTTP", "HTTPS", "HTTP2", "TCP", "SSL", "UDP", "GRPC", "UNSPECIFIED", "H2C"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#protocol ComputeRegionBackendService#protocol}
        :param region: The Region in which the created backend service should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#region ComputeRegionBackendService#region}
        :param session_affinity: Type of session affinity to use. The default is NONE. Session affinity is not applicable if the protocol is UDP. Possible values: ["NONE", "CLIENT_IP", "CLIENT_IP_PORT_PROTO", "CLIENT_IP_PROTO", "GENERATED_COOKIE", "HEADER_FIELD", "HTTP_COOKIE", "CLIENT_IP_NO_DESTINATION", "STRONG_COOKIE_AFFINITY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#session_affinity ComputeRegionBackendService#session_affinity}
        :param strong_session_affinity_cookie: strong_session_affinity_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#strong_session_affinity_cookie ComputeRegionBackendService#strong_session_affinity_cookie}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#timeouts ComputeRegionBackendService#timeouts}
        :param timeout_sec: The backend service timeout has a different meaning depending on the type of load balancer. For more information see, `Backend service settings <https://cloud.google.com/compute/docs/reference/rest/v1/backendServices>`_. The default is 30 seconds. The full range of timeout values allowed goes from 1 through 2,147,483,647 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#timeout_sec ComputeRegionBackendService#timeout_sec}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a7d193a662f1e9eb4abcaa96ce0135d0dd9f195f8f24db270c1567f4623d748)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRegionBackendServiceConfig(
            name=name,
            affinity_cookie_ttl_sec=affinity_cookie_ttl_sec,
            backend=backend,
            cdn_policy=cdn_policy,
            circuit_breakers=circuit_breakers,
            connection_draining_timeout_sec=connection_draining_timeout_sec,
            consistent_hash=consistent_hash,
            custom_metrics=custom_metrics,
            description=description,
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
            session_affinity=session_affinity,
            strong_session_affinity_cookie=strong_session_affinity_cookie,
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
        '''Generates CDKTF code for importing a ComputeRegionBackendService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRegionBackendService to import.
        :param import_from_id: The id of the existing ComputeRegionBackendService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRegionBackendService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1c489a40d0b1d2011dcead9940c2ccc75e15677f4f938843b5f16e0495c23a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackend")
    def put_backend(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionBackendServiceBackend", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__705381bd496efb783ebe0f0ad360b9465d3fa796207cea7a63f6cb943ca18d55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackend", [value]))

    @jsii.member(jsii_name="putCdnPolicy")
    def put_cdn_policy(
        self,
        *,
        cache_key_policy: typing.Optional[typing.Union["ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[jsii.Number] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        max_ttl: typing.Optional[jsii.Number] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        serve_while_stale: typing.Optional[jsii.Number] = None,
        signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#cache_key_policy ComputeRegionBackendService#cache_key_policy}
        :param cache_mode: Specifies the cache setting for all responses from this backend. The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#cache_mode ComputeRegionBackendService#cache_mode}
        :param client_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#client_ttl ComputeRegionBackendService#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#default_ttl ComputeRegionBackendService#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_ttl ComputeRegionBackendService#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#negative_caching ComputeRegionBackendService#negative_caching}
        :param negative_caching_policy: negative_caching_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#negative_caching_policy ComputeRegionBackendService#negative_caching_policy}
        :param serve_while_stale: Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#serve_while_stale ComputeRegionBackendService#serve_while_stale}
        :param signed_url_cache_max_age_sec: Maximum number of seconds the response to a signed URL request will be considered fresh, defaults to 1hr (3600s). After this time period, the response will be revalidated before being served. When serving responses to signed URL requests, Cloud CDN will internally behave as though all responses from this backend had a "Cache-Control: public, max-age=[TTL]" header, regardless of any existing Cache-Control header. The actual headers served in responses will not be altered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#signed_url_cache_max_age_sec ComputeRegionBackendService#signed_url_cache_max_age_sec}
        '''
        value = ComputeRegionBackendServiceCdnPolicy(
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
        max_connections: typing.Optional[jsii.Number] = None,
        max_pending_requests: typing.Optional[jsii.Number] = None,
        max_requests: typing.Optional[jsii.Number] = None,
        max_requests_per_connection: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_connections: The maximum number of connections to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_connections ComputeRegionBackendService#max_connections}
        :param max_pending_requests: The maximum number of pending requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_pending_requests ComputeRegionBackendService#max_pending_requests}
        :param max_requests: The maximum number of parallel requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_requests ComputeRegionBackendService#max_requests}
        :param max_requests_per_connection: Maximum requests for a single backend connection. This parameter is respected by both the HTTP/1.1 and HTTP/2 implementations. If not specified, there is no limit. Setting this parameter to 1 will effectively disable keep alive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_requests_per_connection ComputeRegionBackendService#max_requests_per_connection}
        :param max_retries: The maximum number of parallel retries to the backend cluster. Defaults to 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_retries ComputeRegionBackendService#max_retries}
        '''
        value = ComputeRegionBackendServiceCircuitBreakers(
            max_connections=max_connections,
            max_pending_requests=max_pending_requests,
            max_requests=max_requests,
            max_requests_per_connection=max_requests_per_connection,
            max_retries=max_retries,
        )

        return typing.cast(None, jsii.invoke(self, "putCircuitBreakers", [value]))

    @jsii.member(jsii_name="putConsistentHash")
    def put_consistent_hash(
        self,
        *,
        http_cookie: typing.Optional[typing.Union["ComputeRegionBackendServiceConsistentHashHttpCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        http_header_name: typing.Optional[builtins.str] = None,
        minimum_ring_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_cookie: http_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#http_cookie ComputeRegionBackendService#http_cookie}
        :param http_header_name: The hash based on the value of the specified header field. This field is applicable if the sessionAffinity is set to HEADER_FIELD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#http_header_name ComputeRegionBackendService#http_header_name}
        :param minimum_ring_size: The minimum number of virtual nodes to use for the hash ring. Larger ring sizes result in more granular load distributions. If the number of hosts in the load balancing pool is larger than the ring size, each host will be assigned a single virtual node. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#minimum_ring_size ComputeRegionBackendService#minimum_ring_size}
        '''
        value = ComputeRegionBackendServiceConsistentHash(
            http_cookie=http_cookie,
            http_header_name=http_header_name,
            minimum_ring_size=minimum_ring_size,
        )

        return typing.cast(None, jsii.invoke(self, "putConsistentHash", [value]))

    @jsii.member(jsii_name="putCustomMetrics")
    def put_custom_metrics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionBackendServiceCustomMetrics", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec60033f7de262bba5265cc6c164f9485c8b95f71ab9eeae5eb7d492670f422d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomMetrics", [value]))

    @jsii.member(jsii_name="putFailoverPolicy")
    def put_failover_policy(
        self,
        *,
        disable_connection_drain_on_failover: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_traffic_if_unhealthy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failover_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disable_connection_drain_on_failover: On failover or failback, this field indicates whether connection drain will be honored. Setting this to true has the following effect: connections to the old active pool are not drained. Connections to the new active pool use the timeout of 10 min (currently fixed). Setting to false has the following effect: both old and new connections will have a drain timeout of 10 min. This can be set to true only if the protocol is TCP. The default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#disable_connection_drain_on_failover ComputeRegionBackendService#disable_connection_drain_on_failover}
        :param drop_traffic_if_unhealthy: This option is used only when no healthy VMs are detected in the primary and backup instance groups. When set to true, traffic is dropped. When set to false, new connections are sent across all VMs in the primary group. The default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#drop_traffic_if_unhealthy ComputeRegionBackendService#drop_traffic_if_unhealthy}
        :param failover_ratio: The value of the field must be in [0, 1]. If the ratio of the healthy VMs in the primary backend is at or below this number, traffic arriving at the load-balanced IP will be directed to the failover backend. In case where 'failoverRatio' is not set or all the VMs in the backup backend are unhealthy, the traffic will be directed back to the primary backend in the "force" mode, where traffic will be spread to the healthy VMs with the best effort, or to all VMs when no VM is healthy. This field is only used with l4 load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#failover_ratio ComputeRegionBackendService#failover_ratio}
        '''
        value = ComputeRegionBackendServiceFailoverPolicy(
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
        :param enabled: Whether the serving infrastructure will authenticate and authorize all incoming requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enabled ComputeRegionBackendService#enabled}
        :param oauth2_client_id: OAuth2 Client ID for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#oauth2_client_id ComputeRegionBackendService#oauth2_client_id}
        :param oauth2_client_secret: OAuth2 Client Secret for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#oauth2_client_secret ComputeRegionBackendService#oauth2_client_secret}
        '''
        value = ComputeRegionBackendServiceIap(
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
        :param enable: Whether to enable logging for the load balancer traffic served by this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enable ComputeRegionBackendService#enable}
        :param optional_fields: Specifies the fields to include in logging. This field can only be specified if logging is enabled for this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#optional_fields ComputeRegionBackendService#optional_fields}
        :param optional_mode: Specifies the optional logging mode for the load balancer traffic. Supported values: INCLUDE_ALL_OPTIONAL, EXCLUDE_ALL_OPTIONAL, CUSTOM. Possible values: ["INCLUDE_ALL_OPTIONAL", "EXCLUDE_ALL_OPTIONAL", "CUSTOM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#optional_mode ComputeRegionBackendService#optional_mode}
        :param sample_rate: This field can only be specified if logging is enabled for this backend service. The value of the field must be in [0, 1]. This configures the sampling rate of requests to the load balancer where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#sample_rate ComputeRegionBackendService#sample_rate}
        '''
        value = ComputeRegionBackendServiceLogConfig(
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
        base_ejection_time: typing.Optional[typing.Union["ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime", typing.Dict[builtins.str, typing.Any]]] = None,
        consecutive_errors: typing.Optional[jsii.Number] = None,
        consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_errors: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_success_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[typing.Union["ComputeRegionBackendServiceOutlierDetectionInterval", typing.Dict[builtins.str, typing.Any]]] = None,
        max_ejection_percent: typing.Optional[jsii.Number] = None,
        success_rate_minimum_hosts: typing.Optional[jsii.Number] = None,
        success_rate_request_volume: typing.Optional[jsii.Number] = None,
        success_rate_stdev_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param base_ejection_time: base_ejection_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#base_ejection_time ComputeRegionBackendService#base_ejection_time}
        :param consecutive_errors: Number of errors before a host is ejected from the connection pool. When the backend host is accessed over HTTP, a 5xx return code qualifies as an error. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#consecutive_errors ComputeRegionBackendService#consecutive_errors}
        :param consecutive_gateway_failure: The number of consecutive gateway failures (502, 503, 504 status or connection errors that are mapped to one of those status codes) before a consecutive gateway failure ejection occurs. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#consecutive_gateway_failure ComputeRegionBackendService#consecutive_gateway_failure}
        :param enforcing_consecutive_errors: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive 5xx. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enforcing_consecutive_errors ComputeRegionBackendService#enforcing_consecutive_errors}
        :param enforcing_consecutive_gateway_failure: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive gateway failures. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enforcing_consecutive_gateway_failure ComputeRegionBackendService#enforcing_consecutive_gateway_failure}
        :param enforcing_success_rate: The percentage chance that a host will be actually ejected when an outlier status is detected through success rate statistics. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enforcing_success_rate ComputeRegionBackendService#enforcing_success_rate}
        :param interval: interval block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#interval ComputeRegionBackendService#interval}
        :param max_ejection_percent: Maximum percentage of hosts in the load balancing pool for the backend service that can be ejected. Defaults to 10%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_ejection_percent ComputeRegionBackendService#max_ejection_percent}
        :param success_rate_minimum_hosts: The number of hosts in a cluster that must have enough request volume to detect success rate outliers. If the number of hosts is less than this setting, outlier detection via success rate statistics is not performed for any host in the cluster. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#success_rate_minimum_hosts ComputeRegionBackendService#success_rate_minimum_hosts}
        :param success_rate_request_volume: The minimum number of total requests that must be collected in one interval (as defined by the interval duration above) to include this host in success rate based outlier detection. If the volume is lower than this setting, outlier detection via success rate statistics is not performed for that host. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#success_rate_request_volume ComputeRegionBackendService#success_rate_request_volume}
        :param success_rate_stdev_factor: This factor is used to determine the ejection threshold for success rate outlier ejection. The ejection threshold is the difference between the mean success rate, and the product of this factor and the standard deviation of the mean success rate: mean - (stdev * success_rate_stdev_factor). This factor is divided by a thousand to get a double. That is, if the desired factor is 1.9, the runtime value should be 1900. Defaults to 1900. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#success_rate_stdev_factor ComputeRegionBackendService#success_rate_stdev_factor}
        '''
        value = ComputeRegionBackendServiceOutlierDetection(
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
        ttl: typing.Optional[typing.Union["ComputeRegionBackendServiceStrongSessionAffinityCookieTtl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#name ComputeRegionBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#path ComputeRegionBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#ttl ComputeRegionBackendService#ttl}
        '''
        value = ComputeRegionBackendServiceStrongSessionAffinityCookie(
            name=name, path=path, ttl=ttl
        )

        return typing.cast(None, jsii.invoke(self, "putStrongSessionAffinityCookie", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#create ComputeRegionBackendService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#delete ComputeRegionBackendService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#update ComputeRegionBackendService#update}.
        '''
        value = ComputeRegionBackendServiceTimeouts(
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

    @jsii.member(jsii_name="resetConsistentHash")
    def reset_consistent_hash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsistentHash", []))

    @jsii.member(jsii_name="resetCustomMetrics")
    def reset_custom_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomMetrics", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

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

    @jsii.member(jsii_name="resetSessionAffinity")
    def reset_session_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinity", []))

    @jsii.member(jsii_name="resetStrongSessionAffinityCookie")
    def reset_strong_session_affinity_cookie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrongSessionAffinityCookie", []))

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
    def backend(self) -> "ComputeRegionBackendServiceBackendList":
        return typing.cast("ComputeRegionBackendServiceBackendList", jsii.get(self, "backend"))

    @builtins.property
    @jsii.member(jsii_name="cdnPolicy")
    def cdn_policy(self) -> "ComputeRegionBackendServiceCdnPolicyOutputReference":
        return typing.cast("ComputeRegionBackendServiceCdnPolicyOutputReference", jsii.get(self, "cdnPolicy"))

    @builtins.property
    @jsii.member(jsii_name="circuitBreakers")
    def circuit_breakers(
        self,
    ) -> "ComputeRegionBackendServiceCircuitBreakersOutputReference":
        return typing.cast("ComputeRegionBackendServiceCircuitBreakersOutputReference", jsii.get(self, "circuitBreakers"))

    @builtins.property
    @jsii.member(jsii_name="consistentHash")
    def consistent_hash(
        self,
    ) -> "ComputeRegionBackendServiceConsistentHashOutputReference":
        return typing.cast("ComputeRegionBackendServiceConsistentHashOutputReference", jsii.get(self, "consistentHash"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="customMetrics")
    def custom_metrics(self) -> "ComputeRegionBackendServiceCustomMetricsList":
        return typing.cast("ComputeRegionBackendServiceCustomMetricsList", jsii.get(self, "customMetrics"))

    @builtins.property
    @jsii.member(jsii_name="failoverPolicy")
    def failover_policy(
        self,
    ) -> "ComputeRegionBackendServiceFailoverPolicyOutputReference":
        return typing.cast("ComputeRegionBackendServiceFailoverPolicyOutputReference", jsii.get(self, "failoverPolicy"))

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
    def iap(self) -> "ComputeRegionBackendServiceIapOutputReference":
        return typing.cast("ComputeRegionBackendServiceIapOutputReference", jsii.get(self, "iap"))

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(self) -> "ComputeRegionBackendServiceLogConfigOutputReference":
        return typing.cast("ComputeRegionBackendServiceLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="outlierDetection")
    def outlier_detection(
        self,
    ) -> "ComputeRegionBackendServiceOutlierDetectionOutputReference":
        return typing.cast("ComputeRegionBackendServiceOutlierDetectionOutputReference", jsii.get(self, "outlierDetection"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="strongSessionAffinityCookie")
    def strong_session_affinity_cookie(
        self,
    ) -> "ComputeRegionBackendServiceStrongSessionAffinityCookieOutputReference":
        return typing.cast("ComputeRegionBackendServiceStrongSessionAffinityCookieOutputReference", jsii.get(self, "strongSessionAffinityCookie"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRegionBackendServiceTimeoutsOutputReference":
        return typing.cast("ComputeRegionBackendServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="affinityCookieTtlSecInput")
    def affinity_cookie_ttl_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "affinityCookieTtlSecInput"))

    @builtins.property
    @jsii.member(jsii_name="backendInput")
    def backend_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionBackendServiceBackend"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionBackendServiceBackend"]]], jsii.get(self, "backendInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnPolicyInput")
    def cdn_policy_input(
        self,
    ) -> typing.Optional["ComputeRegionBackendServiceCdnPolicy"]:
        return typing.cast(typing.Optional["ComputeRegionBackendServiceCdnPolicy"], jsii.get(self, "cdnPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="circuitBreakersInput")
    def circuit_breakers_input(
        self,
    ) -> typing.Optional["ComputeRegionBackendServiceCircuitBreakers"]:
        return typing.cast(typing.Optional["ComputeRegionBackendServiceCircuitBreakers"], jsii.get(self, "circuitBreakersInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionDrainingTimeoutSecInput")
    def connection_draining_timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectionDrainingTimeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="consistentHashInput")
    def consistent_hash_input(
        self,
    ) -> typing.Optional["ComputeRegionBackendServiceConsistentHash"]:
        return typing.cast(typing.Optional["ComputeRegionBackendServiceConsistentHash"], jsii.get(self, "consistentHashInput"))

    @builtins.property
    @jsii.member(jsii_name="customMetricsInput")
    def custom_metrics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionBackendServiceCustomMetrics"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionBackendServiceCustomMetrics"]]], jsii.get(self, "customMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    ) -> typing.Optional["ComputeRegionBackendServiceFailoverPolicy"]:
        return typing.cast(typing.Optional["ComputeRegionBackendServiceFailoverPolicy"], jsii.get(self, "failoverPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="healthChecksInput")
    def health_checks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "healthChecksInput"))

    @builtins.property
    @jsii.member(jsii_name="iapInput")
    def iap_input(self) -> typing.Optional["ComputeRegionBackendServiceIap"]:
        return typing.cast(typing.Optional["ComputeRegionBackendServiceIap"], jsii.get(self, "iapInput"))

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
    ) -> typing.Optional["ComputeRegionBackendServiceLogConfig"]:
        return typing.cast(typing.Optional["ComputeRegionBackendServiceLogConfig"], jsii.get(self, "logConfigInput"))

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
    ) -> typing.Optional["ComputeRegionBackendServiceOutlierDetection"]:
        return typing.cast(typing.Optional["ComputeRegionBackendServiceOutlierDetection"], jsii.get(self, "outlierDetectionInput"))

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
    @jsii.member(jsii_name="sessionAffinityInput")
    def session_affinity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="strongSessionAffinityCookieInput")
    def strong_session_affinity_cookie_input(
        self,
    ) -> typing.Optional["ComputeRegionBackendServiceStrongSessionAffinityCookie"]:
        return typing.cast(typing.Optional["ComputeRegionBackendServiceStrongSessionAffinityCookie"], jsii.get(self, "strongSessionAffinityCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecInput")
    def timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionBackendServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionBackendServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="affinityCookieTtlSec")
    def affinity_cookie_ttl_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "affinityCookieTtlSec"))

    @affinity_cookie_ttl_sec.setter
    def affinity_cookie_ttl_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52c9500e4e9fa93a91b304c7e3e135ccf3d7f2a324b03504bc533c94c5a2df32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "affinityCookieTtlSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionDrainingTimeoutSec")
    def connection_draining_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectionDrainingTimeoutSec"))

    @connection_draining_timeout_sec.setter
    def connection_draining_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562c8e062732203e76fac17c68d7268e9b836f2e291e4137b9d74474d5235398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionDrainingTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306edbc75d0eb09cd430efdaaa8fe4ba6cca369f0343b0685ace0323a1801649)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74f99af0ba03bc970ff0be137026d8fb594305f0ca1bd95bda538343ad7fae74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableCdn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthChecks")
    def health_checks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "healthChecks"))

    @health_checks.setter
    def health_checks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba169d163fd0341ebbbfce11a9608f6e5b63e1a95308893e2731f7c62e35e35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthChecks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0969e93341a32202ba7e523eca85fd1ee559e04f9d426de5310155b1cbbb02c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressSelectionPolicy")
    def ip_address_selection_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressSelectionPolicy"))

    @ip_address_selection_policy.setter
    def ip_address_selection_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ac0ee0f0f2eeaa2b07bee93f26ecc5cc20217e4db90a75b0dff430377397d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressSelectionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingScheme")
    def load_balancing_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingScheme"))

    @load_balancing_scheme.setter
    def load_balancing_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09da2d78ec50a281748ef4e20814f3f26e79186dea33f8ac2e95723aec8c35e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localityLbPolicy")
    def locality_lb_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localityLbPolicy"))

    @locality_lb_policy.setter
    def locality_lb_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8506a937369ced4764e829b71f8065eedb9f3a7c2570925faea401e3f50db486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localityLbPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55621c9e6967bdd01d61bfa1a858a6202f0b5315cd29ba41c2e209758ce86117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ebfe702142c520c92089bdb02cba19284e5d5acb56a2fd2c617b5686d4f37e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portName")
    def port_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portName"))

    @port_name.setter
    def port_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c666b75001d11f84a61aa1c90cebb2ab4672e55a574076652e3a0bc126fbaf9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333ec9777f8f7c081037d0b0ddccd0b02c8518c449592f3684754045d9a1f749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c43d834b72384b1d30c53e2abadcde998a0e82887efb5b9facc6b030754f79a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88dfda43761cc9369b3092358ef4f0ead987146f7b0686be2cd2398686706989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionAffinity")
    def session_affinity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionAffinity"))

    @session_affinity.setter
    def session_affinity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94abaa06d37269786924a92c0395e3fcd0057dce5ec470ee0d4ad0525e8e87dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSec")
    def timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSec"))

    @timeout_sec.setter
    def timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3297937f636756385624c47a28ecd8391715e93182b1a77e7f5a54f6a1c8b2e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSec", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceBackend",
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
class ComputeRegionBackendServiceBackend:
    def __init__(
        self,
        *,
        group: builtins.str,
        balancing_mode: typing.Optional[builtins.str] = None,
        capacity_scaler: typing.Optional[jsii.Number] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionBackendServiceBackendCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param group: The fully-qualified URL of an Instance Group or Network Endpoint Group resource. In case of instance group this defines the list of instances that serve traffic. Member virtual machine instances from each instance group must live in the same zone as the instance group itself. No two backends in a backend service are allowed to use same Instance Group resource. For Network Endpoint Groups this defines list of endpoints. All endpoints of Network Endpoint Group must be hosted on instances located in the same zone as the Network Endpoint Group. Backend services cannot mix Instance Group and Network Endpoint Group backends. When the 'load_balancing_scheme' is INTERNAL, only instance groups are supported. Note that you must specify an Instance Group or Network Endpoint Group resource using the fully-qualified URL, rather than a partial URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#group ComputeRegionBackendService#group}
        :param balancing_mode: Specifies the balancing mode for this backend. See the `Backend Services Overview <https://cloud.google.com/load-balancing/docs/backend-service#balancing-mode>`_ for an explanation of load balancing modes. Default value: "UTILIZATION" Possible values: ["UTILIZATION", "RATE", "CONNECTION", "CUSTOM_METRICS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#balancing_mode ComputeRegionBackendService#balancing_mode}
        :param capacity_scaler: A multiplier applied to the group's maximum servicing capacity (based on UTILIZATION, RATE or CONNECTION). ~>**NOTE**: This field cannot be set for INTERNAL region backend services (default loadBalancingScheme), but is required for non-INTERNAL backend service. The total capacity_scaler for all backends must be non-zero. A setting of 0 means the group is completely drained, offering 0% of its available Capacity. Valid range is [0.0,1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#capacity_scaler ComputeRegionBackendService#capacity_scaler}
        :param custom_metrics: custom_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#custom_metrics ComputeRegionBackendService#custom_metrics}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#description ComputeRegionBackendService#description}
        :param failover: This field designates whether this is a failover backend. More than one failover backend can be configured for a given RegionBackendService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#failover ComputeRegionBackendService#failover}
        :param max_connections: The max number of simultaneous connections for the group. Can be used with either CONNECTION or UTILIZATION balancing modes. Cannot be set for INTERNAL backend services. For CONNECTION mode, either maxConnections or one of maxConnectionsPerInstance or maxConnectionsPerEndpoint, as appropriate for group type, must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_connections ComputeRegionBackendService#max_connections}
        :param max_connections_per_endpoint: The max number of simultaneous connections that a single backend network endpoint can handle. Cannot be set for INTERNAL backend services. This is used to calculate the capacity of the group. Can be used in either CONNECTION or UTILIZATION balancing modes. For CONNECTION mode, either maxConnections or maxConnectionsPerEndpoint must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_connections_per_endpoint ComputeRegionBackendService#max_connections_per_endpoint}
        :param max_connections_per_instance: The max number of simultaneous connections that a single backend instance can handle. Cannot be set for INTERNAL backend services. This is used to calculate the capacity of the group. Can be used in either CONNECTION or UTILIZATION balancing modes. For CONNECTION mode, either maxConnections or maxConnectionsPerInstance must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_connections_per_instance ComputeRegionBackendService#max_connections_per_instance}
        :param max_rate: The max requests per second (RPS) of the group. Cannot be set for INTERNAL backend services. Can be used with either RATE or UTILIZATION balancing modes, but required if RATE mode. Either maxRate or one of maxRatePerInstance or maxRatePerEndpoint, as appropriate for group type, must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_rate ComputeRegionBackendService#max_rate}
        :param max_rate_per_endpoint: The max requests per second (RPS) that a single backend network endpoint can handle. This is used to calculate the capacity of the group. Can be used in either balancing mode. For RATE mode, either maxRate or maxRatePerEndpoint must be set. Cannot be set for INTERNAL backend services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_rate_per_endpoint ComputeRegionBackendService#max_rate_per_endpoint}
        :param max_rate_per_instance: The max requests per second (RPS) that a single backend instance can handle. This is used to calculate the capacity of the group. Can be used in either balancing mode. For RATE mode, either maxRate or maxRatePerInstance must be set. Cannot be set for INTERNAL backend services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_rate_per_instance ComputeRegionBackendService#max_rate_per_instance}
        :param max_utilization: Used when balancingMode is UTILIZATION. This ratio defines the CPU utilization target for the group. Valid range is [0.0, 1.0]. Cannot be set for INTERNAL backend services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_utilization ComputeRegionBackendService#max_utilization}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a84ffd6da46f54b7caae12c227efde4a29b7de94f73341429b4bb6ce82854084)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#group ComputeRegionBackendService#group}
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def balancing_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the balancing mode for this backend.

        See the `Backend Services Overview <https://cloud.google.com/load-balancing/docs/backend-service#balancing-mode>`_
        for an explanation of load balancing modes. Default value: "UTILIZATION" Possible values: ["UTILIZATION", "RATE", "CONNECTION", "CUSTOM_METRICS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#balancing_mode ComputeRegionBackendService#balancing_mode}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#capacity_scaler ComputeRegionBackendService#capacity_scaler}
        '''
        result = self._values.get("capacity_scaler")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_metrics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionBackendServiceBackendCustomMetrics"]]]:
        '''custom_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#custom_metrics ComputeRegionBackendService#custom_metrics}
        '''
        result = self._values.get("custom_metrics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionBackendServiceBackendCustomMetrics"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#description ComputeRegionBackendService#description}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#failover ComputeRegionBackendService#failover}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_connections ComputeRegionBackendService#max_connections}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_connections_per_endpoint ComputeRegionBackendService#max_connections_per_endpoint}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_connections_per_instance ComputeRegionBackendService#max_connections_per_instance}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_rate ComputeRegionBackendService#max_rate}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_rate_per_endpoint ComputeRegionBackendService#max_rate_per_endpoint}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_rate_per_instance ComputeRegionBackendService#max_rate_per_instance}
        '''
        result = self._values.get("max_rate_per_instance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_utilization(self) -> typing.Optional[jsii.Number]:
        '''Used when balancingMode is UTILIZATION.

        This ratio defines the
        CPU utilization target for the group. Valid range is [0.0, 1.0].
        Cannot be set for INTERNAL backend services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_utilization ComputeRegionBackendService#max_utilization}
        '''
        result = self._values.get("max_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceBackend(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceBackendCustomMetrics",
    jsii_struct_bases=[],
    name_mapping={
        "dry_run": "dryRun",
        "name": "name",
        "max_utilization": "maxUtilization",
    },
)
class ComputeRegionBackendServiceBackendCustomMetrics:
    def __init__(
        self,
        *,
        dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        max_utilization: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param dry_run: If true, the metric data is collected and reported to Cloud Monitoring, but is not used for load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#dry_run ComputeRegionBackendService#dry_run}
        :param name: Name of a custom utilization signal. The name must be 1-64 characters long and match the regular expression `a-z <%5B-_.a-z0-9%5D*%5Ba-z0-9%5D>`_? which means the first character must be a lowercase letter, and all following characters must be a dash, period, underscore, lowercase letter, or digit, except the last character, which cannot be a dash, period, or underscore. For usage guidelines, see Custom Metrics balancing mode. This field can only be used for a global or regional backend service with the loadBalancingScheme set to EXTERNAL_MANAGED, INTERNAL_MANAGED INTERNAL_SELF_MANAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#name ComputeRegionBackendService#name}
        :param max_utilization: Optional parameter to define a target utilization for the Custom Metrics balancing mode. The valid range is [0.0, 1.0]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_utilization ComputeRegionBackendService#max_utilization}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130c3901929158e06b86da89d4571f764fae179ba8ef51f68bff75a32ee20d3e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#dry_run ComputeRegionBackendService#dry_run}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#name ComputeRegionBackendService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_utilization(self) -> typing.Optional[jsii.Number]:
        '''Optional parameter to define a target utilization for the Custom Metrics balancing mode. The valid range is [0.0, 1.0].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_utilization ComputeRegionBackendService#max_utilization}
        '''
        result = self._values.get("max_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceBackendCustomMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceBackendCustomMetricsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceBackendCustomMetricsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e907b8f41b47fa050dac6f72acef38a5aa3527ce800258dc6c54205f7ef749ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionBackendServiceBackendCustomMetricsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045c42abd849ab15a60bc8eeaa2be4d6351b44f8bf9eb86e307cb4df8007f995)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionBackendServiceBackendCustomMetricsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc43e141c5a01617ab39574e5a31d729bfe3b7377109b1911fe8d0be082b582)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e83a453daf016c3e618f8806c18096154b09e4fbf51cae3a0decdf47577ce949)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59d3cd5e6fcd01fd1dd4e9691a6c11ccfe22962451c2402634828aef62011b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceBackendCustomMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceBackendCustomMetrics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceBackendCustomMetrics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1dbaf6236eb1a270cb18a5e19743a5150638832766eca96f863983226a1e8b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionBackendServiceBackendCustomMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceBackendCustomMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f302beba5cc705c9c1b55ea95d0d17159907c51fa08d957f9b049889f2383029)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1aafd438a07f357a3f32c827753c2dd7b1d11add84af84249ae4be324300158b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dryRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUtilization")
    def max_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUtilization"))

    @max_utilization.setter
    def max_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2249c26bf6154d3dde47d84dbb496cda52fe52c116cea61232025424e1513640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab537b52277742ee60d59293531cbb3b8dbf02478a44c8b40b16353657c30b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceBackendCustomMetrics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceBackendCustomMetrics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceBackendCustomMetrics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cafcc1d2c7289b088ba6bf00b6db6e95805d3fe7d4719239ed12e34aec325e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionBackendServiceBackendList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceBackendList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33ad42b62c7034037df6fc0e372a47ce12ed5f93d1047398fff955799fe8755c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionBackendServiceBackendOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02ae8c7d4c6acec6fc1cb094ec69c8816cc8abeb6c377db26a31e7ec4c4004a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionBackendServiceBackendOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028f467394e4f5484d38e2d9f947ae8a9de767c733136d6400bc0df293924768)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9871a41436307fb3773b0f8858a5f8765984313d301f66c5350dd168a360ba8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__459f5d087073020ef953274782f3c5fb40b6e8081ac3f9b7b6bb4b7a26ff62f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceBackend]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceBackend]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceBackend]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73780d72a57dc4a7a334bb18f154754c4810a2a6351aaaaf535b669624adaedf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionBackendServiceBackendOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceBackendOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d60ce72a29b9b8de82524f272e9c3c7f49ec5af24b170508559ba4020de545dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomMetrics")
    def put_custom_metrics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionBackendServiceBackendCustomMetrics, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f300eacb5a35cd587e8be25d170b826b16cb4e9bc66eb68336ffed6487b3fca)
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
    def custom_metrics(self) -> ComputeRegionBackendServiceBackendCustomMetricsList:
        return typing.cast(ComputeRegionBackendServiceBackendCustomMetricsList, jsii.get(self, "customMetrics"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceBackendCustomMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceBackendCustomMetrics]]], jsii.get(self, "customMetricsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e500bbc3bbb861cca45fe1d2c899d6b659e32cf42f577fbbc9906756eb18f8a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "balancingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacityScaler")
    def capacity_scaler(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "capacityScaler"))

    @capacity_scaler.setter
    def capacity_scaler(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9b15898ea02857144bba2101c6cf8424fa9a6b06e92c8e33cdeb1c21df9f1ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityScaler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbdf14163bf15227bed8d3a287ff6d0ebad8f3b56bbc987dc8936910f03004a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__356f1c06306b3b0e72ac3b00a4bf9e195bab9f8c9adf46c55c59e2c408f7f302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failover", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb817b5f899ab00fc085a04229b510b7725dda0bdd7ccf99554a25346aa4c50a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConnections")
    def max_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnections"))

    @max_connections.setter
    def max_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5e880db719f7758dd97ae75b9f11e62b368ea91165c429ac2a66e9766eade1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsPerEndpoint")
    def max_connections_per_endpoint(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionsPerEndpoint"))

    @max_connections_per_endpoint.setter
    def max_connections_per_endpoint(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5590596f24602ec0f459ce85a1e674563336573ebd3ad4c4d7c496f1e7d93d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionsPerEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConnectionsPerInstance")
    def max_connections_per_instance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionsPerInstance"))

    @max_connections_per_instance.setter
    def max_connections_per_instance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7a98a74dd102bfc173678cff8473b9ed57de54141e2446488e61ffbdd98298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionsPerInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRate")
    def max_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRate"))

    @max_rate.setter
    def max_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9caa2aee99e9ccd5d0e14d437bc570087206c9dc240392a23f02978917c0bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRatePerEndpoint")
    def max_rate_per_endpoint(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRatePerEndpoint"))

    @max_rate_per_endpoint.setter
    def max_rate_per_endpoint(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d2bf64589f55d182149e66f228a3c2fb527656d1644b8df4013fa02ad4c9bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRatePerEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRatePerInstance")
    def max_rate_per_instance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRatePerInstance"))

    @max_rate_per_instance.setter
    def max_rate_per_instance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf0d747f033db0b1f1be871e7383d114ae1edabfa84ae0f195d4ef04a789fc24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRatePerInstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUtilization")
    def max_utilization(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUtilization"))

    @max_utilization.setter
    def max_utilization(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3174f5c4fe5f7edf9a50e38789ba5b00700fcc4b7000f11540b8b77875d31e01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUtilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceBackend]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceBackend]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceBackend]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce8a1426035a988f574e8c5b459f65b49e20b11aa45ea89b8ecdcaf66fa0034b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceCdnPolicy",
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
class ComputeRegionBackendServiceCdnPolicy:
    def __init__(
        self,
        *,
        cache_key_policy: typing.Optional[typing.Union["ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cache_mode: typing.Optional[builtins.str] = None,
        client_ttl: typing.Optional[jsii.Number] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        max_ttl: typing.Optional[jsii.Number] = None,
        negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        serve_while_stale: typing.Optional[jsii.Number] = None,
        signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cache_key_policy: cache_key_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#cache_key_policy ComputeRegionBackendService#cache_key_policy}
        :param cache_mode: Specifies the cache setting for all responses from this backend. The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#cache_mode ComputeRegionBackendService#cache_mode}
        :param client_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#client_ttl ComputeRegionBackendService#client_ttl}
        :param default_ttl: Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#default_ttl ComputeRegionBackendService#default_ttl}
        :param max_ttl: Specifies the maximum allowed TTL for cached content served by this origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_ttl ComputeRegionBackendService#max_ttl}
        :param negative_caching: Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#negative_caching ComputeRegionBackendService#negative_caching}
        :param negative_caching_policy: negative_caching_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#negative_caching_policy ComputeRegionBackendService#negative_caching_policy}
        :param serve_while_stale: Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#serve_while_stale ComputeRegionBackendService#serve_while_stale}
        :param signed_url_cache_max_age_sec: Maximum number of seconds the response to a signed URL request will be considered fresh, defaults to 1hr (3600s). After this time period, the response will be revalidated before being served. When serving responses to signed URL requests, Cloud CDN will internally behave as though all responses from this backend had a "Cache-Control: public, max-age=[TTL]" header, regardless of any existing Cache-Control header. The actual headers served in responses will not be altered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#signed_url_cache_max_age_sec ComputeRegionBackendService#signed_url_cache_max_age_sec}
        '''
        if isinstance(cache_key_policy, dict):
            cache_key_policy = ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy(**cache_key_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f762ad61dc54ad3d79699c5aed3f9b69e4e6b50d5e56cb4ffdcb354b86c3172)
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
    ) -> typing.Optional["ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy"]:
        '''cache_key_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#cache_key_policy ComputeRegionBackendService#cache_key_policy}
        '''
        result = self._values.get("cache_key_policy")
        return typing.cast(typing.Optional["ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy"], result)

    @builtins.property
    def cache_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the cache setting for all responses from this backend.

        The possible values are: USE_ORIGIN_HEADERS, FORCE_CACHE_ALL and CACHE_ALL_STATIC Possible values: ["USE_ORIGIN_HEADERS", "FORCE_CACHE_ALL", "CACHE_ALL_STATIC"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#cache_mode ComputeRegionBackendService#cache_mode}
        '''
        result = self._values.get("cache_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum allowed TTL for cached content served by this origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#client_ttl ComputeRegionBackendService#client_ttl}
        '''
        result = self._values.get("client_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the default TTL for cached content served by this origin for responses that do not have an existing valid TTL (max-age or s-max-age).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#default_ttl ComputeRegionBackendService#default_ttl}
        '''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_ttl(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum allowed TTL for cached content served by this origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_ttl ComputeRegionBackendService#max_ttl}
        '''
        result = self._values.get("max_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def negative_caching(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Negative caching allows per-status code TTLs to be set, in order to apply fine-grained caching for common errors or redirects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#negative_caching ComputeRegionBackendService#negative_caching}
        '''
        result = self._values.get("negative_caching")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def negative_caching_policy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy"]]]:
        '''negative_caching_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#negative_caching_policy ComputeRegionBackendService#negative_caching_policy}
        '''
        result = self._values.get("negative_caching_policy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy"]]], result)

    @builtins.property
    def serve_while_stale(self) -> typing.Optional[jsii.Number]:
        '''Serve existing content from the cache (if available) when revalidating content with the origin, or when an error is encountered when refreshing the cache.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#serve_while_stale ComputeRegionBackendService#serve_while_stale}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#signed_url_cache_max_age_sec ComputeRegionBackendService#signed_url_cache_max_age_sec}
        '''
        result = self._values.get("signed_url_cache_max_age_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceCdnPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy",
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
class ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy:
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
        :param include_host: If true requests to different hosts will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#include_host ComputeRegionBackendService#include_host}
        :param include_named_cookies: Names of cookies to include in cache keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#include_named_cookies ComputeRegionBackendService#include_named_cookies}
        :param include_protocol: If true, http and https requests will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#include_protocol ComputeRegionBackendService#include_protocol}
        :param include_query_string: If true, include query string parameters in the cache key according to query_string_whitelist and query_string_blacklist. If neither is set, the entire query string will be included. If false, the query string will be excluded from the cache key entirely. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#include_query_string ComputeRegionBackendService#include_query_string}
        :param query_string_blacklist: Names of query string parameters to exclude in cache keys. All other parameters will be included. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#query_string_blacklist ComputeRegionBackendService#query_string_blacklist}
        :param query_string_whitelist: Names of query string parameters to include in cache keys. All other parameters will be excluded. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#query_string_whitelist ComputeRegionBackendService#query_string_whitelist}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__379568ce93934ee39c05535e079cd33a2e12de9b3f2e29276b6a8637f132bedf)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#include_host ComputeRegionBackendService#include_host}
        '''
        result = self._values.get("include_host")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_named_cookies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of cookies to include in cache keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#include_named_cookies ComputeRegionBackendService#include_named_cookies}
        '''
        result = self._values.get("include_named_cookies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_protocol(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, http and https requests will be cached separately.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#include_protocol ComputeRegionBackendService#include_protocol}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#include_query_string ComputeRegionBackendService#include_query_string}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#query_string_blacklist ComputeRegionBackendService#query_string_blacklist}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#query_string_whitelist ComputeRegionBackendService#query_string_whitelist}
        '''
        result = self._values.get("query_string_whitelist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceCdnPolicyCacheKeyPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceCdnPolicyCacheKeyPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__199c372215c35b0865ae27599f11e07814fdf9ec61c6b06c34c3458bc268261e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7aa71c2205f76cc9daee07d33568428a7b868016707f7d68fb3c720cc6231765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeNamedCookies")
    def include_named_cookies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeNamedCookies"))

    @include_named_cookies.setter
    def include_named_cookies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647d5d507b4b2c0685f384e891132dc149015b3867ed296427358ac552ad7ea4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__065faa1b914207b3e2105d5b9ac053e3c6c206d5402b5e154d1a9f334cb27434)
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
            type_hints = typing.get_type_hints(_typecheckingstub__432d5cac0d48501477135da33b0c1480bfb775faa681aac7bc5864969dc717aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeQueryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringBlacklist")
    def query_string_blacklist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringBlacklist"))

    @query_string_blacklist.setter
    def query_string_blacklist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63dc0e3e76553beea908d3dd430b8f00f6c84b3a226cb383c8602357a250133c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringBlacklist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringWhitelist")
    def query_string_whitelist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringWhitelist"))

    @query_string_whitelist.setter
    def query_string_whitelist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de07ebb57db02540135ca77305cf6ea4b2fa8cb06dcab09b4e7d5857ba3d521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringWhitelist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d8275ffbd9c4685f84025e63e43f56ef49d2c0a892cb094d32090271ae5903)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy",
    jsii_struct_bases=[],
    name_mapping={"code": "code"},
)
class ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy:
    def __init__(self, *, code: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param code: The HTTP status code to define a TTL against. Only HTTP status codes 300, 301, 308, 404, 405, 410, 421, 451 and 501 can be specified as values, and you cannot specify a status code more than once. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#code ComputeRegionBackendService#code}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab605d31c904330c0eaff74295beb59394008283eba9048b27c64a7ad8eff93a)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code is not None:
            self._values["code"] = code

    @builtins.property
    def code(self) -> typing.Optional[jsii.Number]:
        '''The HTTP status code to define a TTL against.

        Only HTTP status codes 300, 301, 308, 404, 405, 410, 421, 451 and 501
        can be specified as values, and you cannot specify a status code more than once.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#code ComputeRegionBackendService#code}
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f22ea4a5a32175e50467b7c9884a3bb0ee0837e874757ab185255d32fd511d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae51cc8232aba4e45810dbcb7366a432badac90c16fe950a8884267b06656d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00b710afed83d789074b329b34c3efca94bfe67bc48300c57d7b694acc92488)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e99505de1cdbc633a081027b2938957ed3ab8cb9c81d0975f444fd5d65cfa0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f317bd613505711d880fe6b6b3a07db7e455d0589f2c21c85b8d3189b7703abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c8ce4267a145c0945f579aef11116d86bae77795092937c475709b93572898f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f044a9b2b9291f7bf321a3ceb7f065717aaadab5a80ff64b968a62db155d0239)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCode")
    def reset_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCode", []))

    @builtins.property
    @jsii.member(jsii_name="codeInput")
    def code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "codeInput"))

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @code.setter
    def code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f120e1419fd3a83795d7034b40bf7092c0432ffcaabef0d5dcde262757bc0dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762e126574a8f2a98fe6f6b8ab38ea3112bf683014ffb108c0c2706eb9ae32a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionBackendServiceCdnPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceCdnPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1afcc3fcf86329631cc19ce6537e0b1b9730cdee91cf19e622991e3886d18a3f)
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
        :param include_host: If true requests to different hosts will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#include_host ComputeRegionBackendService#include_host}
        :param include_named_cookies: Names of cookies to include in cache keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#include_named_cookies ComputeRegionBackendService#include_named_cookies}
        :param include_protocol: If true, http and https requests will be cached separately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#include_protocol ComputeRegionBackendService#include_protocol}
        :param include_query_string: If true, include query string parameters in the cache key according to query_string_whitelist and query_string_blacklist. If neither is set, the entire query string will be included. If false, the query string will be excluded from the cache key entirely. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#include_query_string ComputeRegionBackendService#include_query_string}
        :param query_string_blacklist: Names of query string parameters to exclude in cache keys. All other parameters will be included. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#query_string_blacklist ComputeRegionBackendService#query_string_blacklist}
        :param query_string_whitelist: Names of query string parameters to include in cache keys. All other parameters will be excluded. Either specify query_string_whitelist or query_string_blacklist, not both. '&' and '=' will be percent encoded and not treated as delimiters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#query_string_whitelist ComputeRegionBackendService#query_string_whitelist}
        '''
        value = ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fafe9e418813c27bb86b466da4afe5cf9926e19d5abac5eaddca8df7f6a3b95)
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
    ) -> ComputeRegionBackendServiceCdnPolicyCacheKeyPolicyOutputReference:
        return typing.cast(ComputeRegionBackendServiceCdnPolicyCacheKeyPolicyOutputReference, jsii.get(self, "cacheKeyPolicy"))

    @builtins.property
    @jsii.member(jsii_name="negativeCachingPolicy")
    def negative_caching_policy(
        self,
    ) -> ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyList:
        return typing.cast(ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyList, jsii.get(self, "negativeCachingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="cacheKeyPolicyInput")
    def cache_key_policy_input(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy], jsii.get(self, "cacheKeyPolicyInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]], jsii.get(self, "negativeCachingPolicyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0ea9599261f5800799bf190ce789cbb1bd8b50f25ce1c95441e7e6e72a78de93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTtl")
    def client_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientTtl"))

    @client_ttl.setter
    def client_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f741e54aa48e0ba4d404b2c7a0a5800c2d17feb3493760085e9b8afca785b64c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091e61f296ec1f9e760ed81656614ce61bec3da6415a857c08fb51882995e0ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTtl")
    def max_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxTtl"))

    @max_ttl.setter
    def max_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a9d12a8353403405940014d2fe4f33866be6cae9285093a77a5366d565d15fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d841e23d6d935d9ad3a75aaa84820fb2fe7ddd846840311bdecd266180a80000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negativeCaching", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serveWhileStale")
    def serve_while_stale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "serveWhileStale"))

    @serve_while_stale.setter
    def serve_while_stale(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89df93bccd2c6efb1d0c9d89a266e435387de7707231f7a2a68d8da30f06a37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serveWhileStale", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signedUrlCacheMaxAgeSec")
    def signed_url_cache_max_age_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "signedUrlCacheMaxAgeSec"))

    @signed_url_cache_max_age_sec.setter
    def signed_url_cache_max_age_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908d3e436e2044802a3d1eec93b50b82c90ad0cec10dd19d6e12eaafdb49cc1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signedUrlCacheMaxAgeSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRegionBackendServiceCdnPolicy]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceCdnPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceCdnPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ffb386b50fdf9e0c7b64ea26c0a5022760515a83b4fa6b585c9b68c6f3dd1dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceCircuitBreakers",
    jsii_struct_bases=[],
    name_mapping={
        "max_connections": "maxConnections",
        "max_pending_requests": "maxPendingRequests",
        "max_requests": "maxRequests",
        "max_requests_per_connection": "maxRequestsPerConnection",
        "max_retries": "maxRetries",
    },
)
class ComputeRegionBackendServiceCircuitBreakers:
    def __init__(
        self,
        *,
        max_connections: typing.Optional[jsii.Number] = None,
        max_pending_requests: typing.Optional[jsii.Number] = None,
        max_requests: typing.Optional[jsii.Number] = None,
        max_requests_per_connection: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_connections: The maximum number of connections to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_connections ComputeRegionBackendService#max_connections}
        :param max_pending_requests: The maximum number of pending requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_pending_requests ComputeRegionBackendService#max_pending_requests}
        :param max_requests: The maximum number of parallel requests to the backend cluster. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_requests ComputeRegionBackendService#max_requests}
        :param max_requests_per_connection: Maximum requests for a single backend connection. This parameter is respected by both the HTTP/1.1 and HTTP/2 implementations. If not specified, there is no limit. Setting this parameter to 1 will effectively disable keep alive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_requests_per_connection ComputeRegionBackendService#max_requests_per_connection}
        :param max_retries: The maximum number of parallel retries to the backend cluster. Defaults to 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_retries ComputeRegionBackendService#max_retries}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__266a5682df9681a59744226a311495815409a6484e6aa17c82ee4d35af09af83)
            check_type(argname="argument max_connections", value=max_connections, expected_type=type_hints["max_connections"])
            check_type(argname="argument max_pending_requests", value=max_pending_requests, expected_type=type_hints["max_pending_requests"])
            check_type(argname="argument max_requests", value=max_requests, expected_type=type_hints["max_requests"])
            check_type(argname="argument max_requests_per_connection", value=max_requests_per_connection, expected_type=type_hints["max_requests_per_connection"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
    def max_connections(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of connections to the backend cluster. Defaults to 1024.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_connections ComputeRegionBackendService#max_connections}
        '''
        result = self._values.get("max_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_pending_requests(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of pending requests to the backend cluster. Defaults to 1024.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_pending_requests ComputeRegionBackendService#max_pending_requests}
        '''
        result = self._values.get("max_pending_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_requests(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of parallel requests to the backend cluster. Defaults to 1024.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_requests ComputeRegionBackendService#max_requests}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_requests_per_connection ComputeRegionBackendService#max_requests_per_connection}
        '''
        result = self._values.get("max_requests_per_connection")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of parallel retries to the backend cluster. Defaults to 3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_retries ComputeRegionBackendService#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceCircuitBreakers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceCircuitBreakersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceCircuitBreakersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__893780769ac8d37355e438525acbd4aed3a005fc80fd17d25190253cfe09411d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__f82019ede3e01a5eeb54fe45d89e3c9d001ded87341ba441c5c02598bd71aaa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPendingRequests")
    def max_pending_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPendingRequests"))

    @max_pending_requests.setter
    def max_pending_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecc6ff032c620d59d5bdba15c2bc5ce9d343ce3d4c0fa9a9fc64b058b8e40a67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPendingRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRequests")
    def max_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRequests"))

    @max_requests.setter
    def max_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c91658cb74df1dc152ca198e9700175b8784a3cef2f99491c1d0cef297a334b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRequestsPerConnection")
    def max_requests_per_connection(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRequestsPerConnection"))

    @max_requests_per_connection.setter
    def max_requests_per_connection(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600c89c29a6a6fd707558664e49aecee221b8ae2860bff5f0819d34f324f36e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRequestsPerConnection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a28d216d508cd81aa3bb776b09b29429a1e999d3438f84f5504cb93a0a89b45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceCircuitBreakers]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceCircuitBreakers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceCircuitBreakers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a0ed6399f9ad92500995d35e4410b7fa0c21fcd0bd76414bf350ccedb8ae9b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceConfig",
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
        "consistent_hash": "consistentHash",
        "custom_metrics": "customMetrics",
        "description": "description",
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
        "session_affinity": "sessionAffinity",
        "strong_session_affinity_cookie": "strongSessionAffinityCookie",
        "timeouts": "timeouts",
        "timeout_sec": "timeoutSec",
    },
)
class ComputeRegionBackendServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cdn_policy: typing.Optional[typing.Union[ComputeRegionBackendServiceCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        circuit_breakers: typing.Optional[typing.Union[ComputeRegionBackendServiceCircuitBreakers, typing.Dict[builtins.str, typing.Any]]] = None,
        connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
        consistent_hash: typing.Optional[typing.Union["ComputeRegionBackendServiceConsistentHash", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionBackendServiceCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failover_policy: typing.Optional[typing.Union["ComputeRegionBackendServiceFailoverPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        iap: typing.Optional[typing.Union["ComputeRegionBackendServiceIap", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address_selection_policy: typing.Optional[builtins.str] = None,
        load_balancing_scheme: typing.Optional[builtins.str] = None,
        locality_lb_policy: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["ComputeRegionBackendServiceLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[builtins.str] = None,
        outlier_detection: typing.Optional[typing.Union["ComputeRegionBackendServiceOutlierDetection", typing.Dict[builtins.str, typing.Any]]] = None,
        port_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[builtins.str] = None,
        strong_session_affinity_cookie: typing.Optional[typing.Union["ComputeRegionBackendServiceStrongSessionAffinityCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionBackendServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#name ComputeRegionBackendService#name}
        :param affinity_cookie_ttl_sec: Lifetime of cookies in seconds if session_affinity is GENERATED_COOKIE. If set to 0, the cookie is non-persistent and lasts only until the end of the browser session (or equivalent). The maximum allowed value for TTL is one day. When the load balancing scheme is INTERNAL, this field is not used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#affinity_cookie_ttl_sec ComputeRegionBackendService#affinity_cookie_ttl_sec}
        :param backend: backend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#backend ComputeRegionBackendService#backend}
        :param cdn_policy: cdn_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#cdn_policy ComputeRegionBackendService#cdn_policy}
        :param circuit_breakers: circuit_breakers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#circuit_breakers ComputeRegionBackendService#circuit_breakers}
        :param connection_draining_timeout_sec: Time for which instance will be drained (not accept new connections, but still work to finish started). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#connection_draining_timeout_sec ComputeRegionBackendService#connection_draining_timeout_sec}
        :param consistent_hash: consistent_hash block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#consistent_hash ComputeRegionBackendService#consistent_hash}
        :param custom_metrics: custom_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#custom_metrics ComputeRegionBackendService#custom_metrics}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#description ComputeRegionBackendService#description}
        :param enable_cdn: If true, enable Cloud CDN for this RegionBackendService. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enable_cdn ComputeRegionBackendService#enable_cdn}
        :param failover_policy: failover_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#failover_policy ComputeRegionBackendService#failover_policy}
        :param health_checks: The set of URLs to HealthCheck resources for health checking this RegionBackendService. Currently at most one health check can be specified. A health check must be specified unless the backend service uses an internet or serverless NEG as a backend. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#health_checks ComputeRegionBackendService#health_checks}
        :param iap: iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#iap ComputeRegionBackendService#iap}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#id ComputeRegionBackendService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address_selection_policy: Specifies preference of traffic to the backend (from the proxy and from the client for proxyless gRPC). Possible values: ["IPV4_ONLY", "PREFER_IPV6", "IPV6_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#ip_address_selection_policy ComputeRegionBackendService#ip_address_selection_policy}
        :param load_balancing_scheme: Indicates what kind of load balancing this regional backend service will be used for. A backend service created for one type of load balancing cannot be used with the other(s). For more information, refer to `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_. Default value: "INTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL", "INTERNAL_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#load_balancing_scheme ComputeRegionBackendService#load_balancing_scheme}
        :param locality_lb_policy: The load balancing algorithm used within the scope of the locality. The possible values are:. - 'ROUND_ROBIN': This is a simple policy in which each healthy backend is selected in round robin order. - 'LEAST_REQUEST': An O(1) algorithm which selects two random healthy hosts and picks the host which has fewer active requests. - 'RING_HASH': The ring/modulo hash load balancer implements consistent hashing to backends. The algorithm has the property that the addition/removal of a host from a set of N hosts only affects 1/N of the requests. - 'RANDOM': The load balancer selects a random healthy host. - 'ORIGINAL_DESTINATION': Backend host is selected based on the client connection metadata, i.e., connections are opened to the same address as the destination address of the incoming connection before the connection was redirected to the load balancer. - 'MAGLEV': used as a drop in replacement for the ring hash load balancer. Maglev is not as stable as ring hash but has faster table lookup build times and host selection times. For more information about Maglev, refer to https://ai.google/research/pubs/pub44824 - 'WEIGHTED_MAGLEV': Per-instance weighted Load Balancing via health check reported weights. Only applicable to loadBalancingScheme EXTERNAL. If set, the Backend Service must configure a non legacy HTTP-based Health Check, and health check replies are expected to contain non-standard HTTP response header field X-Load-Balancing-Endpoint-Weight to specify the per-instance weights. If set, Load Balancing is weight based on the per-instance weights reported in the last processed health check replies, as long as every instance either reported a valid weight or had UNAVAILABLE_WEIGHT. Otherwise, Load Balancing remains equal-weight. - 'WEIGHTED_ROUND_ROBIN': Per-endpoint weighted round-robin Load Balancing using weights computed from Backend reported Custom Metrics. If set, the Backend Service responses are expected to contain non-standard HTTP response header field X-Endpoint-Load-Metrics. The reported metrics to use for computing the weights are specified via the backends[].customMetrics fields. locality_lb_policy is applicable to either: - A regional backend service with the service_protocol set to HTTP, HTTPS, HTTP2 or H2C, and loadBalancingScheme set to INTERNAL_MANAGED. - A global backend service with the load_balancing_scheme set to INTERNAL_SELF_MANAGED. - A regional backend service with loadBalancingScheme set to EXTERNAL (External Network Load Balancing). Only MAGLEV and WEIGHTED_MAGLEV values are possible for External Network Load Balancing. The default is MAGLEV. If session_affinity is not NONE, and locality_lb_policy is not set to MAGLEV, WEIGHTED_MAGLEV, or RING_HASH, session affinity settings will not take effect. Only ROUND_ROBIN and RING_HASH are supported when the backend service is referenced by a URL map that is bound to target gRPC proxy that has validate_for_proxyless field set to true. Possible values: ["ROUND_ROBIN", "LEAST_REQUEST", "RING_HASH", "RANDOM", "ORIGINAL_DESTINATION", "MAGLEV", "WEIGHTED_MAGLEV", "WEIGHTED_ROUND_ROBIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#locality_lb_policy ComputeRegionBackendService#locality_lb_policy}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#log_config ComputeRegionBackendService#log_config}
        :param network: The URL of the network to which this backend service belongs. This field can only be specified when the load balancing scheme is set to INTERNAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#network ComputeRegionBackendService#network}
        :param outlier_detection: outlier_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#outlier_detection ComputeRegionBackendService#outlier_detection}
        :param port_name: A named port on a backend instance group representing the port for communication to the backend VMs in that group. Required when the loadBalancingScheme is EXTERNAL, EXTERNAL_MANAGED, INTERNAL_MANAGED, or INTERNAL_SELF_MANAGED and the backends are instance groups. The named port must be defined on each backend instance group. This parameter has no meaning if the backends are NEGs. API sets a default of "http" if not given. Must be omitted when the loadBalancingScheme is INTERNAL (Internal TCP/UDP Load Balancing). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#port_name ComputeRegionBackendService#port_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#project ComputeRegionBackendService#project}.
        :param protocol: The protocol this BackendService uses to communicate with backends. The default is HTTP. Possible values are HTTP, HTTPS, HTTP2, H2C, TCP, SSL, UDP or GRPC. Refer to the documentation for the load balancers or for Traffic Director for more information. Possible values: ["HTTP", "HTTPS", "HTTP2", "TCP", "SSL", "UDP", "GRPC", "UNSPECIFIED", "H2C"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#protocol ComputeRegionBackendService#protocol}
        :param region: The Region in which the created backend service should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#region ComputeRegionBackendService#region}
        :param session_affinity: Type of session affinity to use. The default is NONE. Session affinity is not applicable if the protocol is UDP. Possible values: ["NONE", "CLIENT_IP", "CLIENT_IP_PORT_PROTO", "CLIENT_IP_PROTO", "GENERATED_COOKIE", "HEADER_FIELD", "HTTP_COOKIE", "CLIENT_IP_NO_DESTINATION", "STRONG_COOKIE_AFFINITY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#session_affinity ComputeRegionBackendService#session_affinity}
        :param strong_session_affinity_cookie: strong_session_affinity_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#strong_session_affinity_cookie ComputeRegionBackendService#strong_session_affinity_cookie}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#timeouts ComputeRegionBackendService#timeouts}
        :param timeout_sec: The backend service timeout has a different meaning depending on the type of load balancer. For more information see, `Backend service settings <https://cloud.google.com/compute/docs/reference/rest/v1/backendServices>`_. The default is 30 seconds. The full range of timeout values allowed goes from 1 through 2,147,483,647 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#timeout_sec ComputeRegionBackendService#timeout_sec}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cdn_policy, dict):
            cdn_policy = ComputeRegionBackendServiceCdnPolicy(**cdn_policy)
        if isinstance(circuit_breakers, dict):
            circuit_breakers = ComputeRegionBackendServiceCircuitBreakers(**circuit_breakers)
        if isinstance(consistent_hash, dict):
            consistent_hash = ComputeRegionBackendServiceConsistentHash(**consistent_hash)
        if isinstance(failover_policy, dict):
            failover_policy = ComputeRegionBackendServiceFailoverPolicy(**failover_policy)
        if isinstance(iap, dict):
            iap = ComputeRegionBackendServiceIap(**iap)
        if isinstance(log_config, dict):
            log_config = ComputeRegionBackendServiceLogConfig(**log_config)
        if isinstance(outlier_detection, dict):
            outlier_detection = ComputeRegionBackendServiceOutlierDetection(**outlier_detection)
        if isinstance(strong_session_affinity_cookie, dict):
            strong_session_affinity_cookie = ComputeRegionBackendServiceStrongSessionAffinityCookie(**strong_session_affinity_cookie)
        if isinstance(timeouts, dict):
            timeouts = ComputeRegionBackendServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__942d906da0191287bd3769b8797469069205f1e711375baabdb5fd74249f6e12)
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
            check_type(argname="argument consistent_hash", value=consistent_hash, expected_type=type_hints["consistent_hash"])
            check_type(argname="argument custom_metrics", value=custom_metrics, expected_type=type_hints["custom_metrics"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
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
            check_type(argname="argument session_affinity", value=session_affinity, expected_type=type_hints["session_affinity"])
            check_type(argname="argument strong_session_affinity_cookie", value=strong_session_affinity_cookie, expected_type=type_hints["strong_session_affinity_cookie"])
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
        if consistent_hash is not None:
            self._values["consistent_hash"] = consistent_hash
        if custom_metrics is not None:
            self._values["custom_metrics"] = custom_metrics
        if description is not None:
            self._values["description"] = description
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
        if session_affinity is not None:
            self._values["session_affinity"] = session_affinity
        if strong_session_affinity_cookie is not None:
            self._values["strong_session_affinity_cookie"] = strong_session_affinity_cookie
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#name ComputeRegionBackendService#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#affinity_cookie_ttl_sec ComputeRegionBackendService#affinity_cookie_ttl_sec}
        '''
        result = self._values.get("affinity_cookie_ttl_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def backend(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceBackend]]]:
        '''backend block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#backend ComputeRegionBackendService#backend}
        '''
        result = self._values.get("backend")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceBackend]]], result)

    @builtins.property
    def cdn_policy(self) -> typing.Optional[ComputeRegionBackendServiceCdnPolicy]:
        '''cdn_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#cdn_policy ComputeRegionBackendService#cdn_policy}
        '''
        result = self._values.get("cdn_policy")
        return typing.cast(typing.Optional[ComputeRegionBackendServiceCdnPolicy], result)

    @builtins.property
    def circuit_breakers(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceCircuitBreakers]:
        '''circuit_breakers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#circuit_breakers ComputeRegionBackendService#circuit_breakers}
        '''
        result = self._values.get("circuit_breakers")
        return typing.cast(typing.Optional[ComputeRegionBackendServiceCircuitBreakers], result)

    @builtins.property
    def connection_draining_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Time for which instance will be drained (not accept new connections, but still work to finish started).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#connection_draining_timeout_sec ComputeRegionBackendService#connection_draining_timeout_sec}
        '''
        result = self._values.get("connection_draining_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def consistent_hash(
        self,
    ) -> typing.Optional["ComputeRegionBackendServiceConsistentHash"]:
        '''consistent_hash block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#consistent_hash ComputeRegionBackendService#consistent_hash}
        '''
        result = self._values.get("consistent_hash")
        return typing.cast(typing.Optional["ComputeRegionBackendServiceConsistentHash"], result)

    @builtins.property
    def custom_metrics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionBackendServiceCustomMetrics"]]]:
        '''custom_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#custom_metrics ComputeRegionBackendService#custom_metrics}
        '''
        result = self._values.get("custom_metrics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionBackendServiceCustomMetrics"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#description ComputeRegionBackendService#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_cdn(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, enable Cloud CDN for this RegionBackendService.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enable_cdn ComputeRegionBackendService#enable_cdn}
        '''
        result = self._values.get("enable_cdn")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def failover_policy(
        self,
    ) -> typing.Optional["ComputeRegionBackendServiceFailoverPolicy"]:
        '''failover_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#failover_policy ComputeRegionBackendService#failover_policy}
        '''
        result = self._values.get("failover_policy")
        return typing.cast(typing.Optional["ComputeRegionBackendServiceFailoverPolicy"], result)

    @builtins.property
    def health_checks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of URLs to HealthCheck resources for health checking this RegionBackendService. Currently at most one health check can be specified.

        A health check must be specified unless the backend service uses an internet
        or serverless NEG as a backend.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#health_checks ComputeRegionBackendService#health_checks}
        '''
        result = self._values.get("health_checks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def iap(self) -> typing.Optional["ComputeRegionBackendServiceIap"]:
        '''iap block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#iap ComputeRegionBackendService#iap}
        '''
        result = self._values.get("iap")
        return typing.cast(typing.Optional["ComputeRegionBackendServiceIap"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#id ComputeRegionBackendService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address_selection_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies preference of traffic to the backend (from the proxy and from the client for proxyless gRPC).

        Possible values: ["IPV4_ONLY", "PREFER_IPV6", "IPV6_ONLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#ip_address_selection_policy ComputeRegionBackendService#ip_address_selection_policy}
        '''
        result = self._values.get("ip_address_selection_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancing_scheme(self) -> typing.Optional[builtins.str]:
        '''Indicates what kind of load balancing this regional backend service will be used for.

        A backend service created for one type of load
        balancing cannot be used with the other(s). For more information, refer to
        `Choosing a load balancer <https://cloud.google.com/load-balancing/docs/backend-service>`_. Default value: "INTERNAL" Possible values: ["EXTERNAL", "EXTERNAL_MANAGED", "INTERNAL", "INTERNAL_MANAGED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#load_balancing_scheme ComputeRegionBackendService#load_balancing_scheme}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#locality_lb_policy ComputeRegionBackendService#locality_lb_policy}
        '''
        result = self._values.get("locality_lb_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_config(self) -> typing.Optional["ComputeRegionBackendServiceLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#log_config ComputeRegionBackendService#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["ComputeRegionBackendServiceLogConfig"], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The URL of the network to which this backend service belongs.

        This field can only be specified when the load balancing scheme is set to INTERNAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#network ComputeRegionBackendService#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outlier_detection(
        self,
    ) -> typing.Optional["ComputeRegionBackendServiceOutlierDetection"]:
        '''outlier_detection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#outlier_detection ComputeRegionBackendService#outlier_detection}
        '''
        result = self._values.get("outlier_detection")
        return typing.cast(typing.Optional["ComputeRegionBackendServiceOutlierDetection"], result)

    @builtins.property
    def port_name(self) -> typing.Optional[builtins.str]:
        '''A named port on a backend instance group representing the port for communication to the backend VMs in that group.

        Required when the
        loadBalancingScheme is EXTERNAL, EXTERNAL_MANAGED, INTERNAL_MANAGED, or INTERNAL_SELF_MANAGED
        and the backends are instance groups. The named port must be defined on each
        backend instance group. This parameter has no meaning if the backends are NEGs. API sets a
        default of "http" if not given.
        Must be omitted when the loadBalancingScheme is INTERNAL (Internal TCP/UDP Load Balancing).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#port_name ComputeRegionBackendService#port_name}
        '''
        result = self._values.get("port_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#project ComputeRegionBackendService#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol this BackendService uses to communicate with backends.

        The default is HTTP. Possible values are HTTP, HTTPS, HTTP2, H2C, TCP, SSL, UDP
        or GRPC. Refer to the documentation for the load balancers or for Traffic Director
        for more information. Possible values: ["HTTP", "HTTPS", "HTTP2", "TCP", "SSL", "UDP", "GRPC", "UNSPECIFIED", "H2C"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#protocol ComputeRegionBackendService#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The Region in which the created backend service should reside. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#region ComputeRegionBackendService#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_affinity(self) -> typing.Optional[builtins.str]:
        '''Type of session affinity to use.

        The default is NONE. Session affinity is
        not applicable if the protocol is UDP. Possible values: ["NONE", "CLIENT_IP", "CLIENT_IP_PORT_PROTO", "CLIENT_IP_PROTO", "GENERATED_COOKIE", "HEADER_FIELD", "HTTP_COOKIE", "CLIENT_IP_NO_DESTINATION", "STRONG_COOKIE_AFFINITY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#session_affinity ComputeRegionBackendService#session_affinity}
        '''
        result = self._values.get("session_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strong_session_affinity_cookie(
        self,
    ) -> typing.Optional["ComputeRegionBackendServiceStrongSessionAffinityCookie"]:
        '''strong_session_affinity_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#strong_session_affinity_cookie ComputeRegionBackendService#strong_session_affinity_cookie}
        '''
        result = self._values.get("strong_session_affinity_cookie")
        return typing.cast(typing.Optional["ComputeRegionBackendServiceStrongSessionAffinityCookie"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRegionBackendServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#timeouts ComputeRegionBackendService#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRegionBackendServiceTimeouts"], result)

    @builtins.property
    def timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''The backend service timeout has a different meaning depending on the type of load balancer.

        For more information see, `Backend service settings <https://cloud.google.com/compute/docs/reference/rest/v1/backendServices>`_.
        The default is 30 seconds.
        The full range of timeout values allowed goes from 1 through 2,147,483,647 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#timeout_sec ComputeRegionBackendService#timeout_sec}
        '''
        result = self._values.get("timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceConsistentHash",
    jsii_struct_bases=[],
    name_mapping={
        "http_cookie": "httpCookie",
        "http_header_name": "httpHeaderName",
        "minimum_ring_size": "minimumRingSize",
    },
)
class ComputeRegionBackendServiceConsistentHash:
    def __init__(
        self,
        *,
        http_cookie: typing.Optional[typing.Union["ComputeRegionBackendServiceConsistentHashHttpCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        http_header_name: typing.Optional[builtins.str] = None,
        minimum_ring_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_cookie: http_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#http_cookie ComputeRegionBackendService#http_cookie}
        :param http_header_name: The hash based on the value of the specified header field. This field is applicable if the sessionAffinity is set to HEADER_FIELD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#http_header_name ComputeRegionBackendService#http_header_name}
        :param minimum_ring_size: The minimum number of virtual nodes to use for the hash ring. Larger ring sizes result in more granular load distributions. If the number of hosts in the load balancing pool is larger than the ring size, each host will be assigned a single virtual node. Defaults to 1024. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#minimum_ring_size ComputeRegionBackendService#minimum_ring_size}
        '''
        if isinstance(http_cookie, dict):
            http_cookie = ComputeRegionBackendServiceConsistentHashHttpCookie(**http_cookie)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186f5d67feab665bb2d4876bd04486790631383e709402ca1ff6c65f62dc27f9)
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
    ) -> typing.Optional["ComputeRegionBackendServiceConsistentHashHttpCookie"]:
        '''http_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#http_cookie ComputeRegionBackendService#http_cookie}
        '''
        result = self._values.get("http_cookie")
        return typing.cast(typing.Optional["ComputeRegionBackendServiceConsistentHashHttpCookie"], result)

    @builtins.property
    def http_header_name(self) -> typing.Optional[builtins.str]:
        '''The hash based on the value of the specified header field.

        This field is applicable if the sessionAffinity is set to HEADER_FIELD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#http_header_name ComputeRegionBackendService#http_header_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#minimum_ring_size ComputeRegionBackendService#minimum_ring_size}
        '''
        result = self._values.get("minimum_ring_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceConsistentHash(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceConsistentHashHttpCookie",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "ttl": "ttl"},
)
class ComputeRegionBackendServiceConsistentHashHttpCookie:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union["ComputeRegionBackendServiceConsistentHashHttpCookieTtl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#name ComputeRegionBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#path ComputeRegionBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#ttl ComputeRegionBackendService#ttl}
        '''
        if isinstance(ttl, dict):
            ttl = ComputeRegionBackendServiceConsistentHashHttpCookieTtl(**ttl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a117844a8b60b6aea7c8b6199be86460b3f62731975b7223126cba9fba95cc5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#name ComputeRegionBackendService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to set for the cookie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#path ComputeRegionBackendService#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(
        self,
    ) -> typing.Optional["ComputeRegionBackendServiceConsistentHashHttpCookieTtl"]:
        '''ttl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#ttl ComputeRegionBackendService#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional["ComputeRegionBackendServiceConsistentHashHttpCookieTtl"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceConsistentHashHttpCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceConsistentHashHttpCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceConsistentHashHttpCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__073af85ae8f145e89c0d5a6c02390e588b2b6158f11b6834ad5e3eedf8f6eafb)
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#seconds ComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#nanos ComputeRegionBackendService#nanos}
        '''
        value = ComputeRegionBackendServiceConsistentHashHttpCookieTtl(
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
    ) -> "ComputeRegionBackendServiceConsistentHashHttpCookieTtlOutputReference":
        return typing.cast("ComputeRegionBackendServiceConsistentHashHttpCookieTtlOutputReference", jsii.get(self, "ttl"))

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
    ) -> typing.Optional["ComputeRegionBackendServiceConsistentHashHttpCookieTtl"]:
        return typing.cast(typing.Optional["ComputeRegionBackendServiceConsistentHashHttpCookieTtl"], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b81d61906c2938b5058b5b3d96276cd846669df06a2d7be3ff48e0580b42b86e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3495691e0fed2f3a351c6eb3e1c93e43d07afaa46d80c5875ccb512e64235d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceConsistentHashHttpCookie]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceConsistentHashHttpCookie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceConsistentHashHttpCookie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9a667f311f1b74f716e42760ebf889e3384726f1561a58a4f19ec74276d95df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceConsistentHashHttpCookieTtl",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeRegionBackendServiceConsistentHashHttpCookieTtl:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#seconds ComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#nanos ComputeRegionBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b9966f17083683869b8e88c1cd71c1a24155c4b3a05ef6336b2b68d9e8c4c3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#seconds ComputeRegionBackendService#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#nanos ComputeRegionBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceConsistentHashHttpCookieTtl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceConsistentHashHttpCookieTtlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceConsistentHashHttpCookieTtlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5360707d67fb0c194038bc663fda444dd849b87b5ade6f5bc97540aba8b40692)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc497e516adef4ade1a0ff25b07115fee1c668e30888d712360d2b8e311d1b14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca4459ee7821e229e9ab5c67900a99758d62700ffb4ce37d823db6e56d7098f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceConsistentHashHttpCookieTtl]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceConsistentHashHttpCookieTtl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceConsistentHashHttpCookieTtl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a44d4a364777f5e9c836721c84e417a1767afb63f2f4cbb4419ebc476a261eb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionBackendServiceConsistentHashOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceConsistentHashOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af2fa8ba75b1ca993fdb1e4a1b65887c59accc42b8dd809ae58e1694dda3dbf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpCookie")
    def put_http_cookie(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union[ComputeRegionBackendServiceConsistentHashHttpCookieTtl, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#name ComputeRegionBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#path ComputeRegionBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#ttl ComputeRegionBackendService#ttl}
        '''
        value = ComputeRegionBackendServiceConsistentHashHttpCookie(
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
    ) -> ComputeRegionBackendServiceConsistentHashHttpCookieOutputReference:
        return typing.cast(ComputeRegionBackendServiceConsistentHashHttpCookieOutputReference, jsii.get(self, "httpCookie"))

    @builtins.property
    @jsii.member(jsii_name="httpCookieInput")
    def http_cookie_input(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceConsistentHashHttpCookie]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceConsistentHashHttpCookie], jsii.get(self, "httpCookieInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__098d8871222d597232b4ff357617d254894e28ca18b5eae2e590eeee7fefc59a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumRingSize")
    def minimum_ring_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumRingSize"))

    @minimum_ring_size.setter
    def minimum_ring_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93de2d2732df7a7bc8a92b1f6fcc21733a3fb155471dc957412fd690d82568a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumRingSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceConsistentHash]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceConsistentHash], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceConsistentHash],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557cf970794dc4fd129c66c4f38e0caf6700d46d8f42557a6318623f6d4c7e53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceCustomMetrics",
    jsii_struct_bases=[],
    name_mapping={"dry_run": "dryRun", "name": "name"},
)
class ComputeRegionBackendServiceCustomMetrics:
    def __init__(
        self,
        *,
        dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
    ) -> None:
        '''
        :param dry_run: If true, the metric data is not used for load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#dry_run ComputeRegionBackendService#dry_run}
        :param name: Name of a custom utilization signal. The name must be 1-64 characters long and match the regular expression `a-z <%5B-_.a-z0-9%5D*%5Ba-z0-9%5D>`_? which means the first character must be a lowercase letter, and all following characters must be a dash, period, underscore, lowercase letter, or digit, except the last character, which cannot be a dash, period, or underscore. For usage guidelines, see Custom Metrics balancing mode. This field can only be used for a global or regional backend service with the loadBalancingScheme set to EXTERNAL_MANAGED, INTERNAL_MANAGED INTERNAL_SELF_MANAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#name ComputeRegionBackendService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4885d6085a557703688baaccad3119738a381a9b10ad7258044a50521c9e825)
            check_type(argname="argument dry_run", value=dry_run, expected_type=type_hints["dry_run"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dry_run": dry_run,
            "name": name,
        }

    @builtins.property
    def dry_run(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, the metric data is not used for load balancing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#dry_run ComputeRegionBackendService#dry_run}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#name ComputeRegionBackendService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceCustomMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceCustomMetricsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceCustomMetricsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e237b5b5ee456158ce434f0b85a61980442a3d683542f8107802f077e1b883f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionBackendServiceCustomMetricsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1060662a7b4193f0253b02a7e8e8c922ed6061045e66054459215f4b4ab46e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionBackendServiceCustomMetricsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dad9033b6fb4a5c78fdf2f658e68d5c01b3b5546de1204d114e874a98ace06a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ec940866bab432036dc39a9ed084275aaa067a7b9c001189931835eed0a7fd7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7441d9426509298ab31a27a517475b14327535856f2a94b4b5698f9ea43ef0f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceCustomMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceCustomMetrics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceCustomMetrics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1fa55d9b924fc9efc78aa7bc6e3d74c15151305aa262b4863e589fe65b4f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionBackendServiceCustomMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceCustomMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__852ae399136ab91edf36a4b72773bb37f251d3b47d7e1862c7f39ec664cfba5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05c03eae2bc08bd3ab79b327e57cecd1b8dff018a5c8c2079bfba65f30b36e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dryRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3863a8be4bdd467fcc6781f89d85c88cbc15f5538ef09d54fd9ec30822f28503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceCustomMetrics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceCustomMetrics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceCustomMetrics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f0d970982f5c3961e966a86e1509270ec78605a980089f4bae3ad9df425dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceFailoverPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "disable_connection_drain_on_failover": "disableConnectionDrainOnFailover",
        "drop_traffic_if_unhealthy": "dropTrafficIfUnhealthy",
        "failover_ratio": "failoverRatio",
    },
)
class ComputeRegionBackendServiceFailoverPolicy:
    def __init__(
        self,
        *,
        disable_connection_drain_on_failover: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drop_traffic_if_unhealthy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        failover_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disable_connection_drain_on_failover: On failover or failback, this field indicates whether connection drain will be honored. Setting this to true has the following effect: connections to the old active pool are not drained. Connections to the new active pool use the timeout of 10 min (currently fixed). Setting to false has the following effect: both old and new connections will have a drain timeout of 10 min. This can be set to true only if the protocol is TCP. The default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#disable_connection_drain_on_failover ComputeRegionBackendService#disable_connection_drain_on_failover}
        :param drop_traffic_if_unhealthy: This option is used only when no healthy VMs are detected in the primary and backup instance groups. When set to true, traffic is dropped. When set to false, new connections are sent across all VMs in the primary group. The default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#drop_traffic_if_unhealthy ComputeRegionBackendService#drop_traffic_if_unhealthy}
        :param failover_ratio: The value of the field must be in [0, 1]. If the ratio of the healthy VMs in the primary backend is at or below this number, traffic arriving at the load-balanced IP will be directed to the failover backend. In case where 'failoverRatio' is not set or all the VMs in the backup backend are unhealthy, the traffic will be directed back to the primary backend in the "force" mode, where traffic will be spread to the healthy VMs with the best effort, or to all VMs when no VM is healthy. This field is only used with l4 load balancing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#failover_ratio ComputeRegionBackendService#failover_ratio}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6284ed9b159f56d80a68611ca0b561c5a0fa9ff4c4f6d4b57864ec2d5c4c4c3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#disable_connection_drain_on_failover ComputeRegionBackendService#disable_connection_drain_on_failover}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#drop_traffic_if_unhealthy ComputeRegionBackendService#drop_traffic_if_unhealthy}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#failover_ratio ComputeRegionBackendService#failover_ratio}
        '''
        result = self._values.get("failover_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceFailoverPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceFailoverPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceFailoverPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17f7c0552e4067873dc9d263beba6d8d2a9214effc8b9d4460061fff573b8466)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ae2c82c68cb277cf0b8b9e729afec5be6df66bfc5b7c93db6b52d8852cc7362)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd88abb42f8372b9f02b2b941f46ab10cdbf30850188b49c268c209efd5b7c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropTrafficIfUnhealthy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failoverRatio")
    def failover_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failoverRatio"))

    @failover_ratio.setter
    def failover_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f29fbbe3ae76726c9fd92dc85e94a761b043d5e3ee926cb0e966cf866d6823b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceFailoverPolicy]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceFailoverPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceFailoverPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c1420fa32d0e7b6544d46ff33d21f615f33521b2cbb93814eaebf4cda6238a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceIap",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "oauth2_client_id": "oauth2ClientId",
        "oauth2_client_secret": "oauth2ClientSecret",
    },
)
class ComputeRegionBackendServiceIap:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        oauth2_client_id: typing.Optional[builtins.str] = None,
        oauth2_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether the serving infrastructure will authenticate and authorize all incoming requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enabled ComputeRegionBackendService#enabled}
        :param oauth2_client_id: OAuth2 Client ID for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#oauth2_client_id ComputeRegionBackendService#oauth2_client_id}
        :param oauth2_client_secret: OAuth2 Client Secret for IAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#oauth2_client_secret ComputeRegionBackendService#oauth2_client_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d6ececf941f643a1e253241ed5cdd3b118d1ce0799c7500a5881efda2d4f1b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enabled ComputeRegionBackendService#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def oauth2_client_id(self) -> typing.Optional[builtins.str]:
        '''OAuth2 Client ID for IAP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#oauth2_client_id ComputeRegionBackendService#oauth2_client_id}
        '''
        result = self._values.get("oauth2_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth2_client_secret(self) -> typing.Optional[builtins.str]:
        '''OAuth2 Client Secret for IAP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#oauth2_client_secret ComputeRegionBackendService#oauth2_client_secret}
        '''
        result = self._values.get("oauth2_client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceIap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceIapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceIapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__393a5e670cd1080a97347f695ca218be5b8b65fdbcf5b9a660f574e128317df2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c399a54c82e65fa83e4a84fd64d007c62b0290c75a79740e03650800ca64522c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientId")
    def oauth2_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2ClientId"))

    @oauth2_client_id.setter
    def oauth2_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f4d193408e9ba6f0d7d60ea8ab47c19e0c8257fafce87e00dc47be842f81a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2ClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientSecret")
    def oauth2_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauth2ClientSecret"))

    @oauth2_client_secret.setter
    def oauth2_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f917ad4a226fcfd428e938a1ec29f5bf7137a8e710c69b0a95f82df21ef35ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauth2ClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRegionBackendServiceIap]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceIap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceIap],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf5be8938c09405557128de3592a24365a490c956a44ad68f98ecd30300fd63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceLogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable": "enable",
        "optional_fields": "optionalFields",
        "optional_mode": "optionalMode",
        "sample_rate": "sampleRate",
    },
)
class ComputeRegionBackendServiceLogConfig:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        optional_mode: typing.Optional[builtins.str] = None,
        sample_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable: Whether to enable logging for the load balancer traffic served by this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enable ComputeRegionBackendService#enable}
        :param optional_fields: Specifies the fields to include in logging. This field can only be specified if logging is enabled for this backend service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#optional_fields ComputeRegionBackendService#optional_fields}
        :param optional_mode: Specifies the optional logging mode for the load balancer traffic. Supported values: INCLUDE_ALL_OPTIONAL, EXCLUDE_ALL_OPTIONAL, CUSTOM. Possible values: ["INCLUDE_ALL_OPTIONAL", "EXCLUDE_ALL_OPTIONAL", "CUSTOM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#optional_mode ComputeRegionBackendService#optional_mode}
        :param sample_rate: This field can only be specified if logging is enabled for this backend service. The value of the field must be in [0, 1]. This configures the sampling rate of requests to the load balancer where 1.0 means all logged requests are reported and 0.0 means no logged requests are reported. The default value is 1.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#sample_rate ComputeRegionBackendService#sample_rate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e185711bb1ea583316001ddc5812a92d7ecca9eb17279f9d4a8a3cb58e3199fa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enable ComputeRegionBackendService#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def optional_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the fields to include in logging.

        This field can only be specified if logging is enabled for this backend service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#optional_fields ComputeRegionBackendService#optional_fields}
        '''
        result = self._values.get("optional_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def optional_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the optional logging mode for the load balancer traffic. Supported values: INCLUDE_ALL_OPTIONAL, EXCLUDE_ALL_OPTIONAL, CUSTOM. Possible values: ["INCLUDE_ALL_OPTIONAL", "EXCLUDE_ALL_OPTIONAL", "CUSTOM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#optional_mode ComputeRegionBackendService#optional_mode}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#sample_rate ComputeRegionBackendService#sample_rate}
        '''
        result = self._values.get("sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a816928e8483eb7fae1bb464b0e5cc3d5d67175b4adeca118360b8db38fa0c42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9c8edd729f954a3ff969d7ced5931df429a474af2c9ffa47e7a63175bc252c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optionalFields")
    def optional_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "optionalFields"))

    @optional_fields.setter
    def optional_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32cb13e87dd9fcd3b5099a3391b4a0104d7aa84fa68541a406307b4340b07ca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionalFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optionalMode")
    def optional_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "optionalMode"))

    @optional_mode.setter
    def optional_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc39788cb94d9bc80a06093e4e19b447c65d911bdcf75c20e416fda283a9a549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionalMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRate")
    def sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRate"))

    @sample_rate.setter
    def sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9835ef1c1f7f2077e32cfb4f7cf972a9424a5d92b18829ae455648f70112f9aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRegionBackendServiceLogConfig]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5469b01a71f51ffce1fc43497651cd8cd367fc147b71216876ecc9468966575f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceOutlierDetection",
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
class ComputeRegionBackendServiceOutlierDetection:
    def __init__(
        self,
        *,
        base_ejection_time: typing.Optional[typing.Union["ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime", typing.Dict[builtins.str, typing.Any]]] = None,
        consecutive_errors: typing.Optional[jsii.Number] = None,
        consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_errors: typing.Optional[jsii.Number] = None,
        enforcing_consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
        enforcing_success_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[typing.Union["ComputeRegionBackendServiceOutlierDetectionInterval", typing.Dict[builtins.str, typing.Any]]] = None,
        max_ejection_percent: typing.Optional[jsii.Number] = None,
        success_rate_minimum_hosts: typing.Optional[jsii.Number] = None,
        success_rate_request_volume: typing.Optional[jsii.Number] = None,
        success_rate_stdev_factor: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param base_ejection_time: base_ejection_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#base_ejection_time ComputeRegionBackendService#base_ejection_time}
        :param consecutive_errors: Number of errors before a host is ejected from the connection pool. When the backend host is accessed over HTTP, a 5xx return code qualifies as an error. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#consecutive_errors ComputeRegionBackendService#consecutive_errors}
        :param consecutive_gateway_failure: The number of consecutive gateway failures (502, 503, 504 status or connection errors that are mapped to one of those status codes) before a consecutive gateway failure ejection occurs. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#consecutive_gateway_failure ComputeRegionBackendService#consecutive_gateway_failure}
        :param enforcing_consecutive_errors: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive 5xx. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enforcing_consecutive_errors ComputeRegionBackendService#enforcing_consecutive_errors}
        :param enforcing_consecutive_gateway_failure: The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive gateway failures. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enforcing_consecutive_gateway_failure ComputeRegionBackendService#enforcing_consecutive_gateway_failure}
        :param enforcing_success_rate: The percentage chance that a host will be actually ejected when an outlier status is detected through success rate statistics. This setting can be used to disable ejection or to ramp it up slowly. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enforcing_success_rate ComputeRegionBackendService#enforcing_success_rate}
        :param interval: interval block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#interval ComputeRegionBackendService#interval}
        :param max_ejection_percent: Maximum percentage of hosts in the load balancing pool for the backend service that can be ejected. Defaults to 10%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_ejection_percent ComputeRegionBackendService#max_ejection_percent}
        :param success_rate_minimum_hosts: The number of hosts in a cluster that must have enough request volume to detect success rate outliers. If the number of hosts is less than this setting, outlier detection via success rate statistics is not performed for any host in the cluster. Defaults to 5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#success_rate_minimum_hosts ComputeRegionBackendService#success_rate_minimum_hosts}
        :param success_rate_request_volume: The minimum number of total requests that must be collected in one interval (as defined by the interval duration above) to include this host in success rate based outlier detection. If the volume is lower than this setting, outlier detection via success rate statistics is not performed for that host. Defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#success_rate_request_volume ComputeRegionBackendService#success_rate_request_volume}
        :param success_rate_stdev_factor: This factor is used to determine the ejection threshold for success rate outlier ejection. The ejection threshold is the difference between the mean success rate, and the product of this factor and the standard deviation of the mean success rate: mean - (stdev * success_rate_stdev_factor). This factor is divided by a thousand to get a double. That is, if the desired factor is 1.9, the runtime value should be 1900. Defaults to 1900. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#success_rate_stdev_factor ComputeRegionBackendService#success_rate_stdev_factor}
        '''
        if isinstance(base_ejection_time, dict):
            base_ejection_time = ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime(**base_ejection_time)
        if isinstance(interval, dict):
            interval = ComputeRegionBackendServiceOutlierDetectionInterval(**interval)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31264aa696be4bc65965ff2b65434998bab515628e1db3edb2f5cd054c701f28)
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
    ) -> typing.Optional["ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime"]:
        '''base_ejection_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#base_ejection_time ComputeRegionBackendService#base_ejection_time}
        '''
        result = self._values.get("base_ejection_time")
        return typing.cast(typing.Optional["ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime"], result)

    @builtins.property
    def consecutive_errors(self) -> typing.Optional[jsii.Number]:
        '''Number of errors before a host is ejected from the connection pool.

        When the
        backend host is accessed over HTTP, a 5xx return code qualifies as an error.
        Defaults to 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#consecutive_errors ComputeRegionBackendService#consecutive_errors}
        '''
        result = self._values.get("consecutive_errors")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def consecutive_gateway_failure(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive gateway failures (502, 503, 504 status or connection errors that are mapped to one of those status codes) before a consecutive gateway failure ejection occurs.

        Defaults to 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#consecutive_gateway_failure ComputeRegionBackendService#consecutive_gateway_failure}
        '''
        result = self._values.get("consecutive_gateway_failure")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enforcing_consecutive_errors(self) -> typing.Optional[jsii.Number]:
        '''The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive 5xx.

        This setting can be used to disable
        ejection or to ramp it up slowly. Defaults to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enforcing_consecutive_errors ComputeRegionBackendService#enforcing_consecutive_errors}
        '''
        result = self._values.get("enforcing_consecutive_errors")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enforcing_consecutive_gateway_failure(self) -> typing.Optional[jsii.Number]:
        '''The percentage chance that a host will be actually ejected when an outlier status is detected through consecutive gateway failures.

        This setting can be
        used to disable ejection or to ramp it up slowly. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enforcing_consecutive_gateway_failure ComputeRegionBackendService#enforcing_consecutive_gateway_failure}
        '''
        result = self._values.get("enforcing_consecutive_gateway_failure")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enforcing_success_rate(self) -> typing.Optional[jsii.Number]:
        '''The percentage chance that a host will be actually ejected when an outlier status is detected through success rate statistics.

        This setting can be used to
        disable ejection or to ramp it up slowly. Defaults to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#enforcing_success_rate ComputeRegionBackendService#enforcing_success_rate}
        '''
        result = self._values.get("enforcing_success_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(
        self,
    ) -> typing.Optional["ComputeRegionBackendServiceOutlierDetectionInterval"]:
        '''interval block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#interval ComputeRegionBackendService#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional["ComputeRegionBackendServiceOutlierDetectionInterval"], result)

    @builtins.property
    def max_ejection_percent(self) -> typing.Optional[jsii.Number]:
        '''Maximum percentage of hosts in the load balancing pool for the backend service that can be ejected. Defaults to 10%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#max_ejection_percent ComputeRegionBackendService#max_ejection_percent}
        '''
        result = self._values.get("max_ejection_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_rate_minimum_hosts(self) -> typing.Optional[jsii.Number]:
        '''The number of hosts in a cluster that must have enough request volume to detect success rate outliers.

        If the number of hosts is less than this setting, outlier
        detection via success rate statistics is not performed for any host in the
        cluster. Defaults to 5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#success_rate_minimum_hosts ComputeRegionBackendService#success_rate_minimum_hosts}
        '''
        result = self._values.get("success_rate_minimum_hosts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_rate_request_volume(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of total requests that must be collected in one interval (as defined by the interval duration above) to include this host in success rate based outlier detection.

        If the volume is lower than this setting, outlier
        detection via success rate statistics is not performed for that host. Defaults
        to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#success_rate_request_volume ComputeRegionBackendService#success_rate_request_volume}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#success_rate_stdev_factor ComputeRegionBackendService#success_rate_stdev_factor}
        '''
        result = self._values.get("success_rate_stdev_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceOutlierDetection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#seconds ComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#nanos ComputeRegionBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa64565ae7dcd9029c04ae62f02eebf905da65efb0e65322f28fff1ca350b66f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#seconds ComputeRegionBackendService#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#nanos ComputeRegionBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceOutlierDetectionBaseEjectionTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceOutlierDetectionBaseEjectionTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1b4d52c6f097b8af762f1527243c3b216c70026e93351580e81f3f6acc4328a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba796b9116b9f9f5c6f3ddf003d644e37b80d8c5105fd939c9cedd65c15a8e24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d372452a1f948a5936fb55c52dcf828b625c72c56a708e70bc25456fc0f0d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8328d8e4d73ad479db129c3d66f759aa237db727c3a73a42f9fc7ed7087855e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceOutlierDetectionInterval",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeRegionBackendServiceOutlierDetectionInterval:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#seconds ComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#nanos ComputeRegionBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e194a33b9788b599baf9e9987fafc1b67df3cc422a71b885a1df2d4c22b3aa5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#seconds ComputeRegionBackendService#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#nanos ComputeRegionBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceOutlierDetectionInterval(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceOutlierDetectionIntervalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceOutlierDetectionIntervalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2c083d002cae0d7253b1124a155d8f8b65d09644ebc3e28a8d6aaa2266a294e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c294b7121abc0666e7afe5f202a9c24f79033158cec3434ee099492a1393cf87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb099efbdf1d5e67d416fa237ef093cc2a8dfdf205b48e18f44fca817e7ce56d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceOutlierDetectionInterval]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceOutlierDetectionInterval], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceOutlierDetectionInterval],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d27e21b509b1b8ac0f5fba6d837e21835a63adb2f48421dcda762ff2e60faa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionBackendServiceOutlierDetectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceOutlierDetectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__011b9b06afbe37fea03099005c40b0dfd101dc018f7abdf8fe26c52848193861)
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#seconds ComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#nanos ComputeRegionBackendService#nanos}
        '''
        value = ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime(
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#seconds ComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 'seconds' field and a positive 'nanos' field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#nanos ComputeRegionBackendService#nanos}
        '''
        value = ComputeRegionBackendServiceOutlierDetectionInterval(
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
    ) -> ComputeRegionBackendServiceOutlierDetectionBaseEjectionTimeOutputReference:
        return typing.cast(ComputeRegionBackendServiceOutlierDetectionBaseEjectionTimeOutputReference, jsii.get(self, "baseEjectionTime"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(
        self,
    ) -> ComputeRegionBackendServiceOutlierDetectionIntervalOutputReference:
        return typing.cast(ComputeRegionBackendServiceOutlierDetectionIntervalOutputReference, jsii.get(self, "interval"))

    @builtins.property
    @jsii.member(jsii_name="baseEjectionTimeInput")
    def base_ejection_time_input(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime], jsii.get(self, "baseEjectionTimeInput"))

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
    ) -> typing.Optional[ComputeRegionBackendServiceOutlierDetectionInterval]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceOutlierDetectionInterval], jsii.get(self, "intervalInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__88c5ee37a5fd33884c73f335a3b4f82e5466b509c5e1816e0796dccc38730d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consecutiveErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consecutiveGatewayFailure")
    def consecutive_gateway_failure(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "consecutiveGatewayFailure"))

    @consecutive_gateway_failure.setter
    def consecutive_gateway_failure(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffeb92147c6e36e8a37a33f8670602fd763b17a8a99e41f1a99d5d6556c9687a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consecutiveGatewayFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcingConsecutiveErrors")
    def enforcing_consecutive_errors(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enforcingConsecutiveErrors"))

    @enforcing_consecutive_errors.setter
    def enforcing_consecutive_errors(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56b0379c16d60c2adf12895aebb98bbb86526fd099736e00571045e6c3dd47cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcingConsecutiveErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcingConsecutiveGatewayFailure")
    def enforcing_consecutive_gateway_failure(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enforcingConsecutiveGatewayFailure"))

    @enforcing_consecutive_gateway_failure.setter
    def enforcing_consecutive_gateway_failure(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47c19b03ea44b765caf71d1a888d0b60e8851dca3fd58da440b96fa549a9f5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcingConsecutiveGatewayFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcingSuccessRate")
    def enforcing_success_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "enforcingSuccessRate"))

    @enforcing_success_rate.setter
    def enforcing_success_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd36605d052be670fb357374c368fd6f0d0554fe4965be9ab6ea99f9badaa3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcingSuccessRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxEjectionPercent")
    def max_ejection_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxEjectionPercent"))

    @max_ejection_percent.setter
    def max_ejection_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39040ddd37b0234eeae24abfa9d9071f75ec893b631ecbe1b681549471fcf3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxEjectionPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successRateMinimumHosts")
    def success_rate_minimum_hosts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successRateMinimumHosts"))

    @success_rate_minimum_hosts.setter
    def success_rate_minimum_hosts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d10cf732b79a8e90d66da46fbda026047a15fbcdffe4cd5ac40c0ba2da603f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successRateMinimumHosts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successRateRequestVolume")
    def success_rate_request_volume(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successRateRequestVolume"))

    @success_rate_request_volume.setter
    def success_rate_request_volume(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d7d66d813561d17dcdb15c85f72841df60791a1776e23b07c8a556bdbd5483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successRateRequestVolume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successRateStdevFactor")
    def success_rate_stdev_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successRateStdevFactor"))

    @success_rate_stdev_factor.setter
    def success_rate_stdev_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77075c5fdda55a634fd4c2a99bf33e2ae5df6a7d8b7a6d4ae5e0b6341945221f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successRateStdevFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceOutlierDetection]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceOutlierDetection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceOutlierDetection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed348d2a88da51d2c1b969848cc895cc8569f7ee22fee82d176246d2dd18c30e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceStrongSessionAffinityCookie",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "ttl": "ttl"},
)
class ComputeRegionBackendServiceStrongSessionAffinityCookie:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[typing.Union["ComputeRegionBackendServiceStrongSessionAffinityCookieTtl", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#name ComputeRegionBackendService#name}
        :param path: Path to set for the cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#path ComputeRegionBackendService#path}
        :param ttl: ttl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#ttl ComputeRegionBackendService#ttl}
        '''
        if isinstance(ttl, dict):
            ttl = ComputeRegionBackendServiceStrongSessionAffinityCookieTtl(**ttl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9378953c64af82d31ae6d47e568ef9e29032a75967eb1306a7dfcef9ec0aa1f8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#name ComputeRegionBackendService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to set for the cookie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#path ComputeRegionBackendService#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(
        self,
    ) -> typing.Optional["ComputeRegionBackendServiceStrongSessionAffinityCookieTtl"]:
        '''ttl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#ttl ComputeRegionBackendService#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional["ComputeRegionBackendServiceStrongSessionAffinityCookieTtl"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceStrongSessionAffinityCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceStrongSessionAffinityCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceStrongSessionAffinityCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64917d220e57d84ebbb5a066c45627257bbbc8e21f32dcf3c23d88d66a230cb1)
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#seconds ComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#nanos ComputeRegionBackendService#nanos}
        '''
        value = ComputeRegionBackendServiceStrongSessionAffinityCookieTtl(
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
    ) -> "ComputeRegionBackendServiceStrongSessionAffinityCookieTtlOutputReference":
        return typing.cast("ComputeRegionBackendServiceStrongSessionAffinityCookieTtlOutputReference", jsii.get(self, "ttl"))

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
    ) -> typing.Optional["ComputeRegionBackendServiceStrongSessionAffinityCookieTtl"]:
        return typing.cast(typing.Optional["ComputeRegionBackendServiceStrongSessionAffinityCookieTtl"], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b07e914d7466d2be985779bb15af135920f0785033ee850d1023f394590fb44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c10ba4758f0a3fb8e96c7c07fede17f75517d480ccb55e44f9685ad88c3c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceStrongSessionAffinityCookie]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceStrongSessionAffinityCookie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceStrongSessionAffinityCookie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5a40f4e1c5a8af8085d8078be24a600dc7e197897a57476c7e55bde9e447d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceStrongSessionAffinityCookieTtl",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeRegionBackendServiceStrongSessionAffinityCookieTtl:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#seconds ComputeRegionBackendService#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#nanos ComputeRegionBackendService#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c93ac9a6c1238802e9635c9ce9dca44da2854d356f5d3a5d5bbffc188dcd5764)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#seconds ComputeRegionBackendService#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#nanos ComputeRegionBackendService#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceStrongSessionAffinityCookieTtl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceStrongSessionAffinityCookieTtlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceStrongSessionAffinityCookieTtlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97ab3f93e36c6345a2bad86fb925e77a292cdad1c76fe8b06798a6cc9474ab69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ad9ebbc269eb85f80d178753d7cd2f98348d1dd5f3fc298ed13c87ef378951c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e678514e0896719c3d29873870f84a41b66ae9617e283726218a82fe732b5f8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionBackendServiceStrongSessionAffinityCookieTtl]:
        return typing.cast(typing.Optional[ComputeRegionBackendServiceStrongSessionAffinityCookieTtl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionBackendServiceStrongSessionAffinityCookieTtl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36fcd83b4576afda39ae4cfe4e4e7d86ab7556d90e8b2f6c7864f999ae546dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRegionBackendServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#create ComputeRegionBackendService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#delete ComputeRegionBackendService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#update ComputeRegionBackendService#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18cc7d41a5763bea88d6890ef53a58815c2a431a2ce1701601f37fec23f383f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#create ComputeRegionBackendService#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#delete ComputeRegionBackendService#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_backend_service#update ComputeRegionBackendService#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionBackendServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionBackendServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionBackendService.ComputeRegionBackendServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7db88d4d9ee44acb375b3abb4ebb88e33da2212efdc92198816b1721d42f28f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b496f041f0d5cef9ffd80a6f446f92be5ead56b92ff58f2c574ff2c4b299dada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe07316d81bb70c9ec70f7de1664f0abcab07eaefb28ede6201ec2fc4b21b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67203a5d196ab7aeb3045ad9eac685da31577d319cf0561d479e7bf7ce3d92f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b93aa246a7bb917b5ae90ffb2d74ad3dc9d55a81a1f1a2b1ac14a09aabd74a26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRegionBackendService",
    "ComputeRegionBackendServiceBackend",
    "ComputeRegionBackendServiceBackendCustomMetrics",
    "ComputeRegionBackendServiceBackendCustomMetricsList",
    "ComputeRegionBackendServiceBackendCustomMetricsOutputReference",
    "ComputeRegionBackendServiceBackendList",
    "ComputeRegionBackendServiceBackendOutputReference",
    "ComputeRegionBackendServiceCdnPolicy",
    "ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy",
    "ComputeRegionBackendServiceCdnPolicyCacheKeyPolicyOutputReference",
    "ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy",
    "ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyList",
    "ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicyOutputReference",
    "ComputeRegionBackendServiceCdnPolicyOutputReference",
    "ComputeRegionBackendServiceCircuitBreakers",
    "ComputeRegionBackendServiceCircuitBreakersOutputReference",
    "ComputeRegionBackendServiceConfig",
    "ComputeRegionBackendServiceConsistentHash",
    "ComputeRegionBackendServiceConsistentHashHttpCookie",
    "ComputeRegionBackendServiceConsistentHashHttpCookieOutputReference",
    "ComputeRegionBackendServiceConsistentHashHttpCookieTtl",
    "ComputeRegionBackendServiceConsistentHashHttpCookieTtlOutputReference",
    "ComputeRegionBackendServiceConsistentHashOutputReference",
    "ComputeRegionBackendServiceCustomMetrics",
    "ComputeRegionBackendServiceCustomMetricsList",
    "ComputeRegionBackendServiceCustomMetricsOutputReference",
    "ComputeRegionBackendServiceFailoverPolicy",
    "ComputeRegionBackendServiceFailoverPolicyOutputReference",
    "ComputeRegionBackendServiceIap",
    "ComputeRegionBackendServiceIapOutputReference",
    "ComputeRegionBackendServiceLogConfig",
    "ComputeRegionBackendServiceLogConfigOutputReference",
    "ComputeRegionBackendServiceOutlierDetection",
    "ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime",
    "ComputeRegionBackendServiceOutlierDetectionBaseEjectionTimeOutputReference",
    "ComputeRegionBackendServiceOutlierDetectionInterval",
    "ComputeRegionBackendServiceOutlierDetectionIntervalOutputReference",
    "ComputeRegionBackendServiceOutlierDetectionOutputReference",
    "ComputeRegionBackendServiceStrongSessionAffinityCookie",
    "ComputeRegionBackendServiceStrongSessionAffinityCookieOutputReference",
    "ComputeRegionBackendServiceStrongSessionAffinityCookieTtl",
    "ComputeRegionBackendServiceStrongSessionAffinityCookieTtlOutputReference",
    "ComputeRegionBackendServiceTimeouts",
    "ComputeRegionBackendServiceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7a7d193a662f1e9eb4abcaa96ce0135d0dd9f195f8f24db270c1567f4623d748(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    affinity_cookie_ttl_sec: typing.Optional[jsii.Number] = None,
    backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cdn_policy: typing.Optional[typing.Union[ComputeRegionBackendServiceCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    circuit_breakers: typing.Optional[typing.Union[ComputeRegionBackendServiceCircuitBreakers, typing.Dict[builtins.str, typing.Any]]] = None,
    connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
    consistent_hash: typing.Optional[typing.Union[ComputeRegionBackendServiceConsistentHash, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionBackendServiceCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    failover_policy: typing.Optional[typing.Union[ComputeRegionBackendServiceFailoverPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    iap: typing.Optional[typing.Union[ComputeRegionBackendServiceIap, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address_selection_policy: typing.Optional[builtins.str] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    locality_lb_policy: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[ComputeRegionBackendServiceLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[builtins.str] = None,
    outlier_detection: typing.Optional[typing.Union[ComputeRegionBackendServiceOutlierDetection, typing.Dict[builtins.str, typing.Any]]] = None,
    port_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    strong_session_affinity_cookie: typing.Optional[typing.Union[ComputeRegionBackendServiceStrongSessionAffinityCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionBackendServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1c1c489a40d0b1d2011dcead9940c2ccc75e15677f4f938843b5f16e0495c23a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__705381bd496efb783ebe0f0ad360b9465d3fa796207cea7a63f6cb943ca18d55(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec60033f7de262bba5265cc6c164f9485c8b95f71ab9eeae5eb7d492670f422d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionBackendServiceCustomMetrics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c9500e4e9fa93a91b304c7e3e135ccf3d7f2a324b03504bc533c94c5a2df32(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562c8e062732203e76fac17c68d7268e9b836f2e291e4137b9d74474d5235398(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306edbc75d0eb09cd430efdaaa8fe4ba6cca369f0343b0685ace0323a1801649(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f99af0ba03bc970ff0be137026d8fb594305f0ca1bd95bda538343ad7fae74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba169d163fd0341ebbbfce11a9608f6e5b63e1a95308893e2731f7c62e35e35(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0969e93341a32202ba7e523eca85fd1ee559e04f9d426de5310155b1cbbb02c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ac0ee0f0f2eeaa2b07bee93f26ecc5cc20217e4db90a75b0dff430377397d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09da2d78ec50a281748ef4e20814f3f26e79186dea33f8ac2e95723aec8c35e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8506a937369ced4764e829b71f8065eedb9f3a7c2570925faea401e3f50db486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55621c9e6967bdd01d61bfa1a858a6202f0b5315cd29ba41c2e209758ce86117(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ebfe702142c520c92089bdb02cba19284e5d5acb56a2fd2c617b5686d4f37e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c666b75001d11f84a61aa1c90cebb2ab4672e55a574076652e3a0bc126fbaf9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333ec9777f8f7c081037d0b0ddccd0b02c8518c449592f3684754045d9a1f749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c43d834b72384b1d30c53e2abadcde998a0e82887efb5b9facc6b030754f79a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88dfda43761cc9369b3092358ef4f0ead987146f7b0686be2cd2398686706989(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94abaa06d37269786924a92c0395e3fcd0057dce5ec470ee0d4ad0525e8e87dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3297937f636756385624c47a28ecd8391715e93182b1a77e7f5a54f6a1c8b2e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84ffd6da46f54b7caae12c227efde4a29b7de94f73341429b4bb6ce82854084(
    *,
    group: builtins.str,
    balancing_mode: typing.Optional[builtins.str] = None,
    capacity_scaler: typing.Optional[jsii.Number] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionBackendServiceBackendCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__130c3901929158e06b86da89d4571f764fae179ba8ef51f68bff75a32ee20d3e(
    *,
    dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    max_utilization: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e907b8f41b47fa050dac6f72acef38a5aa3527ce800258dc6c54205f7ef749ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045c42abd849ab15a60bc8eeaa2be4d6351b44f8bf9eb86e307cb4df8007f995(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc43e141c5a01617ab39574e5a31d729bfe3b7377109b1911fe8d0be082b582(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83a453daf016c3e618f8806c18096154b09e4fbf51cae3a0decdf47577ce949(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d3cd5e6fcd01fd1dd4e9691a6c11ccfe22962451c2402634828aef62011b96(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1dbaf6236eb1a270cb18a5e19743a5150638832766eca96f863983226a1e8b6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceBackendCustomMetrics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f302beba5cc705c9c1b55ea95d0d17159907c51fa08d957f9b049889f2383029(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aafd438a07f357a3f32c827753c2dd7b1d11add84af84249ae4be324300158b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2249c26bf6154d3dde47d84dbb496cda52fe52c116cea61232025424e1513640(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab537b52277742ee60d59293531cbb3b8dbf02478a44c8b40b16353657c30b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafcc1d2c7289b088ba6bf00b6db6e95805d3fe7d4719239ed12e34aec325e18(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceBackendCustomMetrics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ad42b62c7034037df6fc0e372a47ce12ed5f93d1047398fff955799fe8755c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02ae8c7d4c6acec6fc1cb094ec69c8816cc8abeb6c377db26a31e7ec4c4004a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028f467394e4f5484d38e2d9f947ae8a9de767c733136d6400bc0df293924768(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9871a41436307fb3773b0f8858a5f8765984313d301f66c5350dd168a360ba8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459f5d087073020ef953274782f3c5fb40b6e8081ac3f9b7b6bb4b7a26ff62f3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73780d72a57dc4a7a334bb18f154754c4810a2a6351aaaaf535b669624adaedf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceBackend]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60ce72a29b9b8de82524f272e9c3c7f49ec5af24b170508559ba4020de545dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f300eacb5a35cd587e8be25d170b826b16cb4e9bc66eb68336ffed6487b3fca(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionBackendServiceBackendCustomMetrics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e500bbc3bbb861cca45fe1d2c899d6b659e32cf42f577fbbc9906756eb18f8a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b15898ea02857144bba2101c6cf8424fa9a6b06e92c8e33cdeb1c21df9f1ed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdf14163bf15227bed8d3a287ff6d0ebad8f3b56bbc987dc8936910f03004a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356f1c06306b3b0e72ac3b00a4bf9e195bab9f8c9adf46c55c59e2c408f7f302(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb817b5f899ab00fc085a04229b510b7725dda0bdd7ccf99554a25346aa4c50a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5e880db719f7758dd97ae75b9f11e62b368ea91165c429ac2a66e9766eade1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5590596f24602ec0f459ce85a1e674563336573ebd3ad4c4d7c496f1e7d93d3b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7a98a74dd102bfc173678cff8473b9ed57de54141e2446488e61ffbdd98298(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9caa2aee99e9ccd5d0e14d437bc570087206c9dc240392a23f02978917c0bb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d2bf64589f55d182149e66f228a3c2fb527656d1644b8df4013fa02ad4c9bc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0d747f033db0b1f1be871e7383d114ae1edabfa84ae0f195d4ef04a789fc24(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3174f5c4fe5f7edf9a50e38789ba5b00700fcc4b7000f11540b8b77875d31e01(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8a1426035a988f574e8c5b459f65b49e20b11aa45ea89b8ecdcaf66fa0034b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceBackend]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f762ad61dc54ad3d79699c5aed3f9b69e4e6b50d5e56cb4ffdcb354b86c3172(
    *,
    cache_key_policy: typing.Optional[typing.Union[ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    cache_mode: typing.Optional[builtins.str] = None,
    client_ttl: typing.Optional[jsii.Number] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    max_ttl: typing.Optional[jsii.Number] = None,
    negative_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    negative_caching_policy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    serve_while_stale: typing.Optional[jsii.Number] = None,
    signed_url_cache_max_age_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379568ce93934ee39c05535e079cd33a2e12de9b3f2e29276b6a8637f132bedf(
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

def _typecheckingstub__199c372215c35b0865ae27599f11e07814fdf9ec61c6b06c34c3458bc268261e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa71c2205f76cc9daee07d33568428a7b868016707f7d68fb3c720cc6231765(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647d5d507b4b2c0685f384e891132dc149015b3867ed296427358ac552ad7ea4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065faa1b914207b3e2105d5b9ac053e3c6c206d5402b5e154d1a9f334cb27434(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432d5cac0d48501477135da33b0c1480bfb775faa681aac7bc5864969dc717aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63dc0e3e76553beea908d3dd430b8f00f6c84b3a226cb383c8602357a250133c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de07ebb57db02540135ca77305cf6ea4b2fa8cb06dcab09b4e7d5857ba3d521(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d8275ffbd9c4685f84025e63e43f56ef49d2c0a892cb094d32090271ae5903(
    value: typing.Optional[ComputeRegionBackendServiceCdnPolicyCacheKeyPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab605d31c904330c0eaff74295beb59394008283eba9048b27c64a7ad8eff93a(
    *,
    code: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f22ea4a5a32175e50467b7c9884a3bb0ee0837e874757ab185255d32fd511d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae51cc8232aba4e45810dbcb7366a432badac90c16fe950a8884267b06656d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00b710afed83d789074b329b34c3efca94bfe67bc48300c57d7b694acc92488(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e99505de1cdbc633a081027b2938957ed3ab8cb9c81d0975f444fd5d65cfa0b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f317bd613505711d880fe6b6b3a07db7e455d0589f2c21c85b8d3189b7703abb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8ce4267a145c0945f579aef11116d86bae77795092937c475709b93572898f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f044a9b2b9291f7bf321a3ceb7f065717aaadab5a80ff64b968a62db155d0239(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f120e1419fd3a83795d7034b40bf7092c0432ffcaabef0d5dcde262757bc0dc2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762e126574a8f2a98fe6f6b8ab38ea3112bf683014ffb108c0c2706eb9ae32a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afcc3fcf86329631cc19ce6537e0b1b9730cdee91cf19e622991e3886d18a3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fafe9e418813c27bb86b466da4afe5cf9926e19d5abac5eaddca8df7f6a3b95(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionBackendServiceCdnPolicyNegativeCachingPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea9599261f5800799bf190ce789cbb1bd8b50f25ce1c95441e7e6e72a78de93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f741e54aa48e0ba4d404b2c7a0a5800c2d17feb3493760085e9b8afca785b64c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091e61f296ec1f9e760ed81656614ce61bec3da6415a857c08fb51882995e0ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9d12a8353403405940014d2fe4f33866be6cae9285093a77a5366d565d15fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d841e23d6d935d9ad3a75aaa84820fb2fe7ddd846840311bdecd266180a80000(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89df93bccd2c6efb1d0c9d89a266e435387de7707231f7a2a68d8da30f06a37(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908d3e436e2044802a3d1eec93b50b82c90ad0cec10dd19d6e12eaafdb49cc1d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ffb386b50fdf9e0c7b64ea26c0a5022760515a83b4fa6b585c9b68c6f3dd1dd(
    value: typing.Optional[ComputeRegionBackendServiceCdnPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__266a5682df9681a59744226a311495815409a6484e6aa17c82ee4d35af09af83(
    *,
    max_connections: typing.Optional[jsii.Number] = None,
    max_pending_requests: typing.Optional[jsii.Number] = None,
    max_requests: typing.Optional[jsii.Number] = None,
    max_requests_per_connection: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893780769ac8d37355e438525acbd4aed3a005fc80fd17d25190253cfe09411d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82019ede3e01a5eeb54fe45d89e3c9d001ded87341ba441c5c02598bd71aaa3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc6ff032c620d59d5bdba15c2bc5ce9d343ce3d4c0fa9a9fc64b058b8e40a67(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c91658cb74df1dc152ca198e9700175b8784a3cef2f99491c1d0cef297a334b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600c89c29a6a6fd707558664e49aecee221b8ae2860bff5f0819d34f324f36e9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a28d216d508cd81aa3bb776b09b29429a1e999d3438f84f5504cb93a0a89b45(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0ed6399f9ad92500995d35e4410b7fa0c21fcd0bd76414bf350ccedb8ae9b1(
    value: typing.Optional[ComputeRegionBackendServiceCircuitBreakers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942d906da0191287bd3769b8797469069205f1e711375baabdb5fd74249f6e12(
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
    backend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionBackendServiceBackend, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cdn_policy: typing.Optional[typing.Union[ComputeRegionBackendServiceCdnPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    circuit_breakers: typing.Optional[typing.Union[ComputeRegionBackendServiceCircuitBreakers, typing.Dict[builtins.str, typing.Any]]] = None,
    connection_draining_timeout_sec: typing.Optional[jsii.Number] = None,
    consistent_hash: typing.Optional[typing.Union[ComputeRegionBackendServiceConsistentHash, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionBackendServiceCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_cdn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    failover_policy: typing.Optional[typing.Union[ComputeRegionBackendServiceFailoverPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    health_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    iap: typing.Optional[typing.Union[ComputeRegionBackendServiceIap, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address_selection_policy: typing.Optional[builtins.str] = None,
    load_balancing_scheme: typing.Optional[builtins.str] = None,
    locality_lb_policy: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[ComputeRegionBackendServiceLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[builtins.str] = None,
    outlier_detection: typing.Optional[typing.Union[ComputeRegionBackendServiceOutlierDetection, typing.Dict[builtins.str, typing.Any]]] = None,
    port_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    session_affinity: typing.Optional[builtins.str] = None,
    strong_session_affinity_cookie: typing.Optional[typing.Union[ComputeRegionBackendServiceStrongSessionAffinityCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionBackendServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186f5d67feab665bb2d4876bd04486790631383e709402ca1ff6c65f62dc27f9(
    *,
    http_cookie: typing.Optional[typing.Union[ComputeRegionBackendServiceConsistentHashHttpCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    http_header_name: typing.Optional[builtins.str] = None,
    minimum_ring_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a117844a8b60b6aea7c8b6199be86460b3f62731975b7223126cba9fba95cc5(
    *,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[typing.Union[ComputeRegionBackendServiceConsistentHashHttpCookieTtl, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073af85ae8f145e89c0d5a6c02390e588b2b6158f11b6834ad5e3eedf8f6eafb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81d61906c2938b5058b5b3d96276cd846669df06a2d7be3ff48e0580b42b86e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3495691e0fed2f3a351c6eb3e1c93e43d07afaa46d80c5875ccb512e64235d07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a667f311f1b74f716e42760ebf889e3384726f1561a58a4f19ec74276d95df(
    value: typing.Optional[ComputeRegionBackendServiceConsistentHashHttpCookie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b9966f17083683869b8e88c1cd71c1a24155c4b3a05ef6336b2b68d9e8c4c3(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5360707d67fb0c194038bc663fda444dd849b87b5ade6f5bc97540aba8b40692(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc497e516adef4ade1a0ff25b07115fee1c668e30888d712360d2b8e311d1b14(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca4459ee7821e229e9ab5c67900a99758d62700ffb4ce37d823db6e56d7098f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44d4a364777f5e9c836721c84e417a1767afb63f2f4cbb4419ebc476a261eb8(
    value: typing.Optional[ComputeRegionBackendServiceConsistentHashHttpCookieTtl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2fa8ba75b1ca993fdb1e4a1b65887c59accc42b8dd809ae58e1694dda3dbf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098d8871222d597232b4ff357617d254894e28ca18b5eae2e590eeee7fefc59a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93de2d2732df7a7bc8a92b1f6fcc21733a3fb155471dc957412fd690d82568a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557cf970794dc4fd129c66c4f38e0caf6700d46d8f42557a6318623f6d4c7e53(
    value: typing.Optional[ComputeRegionBackendServiceConsistentHash],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4885d6085a557703688baaccad3119738a381a9b10ad7258044a50521c9e825(
    *,
    dry_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e237b5b5ee456158ce434f0b85a61980442a3d683542f8107802f077e1b883f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1060662a7b4193f0253b02a7e8e8c922ed6061045e66054459215f4b4ab46e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dad9033b6fb4a5c78fdf2f658e68d5c01b3b5546de1204d114e874a98ace06a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec940866bab432036dc39a9ed084275aaa067a7b9c001189931835eed0a7fd7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7441d9426509298ab31a27a517475b14327535856f2a94b4b5698f9ea43ef0f8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1fa55d9b924fc9efc78aa7bc6e3d74c15151305aa262b4863e589fe65b4f8d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionBackendServiceCustomMetrics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852ae399136ab91edf36a4b72773bb37f251d3b47d7e1862c7f39ec664cfba5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c03eae2bc08bd3ab79b327e57cecd1b8dff018a5c8c2079bfba65f30b36e28(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3863a8be4bdd467fcc6781f89d85c88cbc15f5538ef09d54fd9ec30822f28503(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f0d970982f5c3961e966a86e1509270ec78605a980089f4bae3ad9df425dee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceCustomMetrics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6284ed9b159f56d80a68611ca0b561c5a0fa9ff4c4f6d4b57864ec2d5c4c4c3(
    *,
    disable_connection_drain_on_failover: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drop_traffic_if_unhealthy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    failover_ratio: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f7c0552e4067873dc9d263beba6d8d2a9214effc8b9d4460061fff573b8466(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae2c82c68cb277cf0b8b9e729afec5be6df66bfc5b7c93db6b52d8852cc7362(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd88abb42f8372b9f02b2b941f46ab10cdbf30850188b49c268c209efd5b7c6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f29fbbe3ae76726c9fd92dc85e94a761b043d5e3ee926cb0e966cf866d6823b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c1420fa32d0e7b6544d46ff33d21f615f33521b2cbb93814eaebf4cda6238a(
    value: typing.Optional[ComputeRegionBackendServiceFailoverPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d6ececf941f643a1e253241ed5cdd3b118d1ce0799c7500a5881efda2d4f1b(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    oauth2_client_id: typing.Optional[builtins.str] = None,
    oauth2_client_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393a5e670cd1080a97347f695ca218be5b8b65fdbcf5b9a660f574e128317df2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c399a54c82e65fa83e4a84fd64d007c62b0290c75a79740e03650800ca64522c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f4d193408e9ba6f0d7d60ea8ab47c19e0c8257fafce87e00dc47be842f81a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f917ad4a226fcfd428e938a1ec29f5bf7137a8e710c69b0a95f82df21ef35ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf5be8938c09405557128de3592a24365a490c956a44ad68f98ecd30300fd63(
    value: typing.Optional[ComputeRegionBackendServiceIap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e185711bb1ea583316001ddc5812a92d7ecca9eb17279f9d4a8a3cb58e3199fa(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    optional_mode: typing.Optional[builtins.str] = None,
    sample_rate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a816928e8483eb7fae1bb464b0e5cc3d5d67175b4adeca118360b8db38fa0c42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c8edd729f954a3ff969d7ced5931df429a474af2c9ffa47e7a63175bc252c4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32cb13e87dd9fcd3b5099a3391b4a0104d7aa84fa68541a406307b4340b07ca1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc39788cb94d9bc80a06093e4e19b447c65d911bdcf75c20e416fda283a9a549(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9835ef1c1f7f2077e32cfb4f7cf972a9424a5d92b18829ae455648f70112f9aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5469b01a71f51ffce1fc43497651cd8cd367fc147b71216876ecc9468966575f(
    value: typing.Optional[ComputeRegionBackendServiceLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31264aa696be4bc65965ff2b65434998bab515628e1db3edb2f5cd054c701f28(
    *,
    base_ejection_time: typing.Optional[typing.Union[ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime, typing.Dict[builtins.str, typing.Any]]] = None,
    consecutive_errors: typing.Optional[jsii.Number] = None,
    consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
    enforcing_consecutive_errors: typing.Optional[jsii.Number] = None,
    enforcing_consecutive_gateway_failure: typing.Optional[jsii.Number] = None,
    enforcing_success_rate: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[typing.Union[ComputeRegionBackendServiceOutlierDetectionInterval, typing.Dict[builtins.str, typing.Any]]] = None,
    max_ejection_percent: typing.Optional[jsii.Number] = None,
    success_rate_minimum_hosts: typing.Optional[jsii.Number] = None,
    success_rate_request_volume: typing.Optional[jsii.Number] = None,
    success_rate_stdev_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa64565ae7dcd9029c04ae62f02eebf905da65efb0e65322f28fff1ca350b66f(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b4d52c6f097b8af762f1527243c3b216c70026e93351580e81f3f6acc4328a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba796b9116b9f9f5c6f3ddf003d644e37b80d8c5105fd939c9cedd65c15a8e24(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d372452a1f948a5936fb55c52dcf828b625c72c56a708e70bc25456fc0f0d3b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8328d8e4d73ad479db129c3d66f759aa237db727c3a73a42f9fc7ed7087855e9(
    value: typing.Optional[ComputeRegionBackendServiceOutlierDetectionBaseEjectionTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e194a33b9788b599baf9e9987fafc1b67df3cc422a71b885a1df2d4c22b3aa5(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c083d002cae0d7253b1124a155d8f8b65d09644ebc3e28a8d6aaa2266a294e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c294b7121abc0666e7afe5f202a9c24f79033158cec3434ee099492a1393cf87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb099efbdf1d5e67d416fa237ef093cc2a8dfdf205b48e18f44fca817e7ce56d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d27e21b509b1b8ac0f5fba6d837e21835a63adb2f48421dcda762ff2e60faa(
    value: typing.Optional[ComputeRegionBackendServiceOutlierDetectionInterval],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011b9b06afbe37fea03099005c40b0dfd101dc018f7abdf8fe26c52848193861(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c5ee37a5fd33884c73f335a3b4f82e5466b509c5e1816e0796dccc38730d76(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffeb92147c6e36e8a37a33f8670602fd763b17a8a99e41f1a99d5d6556c9687a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b0379c16d60c2adf12895aebb98bbb86526fd099736e00571045e6c3dd47cd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47c19b03ea44b765caf71d1a888d0b60e8851dca3fd58da440b96fa549a9f5c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd36605d052be670fb357374c368fd6f0d0554fe4965be9ab6ea99f9badaa3c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39040ddd37b0234eeae24abfa9d9071f75ec893b631ecbe1b681549471fcf3d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d10cf732b79a8e90d66da46fbda026047a15fbcdffe4cd5ac40c0ba2da603f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d7d66d813561d17dcdb15c85f72841df60791a1776e23b07c8a556bdbd5483(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77075c5fdda55a634fd4c2a99bf33e2ae5df6a7d8b7a6d4ae5e0b6341945221f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed348d2a88da51d2c1b969848cc895cc8569f7ee22fee82d176246d2dd18c30e(
    value: typing.Optional[ComputeRegionBackendServiceOutlierDetection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9378953c64af82d31ae6d47e568ef9e29032a75967eb1306a7dfcef9ec0aa1f8(
    *,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[typing.Union[ComputeRegionBackendServiceStrongSessionAffinityCookieTtl, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64917d220e57d84ebbb5a066c45627257bbbc8e21f32dcf3c23d88d66a230cb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b07e914d7466d2be985779bb15af135920f0785033ee850d1023f394590fb44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c10ba4758f0a3fb8e96c7c07fede17f75517d480ccb55e44f9685ad88c3c58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5a40f4e1c5a8af8085d8078be24a600dc7e197897a57476c7e55bde9e447d4(
    value: typing.Optional[ComputeRegionBackendServiceStrongSessionAffinityCookie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93ac9a6c1238802e9635c9ce9dca44da2854d356f5d3a5d5bbffc188dcd5764(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ab3f93e36c6345a2bad86fb925e77a292cdad1c76fe8b06798a6cc9474ab69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad9ebbc269eb85f80d178753d7cd2f98348d1dd5f3fc298ed13c87ef378951c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e678514e0896719c3d29873870f84a41b66ae9617e283726218a82fe732b5f8a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36fcd83b4576afda39ae4cfe4e4e7d86ab7556d90e8b2f6c7864f999ae546dc(
    value: typing.Optional[ComputeRegionBackendServiceStrongSessionAffinityCookieTtl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18cc7d41a5763bea88d6890ef53a58815c2a431a2ce1701601f37fec23f383f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db88d4d9ee44acb375b3abb4ebb88e33da2212efdc92198816b1721d42f28f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b496f041f0d5cef9ffd80a6f446f92be5ead56b92ff58f2c574ff2c4b299dada(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe07316d81bb70c9ec70f7de1664f0abcab07eaefb28ede6201ec2fc4b21b96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67203a5d196ab7aeb3045ad9eac685da31577d319cf0561d479e7bf7ce3d92f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93aa246a7bb917b5ae90ffb2d74ad3dc9d55a81a1f1a2b1ac14a09aabd74a26(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionBackendServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
